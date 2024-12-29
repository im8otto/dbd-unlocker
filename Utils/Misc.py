from datetime import datetime
import platform
import os
import json
import requests

current_system = platform.system()
if current_system == "Windows": 
    market_updater_path = "C:\\Rules"
else:
    market_updater_path = os.path.expanduser("~/Applications/dbd-unlocker")
settings_json = {"market_updater_path": market_updater_path, "banner": True, "bloodweb": True, "getall": True, "market": True, "quest": True}
script_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
settings_filename = os.path.join(script_dir, "8otto_settings.json")
first_load = True

def print_logo():
    os.system("cls")
    logo = r'''
      _____   _      _____    _    _         _               _               
     |  __ \ | |    |  __ \  | |  | |       | |             | |              
     | |  | || |__  | |  | | | |  | | _ __  | |  ___    ___ | | __ ___  _ __ 
     | |  | || '_ \ | |  | | | |  | || '_ \ | | / _ \  / __|| |/ // _ \| '__|
     | |__| || |_) || |__| | | |__| || | | || || (_) || (__ |   <|  __/| |   
     |_____/ |_.__/ |_____/   \____/ |_| |_||_| \___/  \___||_|\_\\___||_|   
                     _               ___          _    _                     
                    | |             / _ \        | |  | |                    
                    | |__   _   _  | (_) |  ___  | |_ | |_  ___              
                    | '_ \ | | | |  > _ <  / _ \ | __|| __|/ _ \             
                    | |_) || |_| | | (_) || (_) || |_ | |_| (_) |            
                    |_.__/  \__, |  \___/  \___/  \__| \__|\___/             
                             __/ |                                           
                            |___/                                
    '''
    print(logo)
    print("\nTo close press CTRL + F4 from keyboard or SELECT+START from controller\nIf you exit in other ways, you have to unset proxy MANUALLY from your PC settings")
    return
    
def print_log(text):
    print(datetime.now().strftime("[%H:%M:%S]:"), text)

def normalize_keys(d):
    if isinstance(d, dict):
        return {k.lower(): normalize_keys(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [normalize_keys(item) for item in d]
    else:
        return d

def load_settings():
    from Rules import Market, Banner, Bloodweb, Headers, GetAll, Quest
    global settings_json, settings_filename, first_load
    if not os.path.exists(settings_filename):
        with open(settings_filename, "w") as file:
            json.dump(settings_json, file, indent=4)
        check_folder()
        return
    with open(settings_filename) as file:
        settings_json = normalize_keys(json.load(file))
    market_updater_path = settings_json["market_updater_path"]
    check_folder()
    Banner.status = settings_json["banner"]
    Bloodweb.status = settings_json["bloodweb"]
    GetAll.status = settings_json["getall"]
    Headers.status = settings_json["quest"]
    Market.status = settings_json["market"]
    Quest.status = settings_json["quest"]
    if first_load:
        print_log(f'Settings successfully loaded\nPath: {market_updater_path}, Banner: {Banner.status}, Bloodweb: {Bloodweb.status}, GetAll: {GetAll.status}, Headers: {Headers.status}, Market: {Market.status}, Quest: {Quest.status}')
        first_load = False
    
def check_folder():
    from Rules import Market, Bloodweb, GetAll
    if not os.path.exists(os.path.join(market_updater_path, "Files")):
        os.makedirs(os.path.join(market_updater_path, "Files"), exist_ok=True)
        with open(os.path.join(market_updater_path, "Files", Market.filename), "wb") as file:
            file.write(requests.get('https://raw.githubusercontent.com/im8otto/Melancholy/refs/heads/main/Rules/Files/MarketNoSavefile.json').content)
        with open(os.path.join(market_updater_path, "Files", Bloodweb.filename), "wb") as file:
            file.write(requests.get('https://raw.githubusercontent.com/im8otto/Melancholy/refs/heads/main/Rules/Files/Bloodweb.json').content)
        with open(os.path.join(market_updater_path, "Files", GetAll.filename), "wb") as file:
            file.write(requests.get('https://raw.githubusercontent.com/im8otto/Melancholy/refs/heads/main/Rules/Files/GetAll.json').content)
        print_log(f"Successfully created {market_updater_path} path and downloaded latest pregenerated Market files.")