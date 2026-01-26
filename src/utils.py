import re, json

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

def extract_district(address: str): 
    district_list = [
        "central and western", "eastern", "southern", "wan chai",
        "kowloon city", "kwun tong", "sham shui po", "wong tai sin", "yau tsim mong",
        "islands", "kwai tsing", "north", "sai kung", "sha tin", "tai po",
        "tsuen wan", "tuen mun", "yuen long"
    ]


    district = re.findall(f'\\b({"|".join(district_list)})\\b', address.lower())
    return district[len(district) - 1] if district else None

def extract_sub_district(address: str):
    address = address.upper()
    subDistrictList = ["CENTRAL", "SHEUNG WAN", "MID-LEVELS", "SAI YING PUN", "KENNEDY TOWN", "WESTERN DISTRICT", "PEAK", "SHEK TONG TSUI", "ADMIRALTY", "NORTH POINT", "QUARRY BAY", "TAI KOO", "SAI WAN HO", "SHAU KEI WAN", "CHAI WAN", "SIU SAI WAN", "TIN HAU", "BREAEMAR HILL", "POK FU LAM", "AP LEI CHAU", "WONG CHUK HANG", "TAI TAM", "STANLEY", "SHOUSON HILL", "REPULSE BAY", "CHUNG HOM KOK", "SHEK O", "ABERDEEN", "WAN CHAI", "CAUSEWAY BAY", "HAPPY VALLEY", "TAI HANG", "SO KON PO", "JARDINE'S LOOKOUT", "HO MAN TIN", "TO KWA WAN", "KOWLOON TONG", "KOWLOON CITY", "HUNG HOM", "MA TAU KOK", "MA TAU WAI", "KAI TAK", "BEACON HILL", "KWUN TONG", "LAM TIN", "NGAU TAU KOK", "JORDAN VALLEY", "PING SHEK", "KOWLOON BAY", "SAU MAU PING", "YAU TONG", "LEI YUE MUN", "SHAM SHUI PO", "SHEK KIP MEI", "MEI FOO", "CHEUNG SHA WAN", "YAU YAT TSUEN", "TAI WO PING", "STONECUTTERS ISLAND", "WONG TAI SIN", "LOK FU", "SAN PO KONG", "NGAU CHI WAN", "TUNG TAU", "WANG TAU HOM", "DIAMOND HILL", "TSZ WAN SHAN", "MONG KOK", "TSIM SHA TSUI", "JORDAN", "TAI KOK TSUI", "PRINCE EDWARD", "YAU MA TEI", "WEST KOWLOON RECLAMATION", "KING'S PARK", "DISCOVERY BAY", "TUNG CHUNG", "CHEUNG CHAU", "LANTAU ISLAND", "PENG CHAU", "LAMMA ISLAND", "FANLING", "SHEUNG SHUI", "LUEN WO HUI", "SHEK WU HUI", "SHA TAU KOK", "LUK KENG", "WU KAU TANG", "SAI KUNG", "TSEUNG KWAN O", "CLEAR WATER BAY", "TAI MONG TSAI", "HANG HAU", "TIU KENG LENG", "MA YAU TONG", "SHA TIN", "FO TAN", "TAI WAI", "SIU LEK YUEN", "MA LIU SHUI", "WU KAI SHA", "MA ON SHAN", "TAI PO", "TAI WO", "TAI PO MARKET", "TAI PO KAU", "TAI MEI TUK", "SUEN WAN", "CHEUNG MUK TAU", "KEI LING HA", "TSUEN WAN", "LEI MUK SHUE", "TING KAU", "SHAM TSENG", "TSING LUNG TAU", "MA WAN", "SUNNY BAY", "TUEN MUN", "SIU HONG", "TAI LAM CHUNG", "SO KWUN WAT", "LAM TEI", "YUEN LONG", "TIN SHUI WAI", "KAM TIN", "HUNG SHUI KIU", "HA TSUEN", "LAU FAU SHAN", "SAN TIN", "LOK MA CHAU", "SHEK KONG", "PAT HEUNG", "KWAI CHUNG", "TSING YI"]
    subdistrict = re.findall(f'\\b({"|".join(subDistrictList)})\\b', address)
    for item in reversed(subdistrict):
        if(check_if_complete_word_exist(item, address)):
            return item
        
def extract_block(address: str):
    address = address.upper()
    blockMatch = re.search(r'\bBLOCK\s+([A-Z0-9]*)\b', address, re.IGNORECASE)
    if blockMatch:
        return blockMatch.group(1)
    return None

def standardize_address(address: str):
    """
    this function is used to replace word for matching address like BLK into it's full form like block and Twr into Block
    """
    address_abbreviation_map = {
        r'\bBLDG\b': 'Building',
        r'\bBLK\b': "Block",
        r'\bTWR\b': 'Block',
        r'\bHSE\b': 'House',
        r'\bQTR\b': 'Quarters',
        r'\bMANSN\b': 'Mansions',
        r'\bGDN\b': 'Gardens',
        r'\bCTR\b': 'Centre',
        r'\bCENTER\b': 'Center',
        r'\bEST\b': 'Estate',
        r'\bST\b': 'Street',
        r'\bRD\b': 'Road',
        r'\bAVE\b': 'Avenue',
        r'\bIND\b': 'Industrial',
        r"(?<!')\bN\b": 'North',
        r"(?<!')\bE\b": 'East',
        r"(?<!')\bS\b": 'South',
        r"(?<!')\bW\b": 'West'
    }

    address = f' {address} ' # allow to use space for a complete word check in replace word
    for key in address_abbreviation_map.keys():
        match = re.findall(key, address)
        if(match):
            original = match[0]
            new_text = address_abbreviation_map[key]
            address = address.replace(f' {original} ', f' {new_text} ')

    address_abbreviation_map_special = {
        r'\b(PH(\w*))\b': 'Phase'
    }
    for key in address_abbreviation_map_special.keys():
        match = re.findall(key, address)
        if(match):
            new_text = f'{address_abbreviation_map_special[key]} {match[0][1]}'
            original = match[0][0]
            address = address.replace(f' {original} ', f' {new_text} ')
        
    return address.strip()

def check_if_complete_word_exist(word: str, fullString: str):
    """
    Check if a word exists as a complete word (not as substring) in the full string.
    Handles punctuation, case sensitivity, and word boundaries properly.
    """
    pattern = rf'\b{re.escape(word.strip())}\b'
    return bool(re.search(pattern, fullString, re.IGNORECASE))

def format_road_name(address: str):
    """
    Assume address are in format {ROAD NAME} {PART NAME}

    """
    castle_peak_road_parts = {'LINGNAN', 'TSUEN WAN', 'SHAM TSENG', 'SAN TIN', 'PING SHAN', 'HUNG SHUI KIU', 'TSING LUNG TAU', 'YUEN LONG', 'SAN HUI', 'CASTLE PEAK BAY', 'CHAU TAU', 'TAM MI', 'KWAI CHUNG', 'MAI PO', 'TING KAU', 'KWU TUNG', 'LAM TEI', 'TAI LAM'}
    sha_tau_kok_road_parts = {'LUNG YEUK TAU', 'SHEK CHUNG AU', 'MA MEI HA', 'WO HANG'}
    tai_po_road_parts = {'SHA TIN HEIGHTS', 'TAI WAI', 'SHA TIN', 'TAI WO', 'TAI PO KAU'}
    road = ""
    road_parts = {}
    if("CASTLE PEAK ROAD" in address):
        road = "CASTLE PEAK ROAD"
        road_parts = castle_peak_road_parts
    elif("TAI PO ROAD" in address):
        road = "TAI PO ROAD"
        road_parts = tai_po_road_parts
    elif("SHA TAU KOK ROAD" in address):
        road = "SHA TAU KOK ROAD"
        road_parts = sha_tau_kok_road_parts

    if(road):
        part = re.findall(rf'\b{"|".join(road_parts)}\b', address, re.IGNORECASE)
        original = f'{road} {part[0]}'
        new_text = f'{road} - {part[0]}'
        address = address.upper().replace(original, new_text)
    return address

def sub_district_to_district(subDistrict: str):
    sub_district_map = {
    "CENTRAL": "Central and Western",
    "SHEUNG WAN": "Central and Western",
    "MID-LEVELS": "Central and Western",
    "SAI YING PUN": "Central and Western",
    "KENNEDY TOWN": "Central and Western",
    "WESTERN DISTRICT": "Central and Western",
    "PEAK": "Central and Western",
    "SHEK TONG TSUI": "Central and Western",
    "ADMIRALTY": "Central and Western",


    "NORTH POINT": "Eastern",
    "QUARRY BAY": "Eastern",
    "TAI KOO": "Eastern",
    "SAI WAN HO": "Eastern",
    "SHAU KEI WAN": "Eastern",
    "CHAI WAN": "Eastern",
    "SIU SAI WAN": "Eastern",
    "TIN HAU": "Eastern",
    "BREAEMAR HILL": "Eastern",

    "POK FU LAM": "Southern",
    "AP LEI CHAU": "Southern",
    "WONG CHUK HANG": "Southern",
    "TAI TAM": "Southern",
    "STANLEY": "Southern",
    "SHOUSON HILL": "Southern",
    "REPULSE BAY": "Southern",
    "CHUNG HOM KOK": "Southern",
    "SHEK O": "Southern",
    "ABERDEEN": "Southern",

    "WAN CHAI": "Wan Chai",
    "CAUSEWAY BAY": "Wan Chai",
    "HAPPY VALLEY": "Wan Chai",
    "TAI HANG": "Wan Chai",
    "SO KON PO": "Wan Chai",
    "JARDINE'S LOOKOUT": "Wan Chai",


    "HO MAN TIN": "Kowloon City",
    "TO KWA WAN": "Kowloon City",
    "KOWLOON TONG": "Kowloon City",
    "KOWLOON CITY": "Kowloon City",
    "HUNG HOM": "Kowloon City",
    "MA TAU KOK": "Kowloon City",
    "MA TAU WAI": "Kowloon City",
    "KAI TAK": "Kowloon City",
    "BEACON HILL": "Kowloon City",


    "KWUN TONG": "Kwun Tong",
    "LAM TIN": "Kwun Tong",
    "NGAU TAU KOK": "Kwun Tong",
    "JORDAN VALLEY": "Kwun Tong",
    "PING SHEK": "Kwun Tong",
    "KOWLOON BAY": "Kwun Tong",
    "SAU MAU PING": "Kwun Tong",
    "YAU TONG": "Kwun Tong",
    "LEI YUE MUN": "Kwun Tong",

    "SHAM SHUI PO": "Sham Shui Po",
    "SHEK KIP MEI": "Sham Shui Po",
    "MEI FOO": "Sham Shui Po",
    "CHEUNG SHA WAN": "Sham Shui Po",
    "YAU YAT TSUEN": "Sham Shui Po",
    "TAI WO PING": "Sham Shui Po",
    "STONECUTTERS ISLAND": "Sham Shui Po",


    "WONG TAI SIN": "Wong Tai Sin",
    "LOK FU": "Wong Tai Sin",
    "SAN PO KONG": "Wong Tai Sin",
    "NGAU CHI WAN": "Wong Tai Sin",
    "TUNG TAU": "Wong Tai Sin",
    "WANG TAU HOM": "Wong Tai Sin",
    "DIAMOND HILL": "Wong Tai Sin",
    "TSZ WAN SHAN": "Wong Tai Sin",

    "MONG KOK": "Yau Tsim Mong",
    "TSIM SHA TSUI": "Yau Tsim Mong",
    "JORDAN": "Yau Tsim Mong",
    "TAI KOK TSUI": "Yau Tsim Mong",
    "PRINCE EDWARD": "Yau Tsim Mong",
    "YAU MA TEI": "Yau Tsim Mong",
    "WEST KOWLOON RECLAMATION": "Yau Tsim Mong",
    "KING'S PARK": "Yau Tsim Mong",


    "DISCOVERY BAY": "Islands",
    "TUNG CHUNG": "Islands",
    "CHEUNG CHAU": "Islands",
    "LANTAU ISLAND": "Islands",
    "PENG CHAU": "Islands",
    "LAMMA ISLAND": "Islands",

    "FANLING": "North",
    "SHEUNG SHUI": "North",
    "LUEN WO HUI": "North",
    "SHEK WU HUI": "North",
    "SHA TAU KOK": "North",
    "LUK KENG": "North",
    "WU KAU TANG": "North",


    "SAI KUNG": "Sai Kung",
    "TSEUNG KWAN O": "Sai Kung",
    "CLEAR WATER BAY": "Sai Kung",
    "TAI MONG TSAI": "Sai Kung",
    "HANG HAU": "Sai Kung",
    "TIU KENG LENG": "Sai Kung",
    "MA YAU TONG": "Sai Kung",


    "SHA TIN": "Sha Tin",
    "FO TAN": "Sha Tin",
    "TAI WAI": "Sha Tin",
    "SIU LEK YUEN": "Sha Tin",
    "MA LIU SHUI": "Sha Tin",
    "WU KAI SHA": "Sha Tin",
    "MA ON SHAN": "Sha Tin",


    "TAI PO": "Tai Po",
    "TAI WO": "Tai Po",
    "TAI PO MARKET": "Tai Po",
    "TAI PO KAU": "Tai Po",
    "TAI MEI TUK": "Tai Po",
    "SUEN WAN": "Tai Po",
    "CHEUNG MUK TAU": "Tai Po",
    "KEI LING HA": "Tai Po",

    "TSUEN WAN": "Tsuen Wan",
    "LEI MUK SHUE": "Tsuen Wan",
    "TING KAU": "Tsuen Wan",
    "SHAM TSENG": "Tsuen Wan",
    "TSING LUNG TAU": "Tsuen Wan",
    "MA WAN": "Tsuen Wan",
    "SUNNY BAY": "Tsuen Wan",


    "TUEN MUN": "Tuen Mun",
    "SIU HONG": "Tuen Mun",
    "TAI LAM CHUNG" : "Tuen Mun",
    "SO KWUN WAT" : "Tuen Mun",
    "LAM TEI" : "Tuen Mun",


    "YUEN LONG": "Yuen Long",
    "TIN SHUI WAI": "Yuen Long",
    "KAM TIN": "Yuen Long",
    "HUNG SHUI KIU": "Yuen Long",
    "HA TSUEN": "Yuen Long",
    "LAU FAU SHAN": "Yuen Long",
    "SAN TIN": "Yuen Long",
    "LOK MA CHAU": "Yuen Long",
    "SHEK KONG": "Yuen Long",
    "PAT HEUNG": "Yuen Long",

    "KWAI CHUNG": "Kwai Tsing",
    "TSING YI": "Kwai Tsing"
}
    return sub_district_map.get(subDistrict.upper(), None)
