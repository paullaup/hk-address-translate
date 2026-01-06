import utils
import os, re, json

def count_matched(full_address, address_component_dict) -> int:
    """
    Count how many components from address_component_dict are present in full_address.

    :param full_address: The complete address string.
    :param address_component_dict: A dictionary with address components as keys.
    :return: The count of matched components.
    """
    match_count = 0
    for component in address_component_dict.keys():
        #check if a full word match exists in the full_address instead of a substring match
        if re.search(r'\b' + re.escape(component) + r'\b', full_address):
            match_count += 1
    return match_count

def extract_block(full_address: str) -> str:
    """
    Extract block information from the full address.

    :param full_address: The complete address string.
    :return: The extracted block information or an empty string if not found.
    """
    patterns_str = [r'\bBlock\s+[A-Za-z0-9]+\b', r'\bBlk\s+[A-Za-z0-9]+\b', r'Tower\s+[A-Za-z0-9]+\b', r'Twr\s+[A-Za-z0-9]+\b']
    block_pattern = re.compile('|'.join(patterns_str), re.IGNORECASE)
    match = block_pattern.search(full_address)
    if match:
        return match.group(0)
    return None

def translate_address(full_address: str) -> dict:
    """
    Translate a full address into its components using predefined dictionaries.

    :param full_address: The complete address string.
    :return: A dictionary with translated address components.
    """
    #find the district for finding the json file to use
    district = utils.extract_district(full_address)
    if not district:
        sub_district = utils.extract_sub_district(full_address)
        if sub_district:
            district = utils.sub_district_to_district(sub_district)
        else:
            raise ValueError("District or Sub-district not found in the address.")

    #find the json file path according to the district
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if(district.lower() == "central and western"):
        district = "central & western"
    districtReformat = "_".join(district.split(" ")).lower()
    file_path = project_root / "data" / f"als_addresses_({districtReformat}_district).geojson"
    with open(file_path, "r", encoding="utf-8") as file:
        collectionList = json.load(file).get("features", [])
        match = {"matchCount": 0}
        for collection in collectionList: 
            engAddress = collection["properties"]["Address"]["PremisesAddress"]["EngPremisesAddress"]
            formatedEngAddress = utils.flatten_dict(engAddress, ['EngDistrict', 'Region', 'EngDistrict', 'BlockDescriptor', 'BlockDescriptorPrecedenceIndicator'])
            
            
            match_count = count_matched(full_address, formatedEngAddress)
            if(match_count > match["matchCount"]):
                match = collection["properties"]["Address"]["PremisesAddress"]["ChiPremisesAddress"]
                match["matchCount"] = match_count
                match["matchRate"] = (match_count/len(formatedEngAddress["ComponentsKeys"]))


        return match    