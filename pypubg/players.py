"""A small wrapper to grab the data from the pubg website
more functions and features will be added as pubg adds more API calls"""
import requests
import json



def get_player(player_handle, api_key):
    """Gets all of the stats available for the specified player.  The player
    handle is the in-game username"""
    
    url = "https://pubgtracker.com/api/profile/pc/" + player_handle
    headers = {
        'content-type': "application/json",
        'trn-api-key': api_key,
        }
    try:
        response = requests.request("GET", url, headers=headers)

        return json.loads(response.text)
    except BaseException as e:
        print('Unhandled exception: ' + str(e))
        raise
