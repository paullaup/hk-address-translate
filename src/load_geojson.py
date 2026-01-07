import json
import os
import pgserver
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine
import sqlalchemy as sql
import pandas as pd

def flatten_dict(dictionary: dict, excludedKeys: list, prefix: str = "") -> dict:
    """
    make the dictionary one level only with prefixed keys
    """
    result = {}
    for key in dictionary.keys():
        if key in excludedKeys:
            continue
        elif isinstance(dictionary[key], dict):
            inner = flatten_dict(dictionary[key], excludedKeys, prefix + key + "_")
            result.update(inner)
        else:
            result[prefix + key] = dictionary[key]
    return result

# Path to PostgreSQL data directory
pgdata_path = r'C:\Users\paul_ip\Documents\GitHub\hk-address-translate\pgdata2'

# Data folder
data_folder = r'C:\Users\paul_ip\Documents\GitHub\hk-address-translate\data'

# Database name
db_name = 'mydb'

def extract_address_data(feature):
    """Extract flat address data from a geojson feature."""
    props = feature['properties']
    addr = props['Address']['PremisesAddress']
    chi = addr.get('ChiPremisesAddress', {})
    eng = addr.get('EngPremisesAddress', {})

    # Geometry
    coords = feature['geometry']['coordinates']
    longitude = coords[0]
    latitude = coords[1]

    data = {
        'northing': props.get('Northing'),
        'easting': props.get('Easting'),
        'latitude': latitude,
        'longitude': longitude,
        'geo_address': addr.get('GeoAddress'),
    }

    # Flatten ChiPremisesAddress with "chi_" prefix
    chi_flat = flatten_dict(chi, [], "chi_")
    data.update(chi_flat)

    # Flatten EngPremisesAddress with "eng_" prefix
    eng_flat = flatten_dict(eng, [], "eng_")
    data.update(eng_flat)

    # Handle BuildingName separately if needed, but since it's in chi and eng, it should be covered
    # If there are conflicts, the eng one will overwrite, but in this case, BuildingName is separate

    return data

def main():
    # Start PostgreSQL server
    db = pgserver.get_server(pgdata_path)
    db.psql('create extension vector')  # Assuming needed

    # Get database URI
    dburi = db.get_uri(database=db_name)
    if not database_exists(dburi):
        create_database(dburi)
    engine = create_engine(dburi)

    # List of geojson files
    geojson_files = [f for f in os.listdir(data_folder) if f.endswith('.geojson')]

    all_data = []

    for file in geojson_files:
        file_path = os.path.join(data_folder, file)
        print(f"Processing {file}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for feature in data['features']:
                row = extract_address_data(feature)
                all_data.append(row)

    # Create DataFrame and insert to DB
    df = pd.DataFrame(all_data)
    df.to_sql('buildings_geojson', engine, if_exists='replace', index=False)

    print(f"Inserted {len(all_data)} records into buildings_geojson table.")

    # Cleanup
    db.cleanup()

if __name__ == '__main__':
    main()