import json
import glob
import os
import pandas as pd

def flatten_address(address_dict, prefix=""):
    """
    Flattens a nested address dictionary into a flat dict with prefixed keys.
    """
    flat = {}
    for key, value in address_dict.items():
        if isinstance(value, dict):
            flat.update(flatten_address(value, f"{prefix}_"))
        else:
            flat[f"{prefix}{key}"] = value
    return flat

def extract_building_data(file_path):
    """
    Extracts flattened building data from a single GeoJSON file.
    """
    buildings = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    for feature in data.get('features', []):
        props = feature.get('properties', {})
        geometry = feature.get('geometry', {})
        
        # Basic fields
        building = {
            'northing': props.get('Northing'),
            'easting': props.get('Easting'),
            'latitude': geometry.get('coordinates', [None, None])[1],
            'longitude': geometry.get('coordinates', [None, None])[0],
        }
        
        address = props.get('Address', {}).get('PremisesAddress', {})
        
        # Flatten ChiPremisesAddress
        chi_addr = address.get('ChiPremisesAddress', {})
        chi_flat = flatten_address(chi_addr, "chi_")
        building.update(chi_flat)
        
        # Flatten EngPremisesAddress
        eng_addr = address.get('EngPremisesAddress', {})
        eng_flat = flatten_address(eng_addr, "eng_")
        building.update(eng_flat)
        
        # GeoAddress
        building['geo_address'] = address.get('GeoAddress')
        
        buildings.append(building)
    
    return buildings

def create_buildings_table(data_dir, output_file):
    """
    Creates a table (DataFrame) of all buildings from GeoJSON files and saves to CSV.
    """
    all_buildings = []
    files = glob.glob(os.path.join(data_dir, "*.geojson"))
    print(f"Processing {len(files)} GeoJSON files...")
    
    for file_path in files:
        print(f"Processing {os.path.basename(file_path)}...")
        buildings = extract_building_data(file_path)
        all_buildings.extend(buildings)
    
    print(f"Total buildings extracted: {len(all_buildings)}")
    
    # Create DataFrame
    df = pd.DataFrame(all_buildings)
    
    #change all column names to lowercase
    df.columns = [col.lower() for col in df.columns]

    # Save to CSV
    df['v-bkey'] = df.index
    df.set_index('v-bkey', inplace=True)
    df.to_csv(output_file, index=True)
    print(f"Data saved to {output_file}")
    
    # Print column info
    print(f"Columns: {list(df.columns)}")
    print(f"Shape: {df.shape}")

if __name__ == "__main__":
    # Path to data directory
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'buildings_table.csv')
    create_buildings_table(data_dir, output_file)