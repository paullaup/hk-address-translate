import json
import glob
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainingArguments, Seq2SeqTrainer, DataCollatorForSeq2Seq
import torch
from datasets import Dataset

def extract_addresses(file_path):
    """
    Extracts English and Chinese address pairs from a GeoJSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    pairs = []
    # Check if 'features' key exists
    if 'features' not in data:
        return []

    for feature in data['features']:
        props = feature.get('properties', {})
        if not props: continue
        
        address = props.get('Address', {}).get('PremisesAddress', {})
        if not address: continue
        
        chi_addr = address.get('ChiPremisesAddress', {})
        eng_addr = address.get('EngPremisesAddress', {})
        
        if not chi_addr or not eng_addr:
            continue
            
        # Construct Chinese Address
        # Format: Region -> District -> Street -> No -> Estate/Building
        c_region = chi_addr.get('Region', '')
        c_district = chi_addr.get('ChiDistrict', '')
        c_street_info = chi_addr.get('ChiStreet', {})
        c_street = c_street_info.get('StreetName', '') if c_street_info else ''
        c_no = c_street_info.get('BuildingNoFrom', '') if c_street_info else ''
        c_estate_info = chi_addr.get('ChiEstate', {})
        c_estate = c_estate_info.get('EstateName', '') if c_estate_info else ''
        
        full_chi = f"{c_region}{c_district}"
        if c_street:
            full_chi += c_street
        if c_no:
            full_chi += f"{c_no}號"
        if c_estate:
            full_chi += c_estate
            
        # Construct English Address
        # Format: Estate, No Street, District, Region
        e_region = eng_addr.get('Region', '')
        e_district = eng_addr.get('EngDistrict', '')
        e_street_info = eng_addr.get('EngStreet', {})
        e_street = e_street_info.get('StreetName', '') if e_street_info else ''
        e_no = e_street_info.get('BuildingNoFrom', '') if e_street_info else ''
        e_estate_info = eng_addr.get('EngEstate', {})
        e_estate = e_estate_info.get('EstateName', '') if e_estate_info else ''
        
        parts = []
        if e_estate:
            parts.append(e_estate)
        
        street_part = ""
        if e_no:
            street_part += f"{e_no} "
        if e_street:
            street_part += e_street
        if street_part:
            parts.append(street_part.strip())
            
        if e_district:
            parts.append(e_district)
        if e_region:
            parts.append(e_region)
            
        full_eng = ", ".join(parts)
        
        if full_chi and full_eng:
            pairs.append({'en': full_eng, 'zh': full_chi})
            
    return pairs

def load_all_data(data_dir):
    """
    Loads all GeoJSON files from the data directory and returns a DataFrame.
    """
    all_pairs = []
    files = glob.glob(os.path.join(data_dir, "*.geojson"))
    print(f"Found {len(files)} files in {data_dir}")
    
    for f in files:
        print(f"Processing {os.path.basename(f)}...")
        file_pairs = extract_addresses(f)
        all_pairs.extend(file_pairs)
        
    print(f"Total address pairs extracted: {len(all_pairs)}")
    return pd.DataFrame(all_pairs)

def train():
    # Path to data directory (assuming script is in src/ and data is in data/)
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    
    print("Loading data...")
    df = load_all_data(data_dir)
    
    if len(df) == 0:
        print("No data found. Please check the data directory.")
        return

    # Drop duplicates to ensure quality
    df = df.drop_duplicates()
    print(f"Unique pairs: {len(df)}")
    
    # Split data
    train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)
    print(f"Training samples: {len(train_df)}, Validation samples: {len(val_df)}")
    
    # Initialize Model and Tokenizer
    model_checkpoint = "Helsinki-NLP/opus-mt-en-zh"
    print(f"Loading model: {model_checkpoint}")
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
    
    max_input_length = 128
    max_target_length = 128
    
    def preprocess_function(examples):
        inputs = examples['en']
        targets = examples['zh']
        model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True)
        
        labels = tokenizer(text_target=targets, max_length=max_target_length, truncation=True)
            
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    # Convert to HuggingFace Dataset
    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)
    
    print("Tokenizing data...")
    tokenized_train = train_dataset.map(preprocess_function, batched=True)
    tokenized_val = val_dataset.map(preprocess_function, batched=True)
    
    # Training Arguments
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'hk-address-model')
    args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        weight_decay=0.01,
        save_total_limit=3,
        num_train_epochs=3,
        predict_with_generate=True,
        fp16=torch.cuda.is_available(),
        logging_steps=100,
    )
    
    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)
    
    trainer = Seq2SeqTrainer(
        model,
        args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_val,
        data_collator=data_collator,
        tokenizer=tokenizer,
    )
    
    print("Starting training...")
    trainer.train()
    
    print("Saving model...")
    trainer.save_model(os.path.join(output_dir, "final_model"))
    tokenizer.save_pretrained(os.path.join(output_dir, "final_model"))
    print("Training complete!")

if __name__ == "__main__":
    train()
