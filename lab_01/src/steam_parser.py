import requests
from enum import Enum
import time

class Status(Enum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_ERROR = 500

class APILinks(Enum):
    APP_LIST_GET        = 'http://api.steampowered.com/ISteamApps/GetAppList/v2'
    APP_GET             = 'http://store.steampowered.com/api/appdetails'
    FRIENDS_LIST_GET    = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/'
    PROFILE_DESCR_GET   = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
    PROFILES_APPS       = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/'
    PLAYER_ACHIEVEMENTS = 'http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/'
    CURRENT_PLAYING     = 'http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1'
    DOTA2_ITEMS         = 'http://api.steampowered.com/IEconDOTA2_570/GetGameItems/v1'
    APP_NEWS            = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/'
    GET_STATS           = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/'
    APP_DETAILS         = 'http://store.steampowered.com/api/appdetails/'

class SteamParser:
    def __init__(self, api_key:str):
        self.api_key = api_key
        self.apps_cache = None
    
    def getApps(self, force=False):
        if self.apps_cache is None or force:
            r = requests.get(APILinks.APP_LIST_GET.value, params={ "key": self.api_key })

            if r.status_code == Status.OK.value:
                self.apps_cache = r.json()['applist']['apps']
                return (r.status_code, self.apps_cache)
            else:
                return (r.status_code, None)
        
        return (Status.OK, self.apps_cache)
    
    def getFriends(self, steam_id):
        r = requests.get(APILinks.FRIENDS_LIST_GET.value, params = { "key": self.api_key, "steamid": steam_id, "realtionship": "friend" })

        if r.status_code == Status.OK.value:
            try:
                return r.json()['friendslist']['friends']
            except KeyError:
                return []
        
        return []
    
    def getProfile(self, steam_id):
        r = requests.get(APILinks.PROFILE_DESCR_GET.value, params = { 'key': self.api_key, 'steamids': steam_id })

        if r.status_code == Status.OK.value:
            if len(r.json()['response']['players']) > 0:
                return r.json()['response']['players'][0]
        return {}

    def getApp(self, app_id):
        r = requests.get(APILinks.APP_GET.value, params = { 'key': self.api_key, 'appids': app_id })

        if r.status_code == Status.OK.value:
            return r.json()
        
        return {}
    
    def timeout(self, secs=1.5):
        time.sleep(secs)
    
    def findAccounts(self, start_id):
        NEED_ACCS = 1000

        accounts = [start_id]
        friends_stack = set([start_id])

        start = time.time()

        while len(accounts) < NEED_ACCS and len(friends_stack) > 0:
            curr_id = friends_stack.pop()

            friends = self.getFriends(curr_id)

            for friend in friends:
                friends_stack.add(friend['steamid'])
                if friend['steamid'] not in accounts:
                    accounts.append(friend['steamid'])
            
            self.timeout(1.5)
            
            print(f'{len(accounts)} / {NEED_ACCS}\t\t {int(time.time() - start)} sec')
        
        print(accounts)

        return accounts
    
    def getProfilesApps(self, steamid):
        r = requests.get(APILinks.PROFILES_APPS.value, { 'key': self.api_key, 'steamid': steamid })

        if r.status_code == Status.OK.value:
            try:
                return r.json()['response']['games']
            except KeyError:
                return {}
        
        return {}
    
    def getProfilesAchievment(self, steamid, appid):
        r = requests.get(APILinks.PLAYER_ACHIEVEMENTS.value, { 'key': self.api_key, 'steamid': steamid, 'appid': appid })

        if r.status_code == Status.OK.value:
            return r.json()['response']
        
        return {}
    
    def getCurrentPlayers(self, appid):
        r = requests.get(APILinks.CURRENT_PLAYING.value, { 'key': self.api_key, 'appid': appid })

        if r.status_code == Status.OK.value:
            return r.json()['response']
        
        return {}
    
    def getDota2Items(self):
        r = requests.get(APILinks.DOTA2_ITEMS.value, { 'key': self.api_key })

        if r.status_code == Status.OK.value:
            return r.json()['result']['items']
        
        return {}
    
    def getAppNews(self, appid, count, maxlenght=100):
        r = requests.get(APILinks.APP_NEWS.value, { 'key': self.api_key, 'appid': appid, 'count': count, 'maxlength':maxlenght })

        if r.status_code == Status.OK.value:
            return r.json()
        
        return {}
    
    def getStats(self, steamid, appid=730):
        r = requests.get(APILinks.GET_STATS.value, { 'key': self.api_key, 'appid': appid, 'steamid': steamid })
        
        if r.status_code == Status.OK.value:
            return r.json()
                
        return {}
    
    def getAppDetails(self, steamid):
        r = requests.get(APILinks.APP_DETAILS.value, {'appids': steamid})
        r_json = r.json()
        if r.status_code == Status.OK.value and r_json[str(steamid)]['success']:
            return r_json[str(steamid)]['data']
        
        return {}
    



