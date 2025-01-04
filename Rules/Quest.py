import os
import json
from mitmproxy import http
import httpx
from Utils import Misc

quest_filename = "Quest.json"
headers_filename = "Headers.json"
url_request = "api/v1/gameDataAnalytics/v2/batch"
url_response = "api/v1/archives/stories/update/active-node-v3"
status = True

async def request(flow: http.HTTPFlow):
    try:
        flow.request.decode()
        request_json = json.loads(flow.request.get_text())

        match_id, kraken_match_id = None, None
        for event in request_json.get("events", []):
            if event["eventType"] in ["postgame_survivor", "postgame_killer"]:
                match_id = event["data"].get("match_id")
                kraken_match_id = event["data"].get("kraken_match_id")
                break

        if not match_id or not kraken_match_id:
            return

        quest_path = os.path.join(Misc.market_updater_path, quest_filename)
        headers_path = os.path.join(Misc.market_updater_path, headers_filename)

        if not os.path.exists(quest_path) or not os.path.exists(headers_path):
            return
        
        with open(headers_path, "r") as header_file:
            headers_json = json.load(header_file)

        with open(quest_path, "r") as quest_file:
            quest_json = json.load(quest_file)

        quest_json["matchId"] = match_id
        quest_json["krakenMatchId"] = kraken_match_id

        request_body = json.dumps(quest_json)
        
        headers = {header["name"]: header["value"] for header in headers_json}

        base_url = None
        for header in headers_json:
            if header["name"] == "Host":
                base_url = "https://" + header["value"]
                break

        if base_url is None:
            raise ValueError("Host header not found")

        url = base_url + "/api/v1/archives/stories/update/quest-progress-v3"
        
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.post(url, headers=headers, data=request_body)

        if response.status_code == 200:
            Misc.print_log("Quest successfully unlocked")
        else:
            Misc.print_log("Error unlocking quest")
    except Exception as e:
        Misc.print_log(f"Error processing request: {str(e)}")

def response(flow: http.HTTPFlow):
    try:
        flow.response.decode()
        response_json = json.loads(flow.response.get_text())

        if not response_json.get("activeNodesFull"):
            quest_path = os.path.join(Misc.market_updater_path, quest_filename)
            if os.path.exists(quest_path):
                os.remove(quest_path)
            return

        role = flow.request.json().get("role", "survivor")
        if role == "both":
            role = "survivor"

        active_nodes = response_json["activeNodesFull"][0]["objectives"]
        needed_progression = active_nodes[0]["neededProgression"]
        quest_events = active_nodes[0]["questEvent"]

        request_body = {"questEvents": [], "role": role}
        for quest_event in quest_events:
            repetition = quest_event["repetition"] * needed_progression
            if quest_event["operation"] == "<":
                repetition -= 1
            elif quest_event["operation"] == ">":
                repetition += 1

            quest_event_data = {
                "questEventId": quest_event["questEventId"],
                "repetition": repetition
            }
            if "parameters" in quest_event:
                quest_event_data["parameters"] = quest_event["parameters"]
            request_body["questEvents"].append(quest_event_data)

        quest_path = os.path.join(Misc.market_updater_path, quest_filename)
        with open(quest_path, "w") as quest_file:
            json.dump(request_body, quest_file)

        Misc.print_log("Quest successfully loaded")

    except Exception as e:
        Misc.print_log(f"Error processing response: {str(e)}")
