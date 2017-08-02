"""A small wrapper to grab the data from the pubg website
more functions and features will be added as pubg adds more API calls"""
import json
import requests



class APIException(Exception):
    """Generic exception class for raising errors"""
    pass


class PUBGAPI:
    """Object that will represent the player unknown tracker api"""
    def __init__(self, api_key, platform='pc'):
        self.api_key = api_key
        self.platform = platform
        self.pubg_url = "https://pubgtracker.com/api/profile/{}/".format(self.platform)
        self.pubg_url_steam = "https://pubgtracker.com/api/search?steamId={}/"
        self.headers = {
            'content-type': "application/json",
            'trn-api-key': api_key,
        }
    def player(self, player_handle):
        """Returns the full set of data on a player, no filtering"""
        try:
            url = self.pubg_url + player_handle
            response = requests.request("GET", url, headers=self.headers)
            return json.loads(response.text)
        except BaseException as error:
            print('Unhandled exception: ' + str(error))
            raise

    def player_s(self, sid)       :
        """Returns the full set of data on a player, no filtering"""
        try:
            url = self.pubg_url_steam.format(str(sid))
            response = requests.request("GET", url, headers=self.headers)
            return json.loads(response.text)
        except BaseException as error:
            print('Unhandled exception: ' + str(error))
            raise

    def player_mode_stats(self, player_handle, game_mode='solo', game_region='as'):
        """Returns the stats for a particular mode of play,
        accepts solo, duo and squad.  Will return both regional
        and global stats.  Default gamemode is solo
        by Zac: Add parameter game_region to extract player stats by region directly
        """
        if game_mode not in ['solo', 'duo', 'squad']:
            raise APIException("game_mode must be one of: solo, duo, squad")
        if game_region not in ['as', 'na', 'agg', 'sea', 'eu', 'oc', 'sa']:
            raise APIException("game_region must be one of: as, na, agg, sea, eu, oc, sa")
        try:
            url = self.pubg_url + player_handle
            response = requests.request("GET", url, headers=self.headers)
            data = json.loads(response.text)
            return_data = []
            for stat in data['Stats']:
                if stat['Match'] == game_mode and stat['Region'] == game_region:
                    return_data.append(stat)
            return return_data
        except BaseException as error:
            print('Unhandled exception: ' + str(error))
            raise
    def player_skill(self, player_handle, game_mode='solo'):
        """Returns the current skill rating of the player for a specified gamemode,
        default gamemode is solo"""
        if game_mode not in ['solo', 'duo', 'squad']:
            raise APIException("game_mode must be one of: solo, duo, squad")
        try:
            url = self.pubg_url + player_handle
            response = requests.request("GET", url, headers=self.headers)
            data = json.loads(response.text)
            player_stats = {}
            return_data = []
            for stat in data['Stats']:
                if stat['Match'] == game_mode:
                    for datas in stat['Stats']:
                        if datas['label'] == 'Rating':
                            player_stats[stat['Region']] = datas['value']
            return player_stats
        except BaseException as error:
            print('Unhandled exception: ' + str(error))
            raise
