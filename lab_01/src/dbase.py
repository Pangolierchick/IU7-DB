import psycopg2

class SteamDBase:
    def __init__(self):
        self.connection = psycopg2.connect(database='db_labs', user='postgres', password='198011901')

        self.createAccsTable()
        self.createAppTable()

    def createAppTable(self):
        with self.connection.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS apps (id INT PRIMARY KEY, name VARCHAR NOT NULL)')
        
        self.connection.commit()
    
    def createAccsTable(self):
        with self.connection.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS accs (id INT PRIMARY KEY, name VARCHAR NOT NULL, timecreated INT NOT NULL, profileurl VARCHAR)')
        
        self.connection.commit()

db = SteamDBase()
