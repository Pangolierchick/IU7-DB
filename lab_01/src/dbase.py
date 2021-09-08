import psycopg2

class SteamDBase:
    def __init__(self, password):
        self.connection = psycopg2.connect(database='db_labs', user='postgres', password=password)

        self.createAccsTable()
        self.createAppTable()
        self.createInventory()
        self.createDota2Items()
    
    def __del__(self):
        self.connection.close()

    def createAppTable(self):
        with self.connection.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS apps (id bigint PRIMARY KEY, name VARCHAR NOT NULL)')

        self.connection.commit()

    def createAccsTable(self):
        with self.connection.cursor() as cur:
            cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS accs (
            id bigint PRIMARY KEY,
            name VARCHAR NOT NULL,
            timecreated INT NOT NULL,
            profileurl VARCHAR,
            profilestate INT,
            CHECK (timecreated > 0))
            ''')

        self.connection.commit()

    def createInventory(self):
        with self.connection.cursor() as cur:
            cur.execute('CREATE TABLE IF NOT EXISTS inventory (appid bigint REFERENCES apps (id), playtime INT, playtime_2weeks INT, userid bigint REFERENCES accs (id), CHECK(playtime >= 0))')
        
        self.connection.commit()

    def createDota2Items(self):
        with self.connection.cursor() as cur:
            cur.execute('''CREATE TABLE IF NOT EXISTS dota2items
            (id INT PRIMARY KEY,
            name VARCHAR,
            cost INT,
            secret_shop INT,
            side_shop INT,
            recipe INT
            )''')
        
        self.connection.commit()

    def insertApps(self, apps):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(apps))
            cur.execute('INSERT INTO apps (id, name) VALUES ' + records_list_template, apps)
        
        self.connection.commit()

    def insertAccs(self, accs):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(accs))
            cur.execute('INSERT INTO accs (id, name, timecreated, profileurl, profilestate) VALUES ' + records_list_template, accs)
        
        self.connection.commit()

    def insertInventory(self, apps):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(apps))
            cur.execute('INSERT INTO inventory (appid, playtime, playtime_2weeks, userid) VALUES ' + records_list_template, apps)
        
        self.connection.commit()
    
    def insertDota2Items(self, items):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(items))
            cur.execute('INSERT INTO dota2items (id, name, cost, secret_shop, side_shop, recipe) VALUES ' + records_list_template, items)
        
        self.connection.commit()

