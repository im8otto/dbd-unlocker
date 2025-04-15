import json
import os
from Utils import Misc

url = "/api/v1/dbd-inventories/all"
filename = "MarketNoSavefile.json"
status = True

def response(flow):
    try:
        market_path = os.path.join(Misc.market_updater_path, "Files", filename)
        if not os.path.exists(market_path):
            Misc.print_log("ERROR: ", market_path, "doesn't exist.")
            return
            
        with open(market_path, "r") as market_file:
            market_json = Misc.normalize_keys(json.load(market_file))
            
        if len(market_json["data"]["inventory"]) > 0:
            items = market_json["data"]["inventory"]
        else:
            items = market_json["inventoryitems"]
            
        flow.response.decode()
        response_json = Misc.normalize_keys(json.loads(flow.response.get_text()))
        
        response_json["inventoryitems"].extend(items)
        
        flow.response.text = json.dumps(response_json)
        Misc.print_log("Market successfully loaded")
    except Exception as e:
        Misc.print_log("Error loading Market")
        Misc.print_log(e)
