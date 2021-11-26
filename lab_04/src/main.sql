-- Скалярная функция.
-- Возвращает стоимость игры с учетом подарка.

create or replace function get_price_p(gifted integer, price integer)
returns integer as $$
    return price * gifted
$$ language plpython3u;

select appid, get_price_p(gifted, price)
from inventory;


-- Пользовательская агрегатная функция CLR
-- Возвращает суммарную стоимость приложений у пользователя
create or replace function get_inv_price_p(uid bigint)
returns integer as $$
    query = plpy.prepare("select price from inventory where inventory.user_id=$1;", ["bigint"])
    res = plpy.execute(query, [uid])
    
    total_price = 0
    
    for i in res:
        total_price += i["price"]
    
    return total_price

$$ language plpython3u;

select * from get_inv_price_p(76561198073820384);


-- Подставляемая табличная функция.
-- Возвращает таблицу из id и времени использования на ОС windows, если оно больше нуля.
create or replace function windows_playtime_p()
returns table (
    id uuid,
    windows integer
) as $$
    query = "select playtime.id, playtime.windows from playtime where playtime.windows > 0"
    res = plpy.execute(query)
    
    for i in res:
        yield(i["id"], i["windows"])
$$ language plpython3u;

select * from windows_playtime_p();

-- Хранимая процедура с параметрами.
-- Изменяет время использования приложения.
create or replace procedure change_playtime_p(uid uuid, w int, m int, l int)
as $$
	query = plpy.prepare("""update playtime set forever = forever + $1 + $2 + $3, 
			windows = windows + $1, 
			mac = mac + $2, 
			linux = linux + $2
			where playtime.id = $4;""", ["int", "int", "int", "uuid"])
	
	res = plpy.execute(query, [w, m, l, uid])
$$ language plpython3u;

call change_playtime('0003809f-3d1f-4be8-adb1-8fbfefb446a4', 30, 0, 20);

select * from playtime where playtime.id = '0003809f-3d1f-4be8-adb1-8fbfefb446a4';

-- Триггер After
-- Выводит уведомление, когда пользователь получает приложение в подарок.

create or replace function present_handler()
returns trigger as $$
	if TD["new"]["gifted"] > 0:
		plpy.notice(f"User {TD['new']['user_id']} got present {TD['new']['appid']}. Congratulations")
$$ language PLPYTHON3U;

create trigger present_trigger_p after insert on inventory
for row execute procedure present_handler();

insert into inventory(id, appid, playtime_id, user_id, gifted, price)
values(gen_random_uuid(), 4500, null, 76561198070966937, 1, 0);
delete from inventory
where user_id = 76561198070966937 and appid = 4500;

-- Определяемый пользователем тип данных CLR

create type product as (
	name varchar,
	title varchar
);

create or replace function set_product_p(n varchar, t varchar)
returns setof product
as $$
	return ([n, t],)
$$ language plpython3u;

select * from set_product_p('dota 2', 'valve');
