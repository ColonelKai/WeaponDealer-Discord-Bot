import time
import json

while True:
    time.sleep(900)
    with open("playerdata.json", "r") as file:
        userdata = json.load(file)

    for i in userdata.keys():
        if userdata[i]["data"]["RP"] < 100:
            userdata[i]["data"]["RP"] += 5
        else:
            pass

    with open("playerdata.json", "w") as file:
        json.dump(userdata, file)