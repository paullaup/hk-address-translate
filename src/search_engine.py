import pandas as pd
import difflib
import re
import os

# Abbreviations dictionary for common address abbreviations
ABBREVIATIONS = {
    'st': 'street',
    'rd': 'road',
    'ave': 'avenue',
    'blvd': 'boulevard',
    'dr': 'drive',
    'ln': 'lane',
    'ct': 'court',
    'pl': 'place',
    'sq': 'square',
    'cir': 'circle',
    'ter': 'terrace',
    'way': 'way',
    'pkwy': 'parkway',
    'hwy': 'highway',
    'blk': 'block',
    'tw': 'tower',
    'twrs': 'towers',
    'ctr': 'centre',
    'cntr': 'centre',
    'bldg': 'building',
    'apt': 'apartment',
    'fl': 'flat',
    'no': 'number',
    # Add more as needed
}

def normalize_text(text):
    """Normalize text: lowercase, remove punctuation, expand abbreviations."""
    if not isinstance(text, str):
        return ''
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # remove punctuation
    words = text.split()
    expanded = [ABBREVIATIONS.get(word, word) for word in words]
    return ' '.join(expanded)

class BuildingSearchEngine:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.addresses = []
        self.buildings = []
        self._build_index()

    def _build_index(self):
        """Build list of normalized addresses and corresponding building data."""
        for idx, row in self.df.iterrows():
            # Construct full address from English fields
            parts = []
            if pd.notna(row.get('eng_EngStreet_BuildingNoFrom')):
                parts.append(str(row['eng_EngStreet_BuildingNoFrom']))
            if pd.notna(row.get('eng_EngStreet_StreetName')):
                parts.append(row['eng_EngStreet_StreetName'])
            if pd.notna(row.get('eng_BuildingName')):
                parts.append(row['eng_BuildingName'])
            if pd.notna(row.get('eng_EngEstate_EstateName')):
                parts.append(row['eng_EngEstate_EstateName'])
            if pd.notna(row.get('eng_EngBlock_BlockNo')):
                parts.append(f"Block {row['eng_EngBlock_BlockNo']}")
            if pd.notna(row.get('eng_EngBlock_BlockDescriptor')):
                parts.append(row['eng_EngBlock_BlockDescriptor'])
            if pd.notna(row.get('eng_EngEstate_EngPhase_PhaseName')):
                parts.append(row['eng_EngEstate_EngPhase_PhaseName'])
            if pd.notna(row.get('eng_EngVillage_VillageName')):
                parts.append(row['eng_EngVillage_VillageName'])
            if pd.notna(row.get('eng_EngDistrict')):
                parts.append(row['eng_EngDistrict'])
            if pd.notna(row.get('eng_Region')):
                parts.append(row['eng_Region'])

            full_address = ', '.join(parts)
            normalized = normalize_text(full_address)
            self.addresses.append(normalized)
            self.buildings.append({
                'full_address': full_address,
                'latitude': row.get('latitude'),
                'longitude': row.get('longitude'),
                'northing': row.get('northing'),
                'easting': row.get('easting'),
                'row': row.to_dict()
            })

    def search(self, query, top_n=10, threshold=0.6):
        """Search for buildings matching the query, allowing typos and abbreviations."""
        normalized_query = normalize_text(query)
        matches = []
        for addr, building in zip(self.addresses, self.buildings):
            score = difflib.SequenceMatcher(None, normalized_query, addr).ratio()
            if score >= threshold:
                matches.append((score, building))

        # Sort by score descending
        matches.sort(key=lambda x: x[0], reverse=True)
        return matches[:top_n]

# Example usage
if __name__ == "__main__":
    print("Loading building data...")
    # Path to the CSV
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'buildings_table.csv')
    engine = BuildingSearchEngine(csv_path)
    print(f"Loaded {len(engine.addresses)} buildings.")

    # Test search
    query = "58 bridges street central western district hk"
    print(f"Searching for: {query}")
    results = engine.search(query)
    print(f"Found {len(results)} matches:")
    for score, building in results:
        print(f"Score: {score:.2f} - {building['full_address']}")
        print(f"Lat: {building['latitude']}, Lon: {building['longitude']}")
        print("---")