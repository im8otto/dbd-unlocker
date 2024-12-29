import os
from Utils import Misc

url = "api/v1/dbd-player-card"
filename = "Banner.json"
status = True
Misc.load_settings()

def response(flow):
    global filename
    banner_path = os.path.join(Misc.market_updater_path, filename)
    
    if "api/v1/dbd-player-card/set" in flow.request.path:
        try:
            flow.request.decode()
            request_body = flow.request.get_text()
            flow.response.status_code = 200
            flow.response.text = request_body
            with open(banner_path, "w") as file:
                file.write(request_body)
        except Exception as e:
            print(e)

    if "api/v1/dbd-player-card/get" in flow.request.path:
        try:
            if not os.path.exists(banner_path):
                return
            with open(banner_path, "r") as file:
                response_body = file.read()
            flow.response.status_code = 200
            flow.response.text = response_body
        except Exception as e:
            print(e)