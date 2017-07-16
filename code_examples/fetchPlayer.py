"""

    Time Diffrence -

        Small program used to fetch matches data from api and tell when was the latest match in minutes.

"""

from gamelocker import wrapper

api_key = "API_KEY_HERE"   # VG API Key

api = wrapper.Vainglory(api_key)

# Vainglory regions
regions = ["na", "eu", "se", "sa", "sg"]
regions_string = " - "
for key in regions:
    regions_string += str(key) + " - "

ans = str(input("Debug Mode?(y/n)")).lower()
if ans == "y":
    api.debugging = True

playerId = input("Player ID:")

while True:
    region = str(input("In-game Region:" + regions_string)).lower()

    if region == "":
        region = "na"
        break

    elif region in regions:
        break

    else:
        print(str(region) + " isn't a valid region!")

print("\n")

player = api.player(playerId, region)

if "error" in player:
    print("Something went wrong!")
    if api.debugging == False:
        print(player)

    exit()

ans = str(input("Print match? (y/n)")).lower()
if ans == "y":
    print(player)

# TODO process player data here

print("!!!DONE!!!")
