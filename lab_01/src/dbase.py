import psycopg2

class SteamDBase:
    def __init__(self, password):
        self.connection = psycopg2.connect(database='db_labs', user='postgres', password=password)

        self.createAccsTable()
        self.createAppsTable()
        self.createPlaytimeTable()
        self.createInventoryTable()
    
    def __del__(self):
        self.connection.close()

    def createAppsTable(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS apps(
                    id bigint PRIMARY KEY,
                    name varchar NOT NULL,
                    author varchar,
                    date date,
                    title VARCHAR NOT NULL
                    )
                '''
                )

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
    
    def createPlaytimeTable(self):
        with self.connection.cursor() as cur:
            cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS playtime (
                id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                forever int NOT NULL,
                weeks2 int NOT NULL,
                windows int NOT NULL,
                mac int NOT NULL,
                linux int NOT NULL
            )
            '''
            )
        
        self.connection.commit()

    def createInventoryTable(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                CREATE TABLE IF NOT EXISTS inventory (
                    id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
                    appid bigint REFERENCES apps(id),
                    playtime_id uuid REFERENCES playtime(id),
                    user_id bigint REFERENCES accs(id),
                    gifted int NOT NULL,
                    price int NOT NULL
                )
                '''
            )
        
        self.connection.commit()

    def insertApps(self, apps):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(apps))
            cur.execute('INSERT INTO apps (id, name, author, date, title) VALUES ' + records_list_template, apps)
        
        self.connection.commit()

    def insertAccs(self, accs):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(accs))
            cur.execute('INSERT INTO accs (id, name, timecreated, profileurl, profilestate) VALUES ' + records_list_template, accs)
        
        self.connection.commit()

    def insertInventory(self, apps):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(apps))
            cur.execute('INSERT INTO inventory (id, appid, playtime_id, user_id, gifted, price) VALUES ' + records_list_template, apps)
        
        self.connection.commit()
    
    def insertPlaytime(self, playtime):
        with self.connection.cursor() as cur:
            records_list_template = ','.join(['%s'] * len(playtime))
            cur.execute('INSERT INTO playtime (id, forever, weeks2, windows, mac, linux) VALUES ' + records_list_template, playtime)
    
        self.connection.commit()
    
    def rollback(self):
        with self.connection.cursor() as cur:
            cur.execute('rollback')
        
        self.connection.commit()
    

