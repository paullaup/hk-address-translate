#prepare data for ai training
import pandas as pd
import pathlib

#load the extracted buildings table
project_root = pathlib.Path(__file__).parent.parent
data_path = project_root / "buildings_table.csv"
df = pd.read_csv(data_path)

training_data = []

for idx, row in df.iterrows():
    eng_address = row['eng_full_address']

    entities = []

    for col in df.columns:
        if not col.startswith('eng_'):
            continue
        value = str(row[col])
        if value and value != 'nan':
            start_idx = eng_address.find(value)
            if start_idx != -1:
                end_idx = start_idx + len(value)
                label = col.replace('eng_', '').upper()
                entities.append((start_idx, end_idx, label))

    training_data.append((eng_address, {"entities": entities}))

#save training data to a file
output_path = project_root / "training_data.pkl"
import pickle
with open(output_path, 'wb') as f:
    pickle.dump(training_data, f)