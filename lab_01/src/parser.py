import requests
from enum import Enum

class Status(Enum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


class SteamParser:
    APP_LIST_GET      = 'http://api.steampowered.com/ISteamApps/GetAppList/v2'
    APP_GET           = 'http://store.steampowered.com/api/appdetails'
    FRIENDS_LIST_GET  = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
    PROFILE_DESCR_GET = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.apps_cache = None
    
    def getApps(self, force=False):
        if self.apps_cache is None or force:
            r = requests.get(self.APP_LIST_GET, params={ "key": self.api_key })

            if r.status_code == 200:
                self.apps_cache = r.json()['applist']['apps']
                return (r.status_code, self.apps_cache)
            else:
                return (r.status_code, None)
        
        return (Status.OK, self.apps_cache)
    
    def getFriends(self, steam_id):
        pass
    
    def getProfile(self, steam_id):
        pass

    def getApp(self, app_id):
        pass


