import sys
import io
from src.utils import *
from src.translate import *
import argparse

def flattenAddressDict(dictionary: dict) -> dict:
    """
    make the dictionary one level only 
    """
    result = {'ComponentsKeys': []}
    for key in dictionary.keys():
        if(type(dictionary[key]) == type(dict())):
            inner = flattenAddressDict(dictionary[key])
            result["ComponentsKeys"].extend(inner["ComponentsKeys"])
            del inner["ComponentsKeys"]
            result.update(inner)
        else:
            result[key] = dictionary[key]
            result["ComponentsKeys"].append(key)
    
    return result

#change the codec
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#define the named input
argumentParser = argparse.ArgumentParser()
argumentParser.add_argument("--fullAddress", help="Full address, better with no flat information", required=True)
argumentParser.add_argument("--streetName", help="optional, name of street")
argumentParser.add_argument("--buildNoFrom", help="optional, start of the building in the street")
argumentParser.add_argument("--buildNoTo", help="optional, end of the building number in the street")
argumentParser.add_argument("--estateName", help="optional, name of the estate")
argumentParser.add_argument("--phaseName", help="optional, name of the phase")
argumentParser.add_argument("--blockNo", help="optional, number or character of the block")
argumentParser.add_argument("--villageName", help="optional, name of the village")
argumentParser.add_argument("--locationName", help="optional, name of the location")
argumentParser.add_argument("--district", help="option, name of the district")
argumentParser.add_argument("--subDistrict", help="optional, name of the subdistrict")

#get the input value
args = argumentParser.parse_args()
fullAddress = args.fullAddress
excludedInputKeys = ["fullAddress", "district", "subDistrict"]  # Add more keys here as needed

#filter out the optional address components that are required to match 
addressComponents = { key: value for key, value in vars(args).items() if value and key not in excludedInputKeys}

#find the address district
district = args.district if(args.district) else extract_district(fullAddress)
if(not district):
    subDistrict = extract_sub_district(fullAddress)
    district = sub_district_to_district(subDistrict) if(subDistrict) else None

if(district):
    file_path = get_district_address_json_path(district)
    standardize = standardize_address(fullAddress)
    translated = translate_address(standardize, file_path, addressComponents)
    formatedOutput = flatten_dict(translated, [])
    print(formatedOutput)
else:
    print("district not found")







