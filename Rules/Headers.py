import json
import os
from Utils import Misc

url = "api/v1/auth/v2/publicKey"
filename = "Headers.json"
status = True
Misc.load_settings()

def request(flow):
    try:
        headers = []
        for header in flow.request.headers.items():
            if len(header) == 2 and "Content-Length" not in header[0]:
                headers.append({"name":str(header[0]), "value":str(header[1])})
        with open(os.path.join(Misc.market_updater_path, filename), "w") as headers_file:
            json.dump(headers, headers_file)
        Misc.print_log("Headers successfully updated")
    except Exception as e:
        print(e)