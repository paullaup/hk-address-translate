import utils
import re, json

def count_matched(full_address: str, address_component: dict, block: str, input_address_component: dict = {}) -> int:
    """
    Count how many components from address_component_dict are present in full_address.

    :param full_address: The complete address string.
    :param address_component_dict: A dictionary with address components as keys.
    :return: The count of matched components.
    """
    match_count = 0
    for key in address_component.keys():
        component = utils.standardize_address(address_component[key])

        #check 
        if(key in input_address_component.keys() and input_address_component[key]):
             if(not re.search(r'\b' + re.escape(component) + r'\b', full_address, re.IGNORECASE)):
                return -1
             

        #handle block number separately to improve matching accuracy, as block number is often a substring of the full address and can lead to false positives
        if(key == "BlockNo" and block):
                    if(component.lower() == block.lower()):
                        match_count += 1
                        continue

        #check if a full word match exists in the full_address instead of a substring match
        if re.search(r'\b' + re.escape(component) + r'\b', full_address, re.IGNORECASE):
            match_count += 1
    return match_count

def translate_address(full_address: str, lookup_file_path: str, address_components: dict) -> dict:
    """
    Translate a full address into its components using predefined dictionaries.

    :param full_address: The complete address string.
    :param lookup_file_path: The file path to the JSON file containing address.
    :param address_components: A dictionary of address components in specific field to be matched
    :return: A dictionary with translated address components.
    """ 
    #extract block number to improve matching accuracy
    block = utils.extract_block(full_address)
    if(block):
        full_address = full_address.lower().replace(block.lower(), '').strip()

    with open(lookup_file_path, "r", encoding="utf-8") as file:
        collectionList = json.load(file).get("features", [])
        match = {"matchCount": 0}
        for collection in collectionList:

            #get only the leaf node English address components for better iteration
            engAddress = collection["properties"]["Address"]["PremisesAddress"]["EngPremisesAddress"]
            formatedEngAddress = utils.flatten_dict(engAddress, ['EngDistrict', 'Region', 'EngDistrict'])

            #count the mached components and update the best match if necessary
            match_count = count_matched(full_address, formatedEngAddress, block, address_components)
            if(match_count > match["matchCount"]):
                match = collection["properties"]["Address"]["PremisesAddress"]["ChiPremisesAddress"]
                match["matchCount"] = match_count
                match["matchRate"] = (match_count/len(formatedEngAddress))
        return match    