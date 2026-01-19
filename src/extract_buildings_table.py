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
            flat.update(flatten_address(value, prefix))
        else:
            flat[f"{prefix}_{key}"] = value
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
        chi_flat = flatten_address(chi_addr, "chi")
        building.update(chi_flat)
        
        # Flatten EngPremisesAddress
        eng_addr = address.get('EngPremisesAddress', {})
        eng_flat = flatten_address(eng_addr, "eng")
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

    #order the columns according to the logic of full address construction
    order = '''v-bkey, 
        northing, easting, latitude, longitude, 
        eng_buildingnofrom, eng_buildingnoto, eng_blockno, eng_blockdescriptor, eng_blockdescriptorprecedenceindicator, eng_buildingname,
        eng_phaseno, eng_phasename, eng_estatename, eng_villagename, eng_locationname, 
        eng_streetname, eng_engdistrict, eng_region,
        chi_region, chi_chidistrict, chi_streetname, chi_villagename, chi_estatename, chi_locationname, 
        chi_phasename, chi_phaseno, chi_buildingname, chi_blockdescriptor, chi_blockno, 
        chi_buildingnoto, chi_buildingnofrom,
        geo_address, eng_full_address, chi_full_address'''
    ordered_cols = [col.strip() for col in order.split(',')]
    df = df[[col for col in ordered_cols if col in df.columns]]

    # calculate the full address by concatenating all column starting with 'eng_'
    eng_address_cols = [col for col in df.columns if col.startswith('eng_')]
    df['eng_full_address'] = df[eng_address_cols].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)
    chi_address_cols = [col for col in df.columns if col.startswith('chi_')]
    df['chi_full_address'] = df[chi_address_cols].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)

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