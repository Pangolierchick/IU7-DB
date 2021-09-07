import requests
import configparser
import parser
import json
import asyncio

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

def main():
    config = parse_cfg('./config.ini')
    p = parser.SteamParser(get_api_key(config))

    apps = p.getApps()
    dumpApps(apps)

if __name__ == '__main__':
    main()
