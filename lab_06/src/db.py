import psycopg2
import uuid

class SteamDBase:
    def __init__(self, password):
        self.connection = psycopg2.connect(database='db_labs', user='postgres', password=password)
    
    def __del__(self):
        self.connection.close()
    
    def scalar(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                select avg(price) from inventory;
                '''
            )
            data = cur.fetchall()

        self.connection.commit()

        return data

    def join(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                select accs.id, sum(inventory.price)
                from accs
                join inventory on accs.id=inventory.user_id
                group by accs.id;
                '''
            )

            data = cur.fetchall()
        
        return data
    
    def cte(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                with cte (row_nu, id, appid, price) as (
                select row_number() over (partition by inventory.appid order by inventory.appid), id, appid, price
                from inventory)

                select *
                from cte
                where row_nu = 1;
                '''
            )

            data = cur.fetchall()
        
        return data

    def meta(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                SELECT pg.oid, pg.datconnlimit FROM pg_database pg WHERE pg.datname = 'db_labs';
                '''
            )

            data = cur.fetchall()
        
        return data

    def scalar3(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                -- create or replace function get_price(gifted integer, price integer)
                -- returns integer as $$
                -- begin
                --     return price * gifted;
                -- end;
                -- $$ language plpgsql;

                select appid, get_price(gifted, price)
                from inventory;
                '''
            )

            data = cur.fetchall()
        
        return data

    def table3(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                 create or replace function find_user_games(_id bigint)
                 returns table(
                 	id bigint,
                 	appid bigint,
                 	name varchar
                 ) as $$

                 begin
                 	create temp table if not exists games (
                 		id bigint,
                 		appid bigint,
                 		name varchar
                 	);
              
                 	insert into games (id, appid, name)
                 	select inventory.user_id, inventory.appid, apps.name
                 	from inventory join apps on inventory.appid = apps.id 
                 	where inventory.user_id = _id;
                    
                 	return query
                 	select * from games;
                 end;
                 $$ language plpgsql;

                select *
                from find_user_games(76561198070966937);
                '''
            )

            data = cur.fetchall()
        
        return data

    def proc3(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                -- create or replace procedure change_playtime(uid uuid, w int, m int, l int)
                -- as $$
                -- begin
                --     update playtime
                --     set forever = forever + w + m + l,
                --     windows = windows + w,
                --     mac = mac + m,
                --     linux = linux + l
                --     where playtime.id = uid;
                -- end;
                -- $$ language plpgsql;

                call change_playtime('0003809f-3d1f-4be8-adb1-8fbfefb446a4', 30, 0, 20)
                '''
            )

    def func(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                select current_date;
                '''
            )

            data = cur.fetchall()
        
        return data

    def create_table(self):
        with self.connection.cursor() as cur:
            cur.execute(
                '''
                create table if not exists Prod(
                    id uuid primary key,
                    name varchar not null,
                    price int CHECK (price >= 0) not null
                );
                '''
            )

        self.connection.commit()
        
    
    def insert(self, n, p):
        cur_uuid = uuid.uuid4()

        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                insert into Prod(id, name, price) 
                values ('{cur_uuid}', '{n}', '{p}');
                '''
            )

        self.connection.commit()

    def user_time(self, name):
        print(f'Inputted nickname is: "{name}"')
        with self.connection.cursor() as cur:
            cur.execute(
                f'''
                create or replace function get_user_time(n varchar)
                returns table (
                        appid 	bigint,
                        mac 	bigint,
                        linux 	bigint,
                        windows bigint
                ) as $$
                begin
                    drop table if exists app_time;
                    create table if not exists app_time (
                        appid 	bigint,
                        mac 	bigint,
                        linux 	bigint,
                        windows bigint
                    );
                    
                    insert into app_time(appid, mac, linux, windows)
                    select inventory.appid, playtime.mac, playtime.linux, playtime.windows
                    from accs
                    join inventory on accs.id = inventory.user_id 
                    join playtime on inventory.playtime_id  = playtime.id
                    where accs."name" = n;

                    return query
                    select *
                    from app_time;
                end;
                $$ language plpgsql;

                select row_to_json(r) from get_user_time('{name}') as r;
                '''
            )
            try:
                data = cur.fetchall()
            except Exception as e:
                print(e)
                return None
        return data
