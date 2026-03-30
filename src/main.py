import os, json
import utils, translate

def main():
    # json_str = """
    #         {
    #           "EngPremisesAddress": {
    #             "EngEstate": {
    #               "EstateName": "KING'S COLLEGE OLD BOYS' ASSOCIATION PRIMARY SCHOOL"
    #             },
    #             "EngStreet": {
    #               "BuildingNoFrom": "58",
    #               "StreetName": "BRIDGES STREET"
    #             },
    #             "EngDistrict": "CENTRAL & WESTERN DISTRICT",
    #             "Region": "HK"
    #           }
    #         }
    #         """
    # data = json.loads(json_str)
    # print(utils.flatten_dict(data, ['EngDistrict', 'Region', 'EngDistrict']))
    print(translate.translate_address("lam wai house lam tin estate, lam tin, kwun tong, kowloon"))


if __name__ == "__main__":
    main()
