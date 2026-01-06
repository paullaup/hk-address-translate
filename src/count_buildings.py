import json
import glob
import os

def count_buildings_in_geojson(file_path):
    """
    Counts the number of features (buildings) in a single GeoJSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        features = data.get('features', [])
        return len(features)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

def count_all_buildings(data_dir):
    """
    Counts the total number of buildings across all GeoJSON files in the data directory.
    """
    total_buildings = 0
    files = glob.glob(os.path.join(data_dir, "*.geojson"))
    print(f"Found {len(files)} GeoJSON files in {data_dir}")
    
    for file_path in files:
        building_count = count_buildings_in_geojson(file_path)
        file_name = os.path.basename(file_path)
        print(f"{file_name}: {building_count} buildings")
        total_buildings += building_count
    
    print(f"\nTotal buildings across all files: {total_buildings}")
    return total_buildings

if __name__ == "__main__":
    # Path to data directory (assuming script is in src/ and data is in ../data/)
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    count_all_buildings(data_dir)