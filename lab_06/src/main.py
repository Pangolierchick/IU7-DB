from db import SteamDBase
import configparser

class transaction:
    def __init__(self, n, f):
        self.name = n
        self.func = f
    
    def __call__(self):
        return self.func()

def read_cfg(path:str):
    config = configparser.ConfigParser()
    config.read(path)

    return config

def get_password(cfg:dict):
    return cfg['dbase']['password']

def insert_wrapper(db:SteamDBase):
    def clojure():
        name = input("Введите название: ")
        price = int(input("Введите стоимость: "))

        return db.insert(name, price)

    return clojure

def get_user_time_wrapper(db:SteamDBase):
    def clojure():
        name = input('Введите имя пользователя: ')

        return db.user_time(name)
    
    return clojure

def main():
    cfg = read_cfg('../config.ini')
    dbase = SteamDBase(get_password(cfg))
    funcs = [
            transaction("Cкалярный запрос", dbase.scalar),
            transaction('Запрос с несколькими соединениями (JOIN)', dbase.join),
            transaction('Запрос с ОТВ(CTE) и оконными функциями', dbase.cte),
            transaction('Запрос к метаданным', dbase.meta),
            transaction('Скалярная функция (написанная в третьей лабораторной работе)', dbase.scalar3),
            transaction('Многооператорная или табличная функция (написанная в третьей лабораторной работе)', dbase.table3),
            transaction('Хранимая процедура (написанная в третьей лабораторной работе)', dbase.proc3),
            transaction('Cистемная функция или процедура', dbase.func),
            transaction('Создать таблицу в базе данных, соответствующую тематике БД', dbase.create_table),
            transaction('Выполнить вставку данных в созданную таблицу с использованием инструкции INSERT', insert_wrapper(dbase)),
            transaction('Получить время использование приложений аккаунта по никнейму в формате json', get_user_time_wrapper(dbase))
            ]

    while True:
        print("0  --- Выход из приложения;")

        for i, f in enumerate(funcs):
            print(f"{i + 1} --- {f.name};")

        chosen = int(input("Выберите пункт меню: "))

        if chosen == 0:
            print("Exitting")
            break
        if 0 <= chosen - 1 < len(funcs):
            print("Calling ... ")
            res = funcs[chosen - 1]()
            
            if res is not None:
                for i in res:
                    print(*i)

        

if __name__ == '__main__':
    main()
