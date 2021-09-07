import psycopg2

class SteamDBase:
    def __init__(self, password):
        self.connection = psycopg2.connect(database='db_labs', user='postgres', password=password)

        self.createAccsTable()
        self.createAppTable()
        self.createInventory()

    def createAppTable(self):
        with self.connection.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS apps (id INT PRIMARY KEY, name VARCHAR NOT NULL)')
        
        self.connection.commit()
    
    def createAccsTable(self):
        with self.connection.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS accs (id INT PRIMARY KEY, name VARCHAR NOT NULL, timecreated INT NOT NULL, profileurl VARCHAR, CHECK (timecreated > 0))')
        
        self.connection.commit()
    
    def createInventory(self):
        with self.connection.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS inventory (appid INT REFERENCES apps (id), playtime INT, userid INT REFERENCES accs (id), CHECK (appid > 0), CHECK(playtime >= 0), CHECK(userid > 0))')
        
        self.connection.commit()
    
    def insertApps(self, apps):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(apps))
            cur.execute('INSERT INTO apps (id, name) VALUES ' + records_list_template, apps)
    
        self.connection.commit()
    
    def insertAccs(self, accs):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(accs))
            cur.execute('INSERT INTO accs (id, name, timecreated, profileurl) VALUES ' + records_list_template, accs)
    
        self.connection.commit()
    
    def insertInventory(self, apps):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(apps))
            cur.execute('INSERT INTO inventory (appid, playtime, userid) VALUES ' + records_list_template, apps)
    
        self.connection.commit()
