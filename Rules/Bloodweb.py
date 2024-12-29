import os
import json
from mitmproxy import http
from Utils import Misc

status = True  
url = "api/v1/dbd-character-data/bloodweb"  
filename = "Bloodweb.json"
custom_data_filename = "CustomCharacterData.json"
custom_status = True
Misc.load_settings()

def request(flow):
    try:
        bloodweb_path = os.path.join(Misc.market_updater_path, "Files", filename)

        if not os.path.exists(bloodweb_path):
            Misc.print_log(f"ERROR: {bloodweb_path} doesn't exist.")
            return
        
        with open(bloodweb_path, "r") as bloodweb_file:
            bloodweb_json = Misc.normalize_keys(json.load(bloodweb_file))
        
        flow.request.decode()
        request_json = Misc.normalize_keys(json.loads(flow.request.get_text()))
        
        character_name = request_json.get("charactername", "")
        bloodweb_json["charactername"] = character_name

        if custom_status:
            custom_data_path = os.path.join(Misc.market_updater_path, "Other", custom_data_filename)
            if os.path.exists(custom_data_path):
                with open(custom_data_path, "r") as custom_data_file:
                    custom_data = Misc.normalize_keys(json.load(custom_data_file))

                for char in custom_data["list"]:
                    if char["charactername"] == character_name:
                        bloodweb_json["prestigelevel"] = char["prestigelevel"]
                        break

        bloodweb_json["bloodweblevel"] = 50
        bloodweb_json["bloodwebdata"] = {"paths": [], "ringData": [{"nodeData": [{"nodeId": 0, "state": "Collected"}]}]}
        
        flow.response = http.Response.make(
            200,  
            json.dumps(bloodweb_json),  
            {"Content-Type": "application/json"}  
        )
        Misc.print_log("Bloodweb successfully loaded")
    except Exception as e:
        Misc.print_log("Error processing Bloodweb")
        Misc.print_log(str(e))
