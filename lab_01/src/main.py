import requests
import configparser
import steam_parser
import json
import logging as log
import dbase
import re
import uuid
import random

def parse_cfg(cfg_path:str) -> dict:
    config = configparser.ConfigParser()
    config.read(cfg_path)

    return config

def get_api_key(cfg:dict):
    return cfg['api']['api_key']

def dumpAccs(accs, filename='accs.txt'):
    with open(filename, 'w') as f:
        for i in accs:
            print(i, file=f)

def dumpApps(apps, filename='apps.json'):
    with open(filename, 'w') as f:
        json.dump(apps, f, indent=4)


def getPublicAccs(parser, accs):
    public = []

    NEED = 1000
    public_len = 0

    for i, id in enumerate(accs):
        account = parser.getProfile(id)

        if public_len > NEED:
            break

        try:
            if account['communityvisibilitystate'] == 3:
                public.append(account)
                public_len += 1
        except KeyError:
            pass

        if len(public) > 50:
            dumpPublicAccs(public)
            public.clear()

        
        print(f'{i} / {len(accs)} / {len(public)}\t\tEstimated time: {(len(accs) - i) * 0.5} secs')
        parser.timeout(0.3)
    
    return public

def dumpPublicAccs(accs, filename='accs.json'):
    with open(filename, 'a') as f:
        json.dump(accs, f, indent=4)
        
def readAccs(filename='accs.txt'):
    with open(filename, 'r') as f:
        return f.readlines()

def readAccsJson(filename='accs.json'):
    with open(filename, 'r') as f:
        return json.load(f)

def readAppsJson(filename='apps.json'):
    with open(filename, 'r') as f:
        return json.load(f)

def main():
    config = parse_cfg('./config.ini')
    p = steam_parser.SteamParser(get_api_key(config))
    base = dbase.SteamDBase(config['dbase']['password'])

    accs = readAccsJson()

    for acc in accs:
        inv = p.getProfilesApps(acc['steamid'])

        player_playtime  = []
        player_inventory = []

        for app in inv:
            playtime_uuid  = str(uuid.uuid4())
            inventory_uuid = str(uuid.uuid4())

            playtime = (playtime_uuid, app['playtime_forever'], 0, app['playtime_windows_forever'], app['playtime_mac_forever'], app['playtime_linux_forever'])

            inv_record = (inventory_uuid, app['appid'], playtime_uuid, acc['steamid'], random.randint(0, 1), random.randint(0, 30))


            try:
                base.insertPlaytime((playtime,))
                base.insertInventory((inv_record,))
            except:
                base.rollback()
                print('Trying to find app')
                app_d = p.getAppDetails(app['appid'])

                if len(app_d) != 0:
                    try:
                        date = app_d['release_date']['date']
                    except:
                        continue
                    
                    author = None

                    try:
                        author = app_d['developers'][0]
                    except:
                        pass
                    
                    if not re.match(r"\d{1,2} \D*\, \d{4}", date):
                        date = None
                    
                    app_info = ((app['appid'], app_d['name'], author, date, app_d['short_description']),)

                    base.insertApps(app_info)

                    print('SUCCESS')

                    base.insertInventory((inv_record,))

                

            # player_playtime.append(playtime)
            # player_inventory.append(inv_record)

        
        # try:
        #     base.insertPlaytime(player_playtime)
        #     base.insertInventory(player_inventory)
        # except:
        #     p.getAppDetails()



if __name__ == '__main__':
    log.basicConfig(filename="db_lab01.log", level=log.INFO, format='%(asctime)s [ %(levelname)s ] %(message)s', datefmt='[ %d-%m-%y %H:%M:%S ] ')
    main()
