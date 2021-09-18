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

    apps = base.getApps()

    for i, app in enumerate(apps):
        if i != 0:
            with base.connection.cursor() as cur:
                cur.execute(f"update apps SET parent={apps[i - 1][0]} where id={app[0]}")
            
            base.connection.commit()


if __name__ == '__main__':
    log.basicConfig(filename="db_lab01.log", level=log.INFO, format='%(asctime)s [ %(levelname)s ] %(message)s', datefmt='[ %d-%m-%y %H:%M:%S ] ')
    main()
