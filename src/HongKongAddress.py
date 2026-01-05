import json, re
def subDistrictToDistrict(subDistrict: str):
    subDistrictMap = {
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
    "DEEP WATER BAY": "Southern",

    "WAN CHAI": "Wan Chai",
    "CAUSEWAY BAY": "Wan Chai",
    "HAPPY VALLEY": "Wan Chai",
    "TAI HANG": "Wan Chai",
    "SO KON PO": "Wan Chai",
    "JARDINE'S LOOKOUT": "Wan Chai",


    "HO MAN TIN": "Kowloon City",
    "TO KWA WAN": "Kowloon City",
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
    "CHA KWO LING": "Kwun Tong",

    "SHAM SHUI PO": "Sham Shui Po",
    "SHEK KIP MEI": "Sham Shui Po",
    "MEI FOO": "Sham Shui Po",
    "CHEUNG SHA WAN": "Sham Shui Po",
    "YAU YAT TSUEN": "Sham Shui Po",
    "YAU YAT CHUEN": "Sham Shui Po",
    "TAI WO PING": "Sham Shui Po",
    "STONECUTTERS ISLAND": "Sham Shui Po",
    "LAI CHI KOK": "Sham Shui Po",
    "KOWLOON TONG": "Sham Shui Po",


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
    "LANTAU": "Islands",
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
    "SHATIN": "Sha Tin",
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
    "YAU KAM TAU": "Tsuen Wan",


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
    return subDistrictMap.get(subDistrict.upper(), None)

def flattenDict(dictionary: dict, excludedKeys: list) -> dict:
    """
    make the dictionary one level only 
    """
    result = {'ComponentsKeys': []}
    for key in dictionary.keys():
        if(key in excludedKeys):
            continue
        elif(type(dictionary[key]) == type(dict())):
            inner = flattenDict(dictionary[key], excludedKeys)
            result["ComponentsKeys"].extend(inner["ComponentsKeys"])
            del inner["ComponentsKeys"]
            result.update(inner)
        else:
            result[key] = dictionary[key]
            result["ComponentsKeys"].append(key)

    return result

def calculateMatchCount(formatedEngAddress: dict, block: str, inputAddress: str, inputAddressdict: dict) -> int:
    """
    Calculate the match count for a formatted English address against the input address.
    """
    matchCount = 0
    isContinue = False
    for key in formatedEngAddress["ComponentsKeys"]:
        item = standardizeAddress(formatedEngAddress[key])
        if(key == "BlockNo" and block):
            print(item, block)
            if(item == block.lower()):
                matchCount += 1
                continue
        # if(inputAddressdict.get(key, None)):
        #     if(not item or not checkIfCompleteWordExist(inputAddressdict[key], item)):
        #         isContinue = True
        #         break
        if(checkIfCompleteWordExist(item, inputAddress)): 
            matchCount += 1 
    return matchCount


def parseFulladdress(district: str, inputAddress: str, inputAddressdict : dict = {}):
    """
    translate english address to chinese address component, \n
    find the address that meet most of the words in the full address \n
    force to meet all the address components by input the address components seperately in a dictionary addressComponents{region, streetName , buildingNoFrom, buildingNoTo, estateName , phaseName, blockString, buildingName , villageName , locationName} \n
    \n example: {'StreetName': 'kwun tong street', 'BlockNo': 'A'}
    """
    block = extractBlock(inputAddress)
    if(block):
        inputAddress = inputAddress.lower().replace(block.lower(), '').strip()

    if(district.lower() == "central and western"):
        district = "central & western"

    districtReformat = "_".join(district.split(" "))
    filePath = rf"C:\Users\paul_ip\Documents\data\hong_kong_address_json\als_addresses_({districtReformat}_district).geojson"
    try:
        with open(filePath, "r", encoding="utf-8") as file:
            collectionList = json.load(file).get("features", [])
            match = {"matchCount": 0}
            for collection in collectionList:  

                #collect the data from the json 
                engAddress = collection["properties"]["Address"]["PremisesAddress"]["EngPremisesAddress"]
                formatedEngAddress = flattenDict(engAddress, ['EngDistrict', 'Region', 'BlockDescriptor', 'BlockDescriptorPrecedenceIndicator'])

                matchCount = 0
                isContinue = False
                for key in formatedEngAddress["ComponentsKeys"]:
                    item = standardizeAddress(formatedEngAddress[key])
                    if(key == "BlockNo" and block):
                        if(item.lower() == block.lower()):
                            matchCount += 1
                            continue
                    # if(inputAddressdict.get(key, None)):
                    #     if(not item or not checkIfCompleteWordExist(inputAddressdict[key], item)):
                    #         isContinue = True
                    #         break
                    if(checkIfCompleteWordExist(item, inputAddress)): 
                        matchCount += 1 

                # if(isContinue): continue
                if(matchCount > match["matchCount"]):
                    match = collection["properties"]["Address"]["PremisesAddress"]["ChiPremisesAddress"]
                    match["matchCount"] = matchCount
                    match["matchRate"] = (matchCount/len(formatedEngAddress["ComponentsKeys"]))
            return match    
    
    except RuntimeError as err:
        raise(err)


def extractDistrict(address: str): 
    address = address.lower()
    districtsList = [
        "central and western", "eastern", "southern", "wan chai",
        "kowloon city", "kwun tong", "sham shui po", "wong tai sin", "yau tsim mong",
        "islands", "kwai tsing", "north", "sai kung", "sha tin", "tai po",
        "tsuen wan", "tuen mun", "yuen long"
    ]


    matches = re.findall(f'\\b({"|".join(districtsList)})\\b', address)
    district = matches[len(matches) - 1] if matches else None
    if(district == "north" and "north point" in address):
        district = None
    return district



def extractSubdistrict(address: str):
    address = address.upper()
    subDistrictList = ["LAI CHI KOK", "YAU KAM TAU", "CHA KWO LING", "ABERDEEN", "DEEP WATER BAY", "CENTRAL", "SHEUNG WAN", "MID-LEVELS", "SAI YING PUN", "KENNEDY TOWN", "WESTERN DISTRICT", "PEAK", "SHEK TONG TSUI", "ADMIRALTY", "NORTH POINT", "QUARRY BAY", "TAI KOO", "SAI WAN HO", "SHAU KEI WAN", "CHAI WAN", "SIU SAI WAN", "TIN HAU", "BREAEMAR HILL", "POK FU LAM", "AP LEI CHAU", "WONG CHUK HANG", "TAI TAM", "STANLEY", "SHOUSON HILL", "REPULSE BAY", "CHUNG HOM KOK", "SHEK O", "WAN CHAI", "CAUSEWAY BAY", "HAPPY VALLEY", "TAI HANG", "SO KON PO", "JARDINE'S LOOKOUT", "HO MAN TIN", "TO KWA WAN", "KOWLOON TONG", "KOWLOON CITY", "HUNG HOM", "MA TAU KOK", "MA TAU WAI", "KAI TAK", "BEACON HILL", "KWUN TONG", "LAM TIN", "NGAU TAU KOK", "JORDAN VALLEY", "PING SHEK", "KOWLOON BAY", "SAU MAU PING", "YAU TONG", "LEI YUE MUN", "SHAM SHUI PO", "SHEK KIP MEI", "MEI FOO", "CHEUNG SHA WAN", "YAU YAT TSUEN", "YAU YAT CHUEN", "TAI WO PING", "STONECUTTERS ISLAND", "WONG TAI SIN", "LOK FU", "SAN PO KONG", "NGAU CHI WAN", "TUNG TAU", "WANG TAU HOM", "DIAMOND HILL", "TSZ WAN SHAN", "MONG KOK", "TSIM SHA TSUI", "JORDAN", "TAI KOK TSUI", "PRINCE EDWARD", "YAU MA TEI", "WEST KOWLOON RECLAMATION", "KING'S PARK", "DISCOVERY BAY", "TUNG CHUNG", "CHEUNG CHAU", "LANTAU ISLAND", "LANTAU", "PENG CHAU", "LAMMA ISLAND", "FANLING", "SHEUNG SHUI", "LUEN WO HUI", "SHEK WU HUI", "SHA TAU KOK", "LUK KENG", "WU KAU TANG", "SAI KUNG", "TSEUNG KWAN O", "CLEAR WATER BAY", "TAI MONG TSAI", "HANG HAU", "TIU KENG LENG", "MA YAU TONG", "SHA TIN", "SHATIN", "FO TAN", "TAI WAI", "SIU LEK YUEN", "MA LIU SHUI", "WU KAI SHA", "MA ON SHAN", "TAI PO", "TAI WO", "TAI PO MARKET", "TAI PO KAU", "TAI MEI TUK", "SUEN WAN", "CHEUNG MUK TAU", "KEI LING HA", "TSUEN WAN", "LEI MUK SHUE", "TING KAU", "SHAM TSENG", "TSING LUNG TAU", "MA WAN", "SUNNY BAY", "TUEN MUN", "SIU HONG", "TAI LAM CHUNG", "SO KWUN WAT", "LAM TEI", "YUEN LONG", "TIN SHUI WAI", "KAM TIN", "HUNG SHUI KIU", "HA TSUEN", "LAU FAU SHAN", "SAN TIN", "LOK MA CHAU", "SHEK KONG", "PAT HEUNG", "KWAI CHUNG", "TSING YI"]
    subdistrict = re.findall(f'\\b({"|".join(subDistrictList)})\\b', address)
    for item in reversed(subdistrict):
        if(checkIfCompleteWordExist(item, address)):
            return item
        

def checkIfCompleteWordExist(word: str, fullString: str):
    """
    Check if a word exists as a complete word (not as substring) in the full string.s
    Handles punctuation, case sensitivity, and word boundaries properly.
    """
    pattern = rf'\b{re.escape(word.strip())}\b'
    return bool(re.search(pattern, fullString, re.IGNORECASE))

def extractBlock(address: str):
    address = address.upper()
    blockMatch = re.search(r'\bBLOCK\s+([A-Z0-9]*)\b', address, re.IGNORECASE)
    if blockMatch:
        return blockMatch.group(1)
    return None

def standardizeAddress(address: str):
    """
    this function is used to replace word for matching address like BLK into it's full form like block and Twr into Block
    """
    addressAbbreviationMap = {
        r'\bBLDG\b': 'Building',
        r'\bBLK\b': "Block",
        r'\bTWR\b': 'Block',
        r'\bHSE\b': 'House',
        r'\bQTR\b': 'Quarters',
        r'\bMANSN\b': 'Mansions',
        r'\bGDN\b': 'Gardens',
        r'\bCTR\b': 'Centre',
        r'\bCENTER\b': 'Centre',
        r'\bEST\b': 'Estate',
        r'\bST\b': 'Street',
        r'\bRD\b': 'Road',
        r'\bAVE\b': 'Avenue',
        r'\bIND\b': 'Industrial',
        r'\bINST\b': "Institution",
        r'\bTER\b': 'Terrace',
        r"(?<!')\bN\b": 'North',
        r"(?<!')\bE\b": 'East',
        r"(?<!')\bS\b": 'South',
        r"(?<!')\bW\b": 'West'
    }

    address = f' {address} ' # allow to use space for a complete word check in replace word
    for key in addressAbbreviationMap.keys():
        match = re.findall(key, address, re.IGNORECASE)
        if(match):
            original = match[0]
            newText = addressAbbreviationMap[key]
            address = address.replace(f' {original} ', f' {newText} ')

    addressAbbreviationMapSpecial = {
        r'\b(PH(\w*))\b': 'Phase'
    }
    for key in addressAbbreviationMapSpecial.keys():
        match = re.findall(key, address, re.IGNORECASE)
        if(match):
            newText = f'{addressAbbreviationMapSpecial[key]} {match[0][1]}'
            original = match[0][0]
            address = address.replace(f' {original} ', f' {newText} ')
        
    return address.strip()


def formatRoadName(address: str):
    """
    Assume address are in format {ROAD NAME} {PART NAME}

    """
    castlePeakRoadParts = {'LINGNAN', 'TSUEN WAN', 'SHAM TSENG', 'SAN TIN', 'PING SHAN', 'HUNG SHUI KIU', 'TSING LUNG TAU', 'YUEN LONG', 'SAN HUI', 'CASTLE PEAK BAY', 'CHAU TAU', 'TAM MI', 'KWAI CHUNG', 'MAI PO', 'TING KAU', 'KWU TUNG', 'LAM TEI', 'TAI LAM'}
    shaTauKokRoadParts = {'LUNG YEUK TAU', 'SHEK CHUNG AU', 'MA MEI HA', 'WO HANG'}
    taiPoRoadParts = {'SHA TIN HEIGHTS', 'TAI WAI', 'SHA TIN', 'TAI WO', 'TAI PO KAU'}
    road = ""
    roadParts = {}
    if("CASTLE PEAK ROAD" in address):
        road = "CASTLE PEAK ROAD"
        roadParts = castlePeakRoadParts
    elif("TAI PO ROAD" in address):
        road = "TAI PO ROAD"
        roadParts = taiPoRoadParts
    elif("SHA TAU KOK ROAD" in address):
        road = "SHA TAU KOK ROAD"
        roadParts = shaTauKokRoadParts

    if(road):
        part = re.findall(rf'\b{"|".join(roadParts)}\b', address, re.IGNORECASE)
        original = f'{road} {part[0]}'
        newText = f'{road} - {part[0]}'
        address = address.upper().replace(original, newText)
    return address






def main():
    # print()
    # while True:
    #     address = input("input the full address")
    #     district = extractDistrict(address)
    #     if(not district):
    #         subdistrict = extractSubdistrict(address)
    #         district = subDistrictToDistrict(subdistrict)

    #     address = standardizeAddress(address)
    #     address = formatRoadName(address)

    #     print(parseFulladdress(district, address, {}))

    json_str = '''
            "EngPremisesAddress": {
              "EngBlock": {
                "BlockDescriptor": "TOWER",
                "BlockNo": "8",
                "BlockDescriptorPrecedenceIndicator": "Y"
              },
              "EngEstate": {
                "EstateName": "PARC OASIS"
              },
              "EngStreet": {
                "BuildingNoFrom": "33",
                "StreetName": "GRANDEUR ROAD"
              },
              "EngDistrict": "SHAM SHUI PO DISTRICT",
              "Region": "KLN"
            }'''
    

    source = json.loads(f'{{{json_str}}}').get("EngPremisesAddress")
    source = flattenDict(source,['EngDistrict', 'Region', 'BlockDescriptor', 'BlockDescriptorPrecedenceIndicator'])
    address = 'PARC OASIS 33 TAT CHEE AVE KOWLOON TONG, KLN'
    result = calculateMatchCount(source, '28', address, None)

    print(result)


if __name__ == "__main__":
    main()