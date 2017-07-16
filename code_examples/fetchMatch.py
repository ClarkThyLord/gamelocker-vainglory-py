"""

    Fetch Match -

        Small program which retrieves a match by it's id.

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

matchId = input("Matches ID:")

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

match = api.match(matchId, region)

if "error" in match:
    print("Something went wrong!")
    if api.debugging == False:
        print(match)

    exit()

ans = str(input("Print match? (y/n)")).lower()
if ans == "y":
    print(match)

# TODO process match data here

print("!!!DONE!!!")
