"""

    List Events -

        Small program used to list all events in a match and give examples to those events.

"""

import datetime
import json
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

ign = input("In-game Name:")
repeat = True
while repeat == True:
    region = str(input("In-game Region:" + regions_string)).lower()

    if region == "":
        region = "na"
        repeat = False

    elif region in regions:
        repeat = False

    else:
        print(str(region) + " isn't a valid region!")
repeat = True
while repeat == True:
    game_mode = str(input("Game Mode:" + game_modes_string)).lower()

    if game_mode == "" or game_mode == "any":
        game_mode = False
        repeat = False

    elif game_mode in game_modes:
        game_mode = game_modes[game_mode]
        repeat = False

    else:
        print(str(game_mode) + " isn't a valid game mode!")

# Args to fetch data with
args = {'filter[createdAt-start]': str(datetime.date.today() - datetime.timedelta(days=28)) + "T00:00:00Z", 'page[limit]': 50, 'filter[playerNames]': ign, "sort": "-createdAt"}

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


def process(match):
    try:

        url = match["telemetry"]["URL"]

        print("Telemetry URL:\n" + str(url))

        telemetry = api.telemetry(url)

        print("Telemetry Info -\nEvents: " + str(len(telemetry)))

        print("\n")

        # Variables
        hickups = 0
        eventTypes = {}

        for event in telemetry:
            try:

                if event["type"] not in eventTypes:
                    eventTypes[event["type"]] = event

            except Exception as e:
                print("hick-up!\n" + str(e))

        print("\n")

        print("Process Info:\nHick Ups: " + str(hickups))

        print("\n")

        for eventType in eventTypes:
            print("Event Type: " + str(eventType) + "\nExample:\n" + str(eventTypes[eventType]) + "\n")

        ans = input("Save to json as result.json in working directory? (y/n)")
        if ans == "y":
            with open("result.json", "w") as handler:
                json.dump(eventTypes, handler)

            print("Saved!")

        else:
            print("Not saved!")

        print("\n")

    except Exception as e:
        print("An error has occurred while processing match telemetry!\n" + str(e))


def processAll(data):
    try:

        # Variables
        hickups = 0
        eventTypes = {}

        for match in data:

            try:

                url = match["telemetry"]["URL"]

                print("Telemetry URL:\n" + str(url))

                telemetry = api.telemetry(url)

                print("Telemetry Info -\nEvents: " + str(len(telemetry)))

                print("\n")

                for event in telemetry:
                    try:

                        if event["type"] not in eventTypes:
                            eventTypes[event["type"]] = event

                    except Exception as e:
                        print("hick-up!\n" + str(e))

            except Exception as e:
                print("An error has occurred while processing a match!\n" + str(e))

        print("\n")

        print("Process Info:\nHick Ups: " + str(hickups))

        print("\n")

        for eventType in eventTypes:
            print("Event Type: " + str(eventType) + "\nExample:\n" + str(eventTypes[eventType]) + "\n")

        ans = input("Save to json as result.json in working directory? (y/n)")
        if ans == "y":
            with open("result.json", "w") as handler:
                json.dump(eventTypes, handler)

            print("Saved!")

        else:
            print("Not saved!")

        print("\n")

    except Exception as e:
        print("An error has occurred while processing match telemetry!\n" + str(e))

# Variables
current = 0

repeat = True
while repeat == True:
    ans = input("On " + str(current + 1) + ", a " + str(data[current]["gameMode"]) + " match, of " + str(len(data)) + " matches; what would you like to do?\n~ next - back - process - processAll - exit ~")

    if ans == "next":
        if (current + 1) == len(data):
            current = 0

        else:
            current += 1

    elif ans == "back":
        if current == 0:
            current = (len(data) - 1)

        else:
            current -= 1

    elif ans == "process":
        process(data[current])

    elif ans == "processAll":
        ans = input("Processing all the matches may take a while, continue? (y/n)")
        if ans == "y":
            processAll(data)

        else:
            print("Cancelling...\n")

    elif ans == "exit":
        print("bye")
        exit()

    else:
        print(str(ans) + " isn't a command!")
