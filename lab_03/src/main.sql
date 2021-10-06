-- Скалярная функция.
-- Возвращает стоимость игры с учетом подарка.
create or replace function get_price(gifted integer, price integer)
returns integer as $$
begin
    return price * gifted;
end;
$$ language plpgsql;

select appid, get_price(gifted, price)
from inventory;

-- Подставляемая табличная функция.
-- Возвращает таблицу из id и времени использования на ОС windows, если оно больше нуля.
create or replace function windows_playtime()
returns table (
	id uuid,
	windows integer
)
as $$
begin
	return query 
	select playtime.id, playtime.windows
	from playtime
	where playtime.windows > 0
	order by playtime.windows;
end;
$$ language plpgsql;

select *
from windows_playtime();

-- Многооператорная табличная функция.
-- Возвращает все игры и их названия по id пользователя.
create or replace function find_user_games(_id bigint)
returns table(
	id bigint,
	appid bigint,
	name varchar
) as $$

begin
	drop table games;
	create temp table games (
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

-- Рекурсивная функция.
create or replace function reqursive()
returns table (
    id     bigint,
    parent bigint,
    name   varchar
) as $$
begin
    return query
    with RECURSIVE r as (
	select apps.id, apps.parent, apps.name
	from apps
	
	union
	
	select apps.id, apps.parent, apps.name
	from apps
		join r
			on apps.parent = r.id
	)
	
    select *
	from r
    order by r.id;
end;
$$ language plpgsql;

select *
from reqursive();

-- Хранимая процедура с параметрами.
-- Изменяет время использования приложения.
create or replace procedure change_playtime(uid uuid, w int, m int, l int)
as $$
begin
	update playtime
	set forever = forever + w + m + l,
	windows = windows + w,
	mac = mac + m,
	linux = linux + l
	where playtime.id = uid;
end;
$$ language plpgsql;

call change_playtime('0003809f-3d1f-4be8-adb1-8fbfefb446a4', 30, 0, 20)

-- Рекурсивная хранимая процедура.
create or replace procedure reqursive_proc(app_id bigint, iter int)
as $$
declare
	name varchar;
	author varchar;
	parent bigint;
begin
	if iter > 10 then
		return;
	end if;
	
	select apps.name, apps.author, apps.parent
	from apps
	where apps.id = app_id
	into name, author, parent;

	raise notice '| name %s | id %s | parent %s |', name, app_id, parent;
	
	call reqursive_proc(parent, iter + 1);
end;
$$ language plpgsql;

call reqursive_proc(10, 0);

-- Хранимая процедура с курсором.
-- Возвращает аккаунты, зарегистрированные между lo и hi
create or replace procedure accs_between(lo date, hi date)
as $$
declare
	cur_acc record;
	accs_cur cursor for 
		select *
		from accs
		where to_timestamp(accs.timecreated)::date between lo and hi;
begin
	open accs_cur;
	loop
		fetch accs_cur into cur_acc;
		raise notice 'Name: %s, date %s', cur_acc.name, to_timestamp(cur_acc.timecreated)::date;
		exit when not found;
	end loop;
	close accs_cur;
end;
$$ language plpgsql;

call accs_between('2010-01-01', current_date);


