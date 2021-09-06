import requests
import configparser

def parse_cfg(cfg_path:str) -> dict:
    config = configparser.ConfigParser()
    config.read(cfg_path)

    return config

def get_api_key(cfg:dict):
    return cfg['api']['api_key']

def main():
    config = parse_cfg('./config.ini')

if __name__ == '__main__':
    main()
