"""

    Fetch Matches -

        Small program that retrieves matches by filters, args.

"""

import datetime
from gamelocker import wrapper

api_key = "API_KEY_HERE"   # VG API Key

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

amount = input("Amount of matches?")
if amount > 50:
    amount = 50
    print("50 matches is the maximum amount you can call for!")

elif amount < 1:
    amount = 1
    print("Going to be calling on one match!")

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
args = {'filter[createdAt-start]': str(datetime.date.today() - datetime.timedelta(days=28)) + "T00:00:00Z", 'page[limit]': amount, 'filter[playerNames]': ign, "sort": "-createdAt"}

if game_mode != False:
    args["filter[gameMode]"] = game_mode

print("ARGS USED:\n" + str(args))

print("\n")

matches = api.matches(args, region)

if "error" in matches:
    print("Something went wrong!")
    if api.debugging == False:
        print(matches)

    exit()

print("Data Info -\nMatches: " + str(len(matches)))

ans = str(input("Print matches? (y/n)")).lower()
if ans == "y":
    for match in matches:
        print(match)

# TODO process matches data here

print("!!!DONE!!!")
