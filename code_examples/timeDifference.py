"""

    Time Diffrence -

        Small program used to fetch matches data from api and tell when was the latest match in minutes.

"""

import datetime
from gamelocker import wrapper

api_key = "API_KEY_HERE"  # VG API Key

api = wrapper.Vainglory(api_key)

# Vainglory game modes
game_modes = {"casual": "casual", "ranked": "ranked", "royale": "casual_aral", "blitz": "blitz_pvp_ranked"}
game_modes_string = " - any - "
for key in game_modes:
    game_modes_string += str(key) + " - "

# Vainglory regions
regions = ["na", "eu", "se", "sa", "sg"]
regions_string = " - "
for key in regions:
    regions_string += str(key) + " - "

ans = str(input("Debug Mode?(y/n)")).lower()
if ans == "y":
    api.debugging = True

ign = input("In-game Name:")

while True:
    region = str(input("In-game Region:" + regions_string)).lower()

    if region == "":
        region = "na"
        break

    elif region in regions:
        break

    else:
        print(str(region) + " isn't a valid region!")

while True:
    game_mode = str(input("Game Mode:" + game_modes_string)).lower()

    if game_mode == "" or game_mode == "any":
        game_mode = False
        break

    elif game_mode in game_modes:
        game_mode = game_modes[game_mode]
        break

    else:
        print(str(game_mode) + " isn't a valid game mode!")

# Args to fetch data with
args = {'filter[createdAt-start]': str(datetime.date.today() - datetime.timedelta(days=28)) + "T00:00:00Z", 'page[limit]': 1, 'filter[playerNames]': ign, "sort": "-createdAt"}

if game_mode != False:
    args["filter[gameMode]"] = game_mode

print("ARGS USED:\n" + str(args))

print("\n")

data = api.matches(args, region)

if "error" in data:
    print("Something went wrong!")
    if api.debugging == False:
        print(data)

    exit()

print("Data Info -\nMatches: " + str(len(data)))

print("\n")

# TODO handle data here

print("Raw Time Stamp: " + str(data[0]["createdAt"]))
latest = datetime.datetime.strptime(str(data[0]["createdAt"]).replace("Z", ""), "%Y-%m-%dT%H:%M:%S")
print("Latest: " + str(latest))

now = datetime.datetime.now()
print("Now: " + str(now))

difference = (now - latest).seconds / 60
print("Difference: " + str(round(difference, 2)) + " min.")


print("\n")

print("!!!DONE!!!")
