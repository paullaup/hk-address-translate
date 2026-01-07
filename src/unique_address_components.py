import json
import glob
import os
import pandas as pd
from collections import defaultdict

def flatten_dict(dictionary: dict, excludedKeys: list) -> dict:
    """
    make the dictionary one level only 
    """
    result = {}
    for key in dictionary.keys():
        if(key in excludedKeys):
            continue
        elif(type(dictionary[key]) == type(dict())):
            inner = flatten_dict(dictionary[key], excludedKeys)
            # result["ComponentsKeys"].extend(inner["ComponentsKeys"])
            # del inner["ComponentsKeys"]
            result.update(inner)
        else:
            result[key] = dictionary[key]
            # result["ComponentsKeys"].append(key)
    return result

def extract_address_components(file_path):
    """
    Extracts address components from a single GeoJSON file.
    """
    print(f'Extracting address components from {file_path}...')
    count = 0
    df = pd.DataFrame({'Column': [], 'Value': []})
    with open(file_path, "r", encoding="utf-8") as file:
        collectionList = json.load(file).get("features", [])
        for i in range(len(collectionList)):
            collection = collectionList[i]  
            #collect the data from the json 
            engAddress = collection["properties"]["Address"]["PremisesAddress"]["EngPremisesAddress"]
            formatedEngAddress = flatten_dict(engAddress, ['BlockDescriptorPrecedenceIndicator', 'BlockNo', 'BuildingNoFrom', 'BuildingNoTo', 'Region', 'PhaseNo'])
            for key in formatedEngAddress.keys():
                df = pd.concat([df, pd.DataFrame({'Column': [key], 'Value': [formatedEngAddress[key]]})], ignore_index=True)
                
                count += 1
                if(count > 1000):
                    df.drop_duplicates(inplace=True)
                    count = 0
            
    print(f'Extracted {len(df)} unique address components.')
    return df

def save_components_to_csv(components, output_dir):
    """
    Saves the collected components to separate CSV files.
    """
    address_components_types = components['Column'].unique()
    for component_type in address_components_types:
        component_df = components[components['Column'] == component_type]
        output_path = os.path.join(output_dir, f"{component_type}.csv")
        component_df.to_csv(output_path, index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    data_folder_path = r'C:\Users\paul_ip\Documents\GitHub\hk-address-translate\data'
    summary_df = pd.DataFrame({'Column': [], 'Value': []})
    #loop the data in the folder
    for file_name in os.listdir(data_folder_path):
        if not file_name.endswith('.geojson'):
            continue
        file_path = os.path.join(data_folder_path, file_name)
        components_df = extract_address_components(file_path)
        summary_df = pd.concat([summary_df, components_df], ignore_index=True)
        summary_df.drop_duplicates(inplace=True)

    output_directory = r'C:\Users\paul_ip\Documents\GitHub\hk-address-translate\address_components'
    save_components_to_csv(summary_df, output_directory)
    print("Address components have been extracted and saved to CSV files.")
