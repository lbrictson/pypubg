"""A small wrapper to grab the data from the pubg website
more functions and features will be added as pubg adds more API calls"""
import json
import requests

import constants

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

    def _get_player_profile(self, player_handle):
        """Returns pubg player profile from PUBG api, no filtering

            :param player_handle: player PUBG profile name
            :type player_handle: str
            :return: return json from PUBG API
            :rtype: dict
        """
        url = self.pubg_url + player_handle
        response = requests.request("GET", url, headers=self.headers)
        data = json.loads(response.text)
        return data

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

    def player_mode_stats(self, player_handle, game_mode=constants.GAME_MODE_WILDCARD, game_region=constants.GAME_REGION_WILDCARD):
        """Returns the stats for a particular mode of play,
        accepts solo, duo and squad.  Will return both regional
        and global stats.  Default gamemode is solo
        by Zac: Add parameter game_region to extract player stats by region directly
        """
        if game_mode not in constants.GAME_MODES:
            raise APIException("game_mode must be one of: solo, duo, squad, all")
        if game_region not in constants.GAME_REGIONS:
            raise APIException("game_region must be one of: as, na, agg, sea, eu, oc, sa, all")
        try:
            data = self._get_player_profile(player_handle)
            data = self._filter_gameplay_stats(data, game_mode, game_region)
            return data
        except BaseException as error:
            print('Unhandled exception: ' + str(error))
            raise

    def _filter_gameplay_stats(self, data, game_mode, game_region):
        """Returns gameplay stats that are filtered by game_mode and game_region.

            :param data: Json of gameplay stats.
            :type data: dict
            :param game_mode: Target game mode.
            :type game_mode: str
            :param game_region: Target game region.
            :type game_region: str
            :return: return list of gameplay stats with target game mode and region.
            :rtype: list
        """
        return_data = []
        for stat in data['Stats']:
            if self._is_target_game_mode(stat, game_mode) and self._is_target_region(stat, game_region):
                return_data.append(stat)
        return return_data

    def _is_target_game_mode(self, stat, game_mode):
        """Returns if the stat matches target game mode.

            :param stat: Json of gameplay stat.
            :type stat: dict
            :param game_mode: Target game mode.
            :type game_mode: str
            :return: return does the stat matches target game mode.
            :rtype: bool
        """
        if game_mode == constants.GAME_MODE_WILDCARD:
            return True
        return stat['Match'] == game_mode

    def _is_target_region(self, stat, game_region):
        """Returns if the stat matches target game region.

            :param stat: Json of gameplay stat.
            :type stat: dict
            :param game_region: Target game region.
            :type game_region: str
            :return: return does the stat matches target game region.
            :rtype: bool
        """
        if game_region == constants.GAME_REGION_WILDCARD:
            return True
        return stat['Region'] == game_region

    def player_skill(self, player_handle, game_mode='solo'):
        """Returns the current skill rating of the player for a specified gamemode,
        default gamemode is solo"""
        if game_mode not in constants.GAME_MODES:
            raise APIException("game_mode must be one of: solo, duo, squad, all")
        try:
            data = self._get_player_profile(player_handle)
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
