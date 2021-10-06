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


