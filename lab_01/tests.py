from src.parser import SteamParser
import json

parser = SteamParser('8344C45B3AB6B7F1F514E226E6DF9ADE')

def friends():
    friends = parser.getFriends('76561198132934832')

    print(friends)

def accs():
    accs = parser.findAccounts('76561198132934832') # 76561198048352441 76561198132934832
    with open('accs.txt', 'w') as f:
        for i in accs:
            print(i, file=f)

accs()
