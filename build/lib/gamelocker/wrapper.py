"""This is where all the magic happens.

Reference:
https://developer.vainglorygame.com/docs
http://docs.python-requests.org/en/master/

"""

import logging  # To long events
import requests  # To call on services

class Vainglory(object):

    def __init__(self, key, dataCenter="dc01"):
        """At creation of this object setup variables.

        :argument key: API key used to access data | Get your own VG API key at https://developer.vainglorygame.com/
        :argument dataCenter: The data center that object should connect to; Default: dc01, Options: dc01

        """

        self.key = key
        self.dataCenter = dataCenter

    def _req(self, endpoint, args):
        """Request the data from Vainglory.

        :argument args: argss used to fetch appropriate data.
        :argument endpoint: Where do you wanna call this data from.
        :returns: JSONs, in a list, with what you've requested.

        """

        try:

            headers = {
                "Authorization": self.key,
                "X-TITLE-ID": "semc-vainglory",
                "Accept": "application/vnd.api+json"
            }

            while True:
                http = requests.get(

                    "https://api." + self.dataCenter + ".gamelockerapp.com/" + endpoint,
                    headers=headers,
                    params=args

                )

                if http.status_code != 200:
                    logging.info("<!--\nVainglory API Error\n" + str(http.status_code) + "\n--!>")
                    return None

                else:
                    break

            return http.json()

        except Exception as e:
            print("ERROR:   " + str(e))

    def _getMatch(self, region="na", endpoint="matches", elementID=""):
        """Get data from api.

        :argument region: Region from which to pull data from.
        :argument endpoint: What type of data you would like to pull.
        :argument elementID: ID of element you are specifying for.
        :returns: Dictionary with requested data; None if error occurred!

        """

        original = self._req("shards/" + str(region) + "/" + str(endpoint) + "/" + str(elementID), None)

        data = [original["data"]]
        included = original["included"]

        Match = []
        for part in data:
            Match.append(
                {
                    "id": part["id"],
                    "type": part["type"],
                    "gameMode": part["attributes"]["gameMode"],
                    "endGameReason": part["attributes"]["stats"]["endGameReason"],
                    "createdAt": part["attributes"]["createdAt"],
                    "duration": part["attributes"]["duration"],
                    "rosters": [
                        part["relationships"]["rosters"]["data"][0]["id"],
                        part["relationships"]["rosters"]["data"][1]["id"]
                    ],
                    "telemetry": part["relationships"]["assets"]["data"][0]["id"]
                }
            )

        rosters = {}
        participants = {}
        players = {}
        assets = {}
        for part in included:
            if part["type"] == "roster":
                rosters[str(part["id"])] = {

                    "side": part["attributes"]["stats"]["side"],
                    "heroKills": part["attributes"]["stats"]["heroKills"],
                    "gold": part["attributes"]["stats"]["gold"],
                    "acesEarned": part["attributes"]["stats"]["acesEarned"],
                    "turretKills": part["attributes"]["stats"]["turretKills"],
                    "turretsRemaining": part["attributes"]["stats"]["turretsRemaining"],
                    "krakenCaptures": part["attributes"]["stats"]["krakenCaptures"],
                    "participants": []

                }
                for participant in part["relationships"]["participants"]["data"]:
                    rosters[str(part["id"])]["participants"].append(participant["id"])

            elif part["type"] == "participant":
                participants[str(part["id"])] = {

                    "actor": part["attributes"]["actor"],
                    "kills": part["attributes"]["stats"]["kills"],
                    "jungleKills": part["attributes"]["stats"]["jungleKills"],
                    "assists": part["attributes"]["stats"]["assists"],
                    "deaths": part["attributes"]["stats"]["deaths"],
                    "farm": part["attributes"]["stats"]["farm"],
                    "gold": part["attributes"]["stats"]["gold"],
                    "turretCaptures": part["attributes"]["stats"]["turretCaptures"],
                    "crystalMineCaptures": part["attributes"]["stats"]["crystalMineCaptures"],
                    "goldMineCaptures": part["attributes"]["stats"]["goldMineCaptures"],
                    "krakenCaptures": part["attributes"]["stats"]["krakenCaptures"],
                    "minionKills": part["attributes"]["stats"]["minionKills"],
                    "nonJungleMinionKills": part["attributes"]["stats"]["nonJungleMinionKills"],
                    "level": part["attributes"]["stats"]["level"],
                    "skillTier": part["attributes"]["stats"]["skillTier"],
                    "karmaLevel": part["attributes"]["stats"]["karmaLevel"],
                    "wentAfk": part["attributes"]["stats"]["wentAfk"],
                    "firstAfkTime": part["attributes"]["stats"]["firstAfkTime"],
                    "winner": part["attributes"]["stats"]["winner"],
                    "skinKey": part["attributes"]["stats"]["skinKey"],
                    "items": part["attributes"]["stats"]["items"],
                    "itemGrants": part["attributes"]["stats"]["itemGrants"],
                    "itemSells": part["attributes"]["stats"]["itemSells"],
                    "itemUses": part["attributes"]["stats"]["itemUses"],
                    "player": str(part["relationships"]["player"]["data"]["id"])

                }

            elif part["type"] == "player":
                players[str(part["id"])] = {

                    "name": part["attributes"]["name"],
                    "level": part["attributes"]["stats"]["level"],
                    "xp": part["attributes"]["stats"]["xp"],
                    "lifetimeGold": part["attributes"]["stats"]["lifetimeGold"],
                    "played": part["attributes"]["stats"]["played"],
                    "played_ranked": part["attributes"]["stats"]["played_ranked"],
                    "wins": part["attributes"]["stats"]["wins"],
                    "winStreak": part["attributes"]["stats"]["winStreak"],
                    "lossStreak": part["attributes"]["stats"]["lossStreak"]

                }

            elif part["type"] == "asset":
                assets[str(part["id"])] = {

                    "name": part["attributes"]["name"],
                    "createdAt": part["attributes"]["createdAt"],
                    "contentType": part["attributes"]["contentType"],
                    "URL": part["attributes"]["URL"]

                }

                pass

            else:
                print(part)

        for r in Match:
            full = []
            for ro in r["rosters"]:
                ros = rosters[ro]
                par = []
                for p in ros["participants"]:
                    part = participants[p]

                    player_id = part["player"]

                    part["player"] = players[player_id]

                    par.append(part)

                ros["participants"] = par

                full.append(ros)

            r["rosters"] = full
            
        return Match

    def _getMatches(self, region="na", endpoint="matches", args=None):
        """Get data from api.

        :argument region: Region from which to pull data from.
        :argument endpoint: What type of data you would like to pull.
        :argument args: Parameters, args, used to args data with.
        :returns: List of dictionaries with requested data; None if error occurred!

        """

        original = self._req("shards/" + str(region) + "/" + str(endpoint) + "/", args)

        data = [original["data"]]
        included = original["included"]

        Matches = []
        for cluster in data:
            for part in cluster:
                Matches.append(
                    {
                        "id": part["id"],
                        "type": part["type"],
                        "gameMode": part["attributes"]["gameMode"],
                        "endGameReason": part["attributes"]["stats"]["endGameReason"],
                        "createdAt": part["attributes"]["createdAt"],
                        "duration": part["attributes"]["duration"],
                        "rosters": [
                            part["relationships"]["rosters"]["data"][0]["id"],
                            part["relationships"]["rosters"]["data"][1]["id"]
                        ],
                        "telemetry": part["relationships"]["assets"]["data"][0]["id"]
                    }
                )

        rosters = {}
        participants = {}
        players = {}
        assets = {}
        for part in included:
            if part["type"] == "roster":
                rosters[str(part["id"])] = {

                    "side": part["attributes"]["stats"]["side"],
                    "heroKills": part["attributes"]["stats"]["heroKills"],
                    "gold": part["attributes"]["stats"]["gold"],
                    "acesEarned": part["attributes"]["stats"]["acesEarned"],
                    "turretKills": part["attributes"]["stats"]["turretKills"],
                    "turretsRemaining": part["attributes"]["stats"]["turretsRemaining"],
                    "krakenCaptures": part["attributes"]["stats"]["krakenCaptures"],
                    "participants": []

                }
                for participant in part["relationships"]["participants"]["data"]:
                    rosters[str(part["id"])]["participants"].append(participant["id"])

            elif part["type"] == "participant":
                participants[str(part["id"])] = {

                    "actor": part["attributes"]["actor"],
                    "kills": part["attributes"]["stats"]["kills"],
                    "jungleKills": part["attributes"]["stats"]["jungleKills"],
                    "assists": part["attributes"]["stats"]["assists"],
                    "deaths": part["attributes"]["stats"]["deaths"],
                    "farm": part["attributes"]["stats"]["farm"],
                    "gold": part["attributes"]["stats"]["gold"],
                    "turretCaptures": part["attributes"]["stats"]["turretCaptures"],
                    "crystalMineCaptures": part["attributes"]["stats"]["crystalMineCaptures"],
                    "goldMineCaptures": part["attributes"]["stats"]["goldMineCaptures"],
                    "krakenCaptures": part["attributes"]["stats"]["krakenCaptures"],
                    "minionKills": part["attributes"]["stats"]["minionKills"],
                    "nonJungleMinionKills": part["attributes"]["stats"]["nonJungleMinionKills"],
                    "level": part["attributes"]["stats"]["level"],
                    "skillTier": part["attributes"]["stats"]["skillTier"],
                    "karmaLevel": part["attributes"]["stats"]["karmaLevel"],
                    "wentAfk": part["attributes"]["stats"]["wentAfk"],
                    "firstAfkTime": part["attributes"]["stats"]["firstAfkTime"],
                    "winner": part["attributes"]["stats"]["winner"],
                    "skinKey": part["attributes"]["stats"]["skinKey"],
                    "items": part["attributes"]["stats"]["items"],
                    "itemGrants": part["attributes"]["stats"]["itemGrants"],
                    "itemSells": part["attributes"]["stats"]["itemSells"],
                    "itemUses": part["attributes"]["stats"]["itemUses"],
                    "player": str(part["relationships"]["player"]["data"]["id"])

                }

            elif part["type"] == "player":
                players[str(part["id"])] = {

                    "name": part["attributes"]["name"],
                    "level": part["attributes"]["stats"]["level"],
                    "xp": part["attributes"]["stats"]["xp"],
                    "lifetimeGold": part["attributes"]["stats"]["lifetimeGold"],
                    "played": part["attributes"]["stats"]["played"],
                    "played_ranked": part["attributes"]["stats"]["played_ranked"],
                    "wins": part["attributes"]["stats"]["wins"],
                    "winStreak": part["attributes"]["stats"]["winStreak"],
                    "lossStreak": part["attributes"]["stats"]["lossStreak"]

                }

            elif part["type"] == "asset":
                assets[str(part["id"])] = {

                    "name": part["attributes"]["name"],
                    "createdAt": part["attributes"]["createdAt"],
                    "contentType": part["attributes"]["contentType"],
                    "URL": part["attributes"]["URL"]

                }

                pass

            else:
                print(part)

        for r in Matches:
            full = []
            for ro in r["rosters"]:
                ros = rosters[ro]
                par = []
                for p in ros["participants"]:
                    part = participants[p]

                    player_id = part["player"]

                    part["player"] = players[player_id]

                    par.append(part)

                ros["participants"] = par

                full.append(ros)
                # del rosters[ro]

            r["rosters"] = full

        return Matches

    def _getPlayer(self, region="na", endpoint="matches", elementID=""):
        """Get data from api.

        :argument region: Region from which to pull data from.
        :argument endpoint: What type of data you would like to pull.
        :argument elementID: ID of element you are specifying for.
        :returns: Dictionary with requested data; None if error occurred!

        """

        original = self._req("shards/" + str(region) + "/" + str(endpoint) + "/" + str(elementID), None)

        data = original["data"]

        player = {
            "id": data["id"],
            "createdAt": data["attributes"]["createdAt"],
            "name": data["attributes"]["name"],
            "shardId": data["attributes"]["shardId"],
            "level": data["attributes"]["stats"]["level"],
            "lifetimeGold": data["attributes"]["stats"]["lifetimeGold"],
            "lossStreak": data["attributes"]["stats"]["lossStreak"],
            "played": data["attributes"]["stats"]["played"],
            "played_ranked": data["attributes"]["stats"]["played_ranked"],
            "winStreak": data["attributes"]["stats"]["winStreak"],
            "wins": data["attributes"]["stats"]["wins"],
            "xp": data["attributes"]["stats"]["xp"],
        }

        return player

    def _getPlayers(self, region="na", endpoint="matches", args=None):
        """Get data from api.

        :argument region: Region from which to pull data from.
        :argument endpoint: What type of data you would like to pull.
        :argument args: Parameters, args, used to args data with.
        :returns: List with requested data; None if error occurred!

        """

        original =  self._req("shards/" + str(region) + "/" + str(endpoint) + "/", args)

        data = original["data"]

        players = []
        for part in data:

            players.append(
                {
                    "id": part["id"],
                    "createdAt": part["attributes"]["createdAt"],
                    "name": part["attributes"]["name"],
                    "shardId": part["attributes"]["shardId"],
                    "level": part["attributes"]["stats"]["level"],
                    "lifetimeGold": part["attributes"]["stats"]["lifetimeGold"],
                    "lossStreak": part["attributes"]["stats"]["lossStreak"],
                    "played": part["attributes"]["stats"]["played"],
                    "played_ranked": part["attributes"]["stats"]["played_ranked"],
                    "winStreak": part["attributes"]["stats"]["winStreak"],
                    "wins": part["attributes"]["stats"]["wins"],
                    "xp": part["attributes"]["stats"]["xp"],
                }
            )

        return players

    def _getSamples(self, region="na", endpoint="samples", args=None):
        """Get data from api.

        :argument region: Region from which to pull data from.
        :argument endpoint: What type of data you would like to pull.
        :argument args: Parameters, args, used to args data with.
        :returns: List of/A dictionary(s) with requested data; None if error occurred!

        """

        return self._req("shards/" + str(region) + "/" + str(endpoint) + "/", args)

    def dict_to_object(self, dictionary):
        """Convert a dictionary to a object.

        :argument dictionary: Dictionary that will be converted to an object.
        :returns: Object of dictionary.

        """

        return DictObject(dictionary)


    def player(self, playerID, region="na", toObject=False):
        """Used to fetch a player.

        :parameter playerID: ID of player to retrieve; Reference: https://developer.vainglorygame.com/docs#get-a-single-player
        :parameter region: Region from which to fetch data; Default: na, Options: na, eu, sg , ea, sa
        :parameter toObject: Weather or not dictionary should be turned into object.
        :return:  Dictionary/Object with requested data; None if error occurred!

        """

        original = self._getPlayer(region, "players", playerID)

        if toObject == True:
            data = []
            for cluster in original:
                data.append(self.dict_to_object(cluster))

            return data

        return original

    def players(self, args, region="na", toObject=False):
        """Used to fetch multiple players.

        :parameter args: What to filter with in a dictionary; Reference: https://developer.vainglorygame.com/docs#get-a-collection-of-players
        :parameter region: Region from which to fetch data; Default: na, Options: na, eu, sg , ea, sa
        :parameter toObject: Weather or not dictionary should be turned into object.
        :returns:  List of dictionaries/objects with requested data; None if error occurred!

        """

        original = self._getPlayers(region, "players", args=args)

        if toObject == True:
            data = []
            for cluster in original:
                data.append(self.dict_to_object(cluster))

            return data

        return original

    def samples(self, args, region="na"):
        """Used to fetch samples.

        :parameter args: What to filter with in a dictionary; Reference in a dictionary: https://developer.vainglorygame.com/docs#samples
        :parameter region: Region from which to fetch data; Default: na, Options: na, eu, sg , ea, sa
        :returns: List of dictionaries with requested data; None if error occurred!

        """

        return self._getSamples(region, "samples", args=args)

    def match(self, matchID, region="na", toObject=False):
        """Used to fetch a specific match.

        :parameter matchID: ID of match to retrieve; Reference: https://developer.vainglorygame.com/docs#get-a-single-match
        :parameter region: Region from which to fetch data; Default: na, Options: na, eu, sg , ea, sa
        :parameter toObject: Weather or not dictionary should be turned into object.
        :return: Dictionaries/Object with requested data; None if error occurred!

        """

        original = self._getMatch(region, "matches", matchID)

        if toObject == True:
            data = []
            for cluster in original:
                data.append(self.dict_to_object(cluster))

            return data

        return original

    def matches(self, args, region="na", toObject=False):
        """Used to fetch multiple matches.

        :parameter args: What to filter with in a dictionary; Reference: https://developer.vainglorygame.com/docs#get-a-collection-of-matches
        :parameter region: Region from which to fetch data; Default: na, Options: na, eu, sg , ea, sa
        :parameter toObject: Weather or not dictionary should be turned into object.
        :return: List of dictionaries/objects with requested data; None if error occurred!

        """

        original = self._getMatches(region, "matches", args=args)

        if toObject == True:
            data = []
            for cluster in original:
                data.append(self.dict_to_object(cluster))

            return data

        return original

    def telemetry(self, url):
        """Used to fetch telemetry JSON.

        :argument url: Link to telemetry; Reference: https://developer.vainglorygame.com/docs#to-get-telemetry-data
        :returns: Dictionary with telemetry data.

        """

        return (requests.get(url)).json()


class DictObject(object):
    def __init__(self, dictionary):
        """Set up variables at creating of object.

        :argument dictionary: Dictionary to convert to object
        :returns: Object of dictionary

        """

        # Get everything from the dictionary and place it into the object
        self.__dict__.update(dictionary)

        # So that dictionaries function correctly in the object as well
        for key, value in dictionary.items():
            if isinstance(value, dict):
                self.__dict__[key] = DictObject(value)
