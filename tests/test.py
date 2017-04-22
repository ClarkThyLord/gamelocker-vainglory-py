import gamelocker

VaingloryAPIKey = "<!-- API-KEY-HERE --!>"  # Key to access vainglory api | Get yours here, https://developer.vainglorygame.com/
DataCenter = "dc01"  # Data center from which to fetch data | Reference: https://developer.vainglorygame.com/docs#datacenters
vgApi = gamelocker.Vainglory(VaingloryAPIKey, DataCenter)  # Create a object of wrapper


def testPlayer():
    """Assert that the player part of the wrapper is working."""

    # Reference: https://developer.vainglorygame.com/docs#get-a-single-player
    player_id = "99b050b8-cd6b-11e5-b233-06eb725f8a76"

    # Reference: https://developer.vainglorygame.com/docs#regions
    region = "na"

    assert vgApi.player(player_id, region)


def testPlayers():
    """Assert that the players part of the wrapper is working."""

    # Reference: https://developer.vainglorygame.com/docs#get-a-collection-of-players
    args = {

        'filter[playerNames]': 'ClarkthyLord,AmethystCrow'

    }

    # Reference: https://developer.vainglorygame.com/docs#regions
    region = "na"

    assert vgApi.players(args, region)


def testMatch():
    """Assert that the match part of the wrapper is working."""

    # Reference: https://developer.vainglorygame.com/docs#get-a-single-match
    match_id = "ceff1d8c-226d-11e7-870a-062445d3d668"

    # Reference: https://developer.vainglorygame.com/docs#regions
    region = "na"

    assert vgApi.match(match_id, region)


def testMatches():
    """Assert that the matches part of the wrapper is working."""

    # Reference: https://developer.vainglorygame.com/docs#get-a-collection-of-matches
    args = {

        'filter[createdAt-start]': '2017-04-00T00:00:00Z',
        'sort': '-createdAt',
        'page[limit]': '50',
        'filter[playerNames]': 'ClarkThyLord',
        'filter[gameMode]': 'casual'

    }

    # Reference: https://developer.vainglorygame.com/docs#regions
    region = "na"

    assert vgApi.matches(args, region)


def testTelemetry():
    """Assert that the telemetry part of the wrapper is working."""

    # Reference: https://developer.vainglorygame.com/docs#telemetry
    link = "6d6c3d78-2270-11e7-ba8d-0242ac110008"

    assert vgApi.telemetry(link)


def testSamples():
    """Assert that the samples part of the wrapper is working."""

    # Reference: https://developer.vainglorygame.com/docs#get-a-collection-of-samples
    args = {

        'filter[createdAt-start]': '2017-01-15T00:00:00Z',
        'sort': '-createdAt',
        'page[limit]': '50'

    }

    # Reference: https://developer.vainglorygame.com/docs#regions
    region = "na"

    assert vgApi.samples(args, region)
