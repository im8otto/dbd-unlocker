import os
import json
from mitmproxy import http
from Utils import Misc

status = True  
url = "api/v1/dbd-character-data/get-all"  
filename = "GetAll.json"
custom_data_filename = "CustomCharacterData.json"
custom_status = True

def request(flow: http.HTTPFlow):
    try:
        getall_path = os.path.join(Misc.market_updater_path, "Files", filename)

        if not os.path.exists(getall_path):
            Misc.print_log(f"ERROR: {getall_path} doesn't exist.")
            return

        with open(getall_path, "r") as getall_file:
            getall_json = Misc.normalize_keys(json.load(getall_file))
        
        if custom_status:
            custom_data_path = os.path.join(Misc.market_updater_path, "Other", custom_data_filename)
            if os.path.exists(custom_data_path):
                with open(custom_data_path, "r") as custom_data_file:
                    custom_data = Misc.normalize_keys(json.load(custom_data_file))

                for char in getall_json["list"]:
                    character_name = char["charactername"]
                    for custom_char in custom_data["list"]:
                        if custom_char["charactername"] == character_name:
                            char["prestigelevel"] = custom_char["prestigelevel"]
                            break
        
        flow.response = http.Response.make(
            200,  
            json.dumps(getall_json),  
            {"Content-Type": "application/json"}  
        )
        Misc.print_log("GetAll successfully loaded")
    except Exception as e:
        Misc.print_log("Error processing GetAll")
        Misc.print_log(str(e))