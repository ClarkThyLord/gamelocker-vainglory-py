"""

    Fetch Players -

        Small program that retrieves multiple players data by there ign.

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

igns = input("In-game Names: (separate with , Example: ClarkthyLord,AmethystCrow,jeovanne)")

while True:
    region = str(input("In-game Region:" + regions_string)).lower()

    if region == "":
        region = "na"
        break

    elif region in regions:
        break

    else:
        print(str(region) + " isn't a valid region!")

# Args to fetch data with
args = {'filter[playerNames]': igns}

print("\n")

players = api.players(args, region)

if "error" in players:
    print("Something went wrong!")
    if api.debugging == False:
        print(players)

    exit()

print("Data Info -\nPlayers: " + str(len(players)))

ans = str(input("Print match? (y/n)")).lower()
if ans == "y":
    for player in players:
        print(player)

# TODO process players data here

print("!!!DONE!!!")
