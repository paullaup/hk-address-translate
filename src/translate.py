import utils
import re

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

def translate_address(full_address: str) -> dict:
    """
    Translate a full address into its components using predefined dictionaries.

    :param full_address: The complete address string.
    :return: A dictionary with translated address components.
    """
    district = utils.extract_district(full_address)
    if not district:
        sub_district = utils.extrac