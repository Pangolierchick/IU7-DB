-- Из таблиц базы данных, созданной в первой лабораторной работе, извлечь данные в JSON.
\cd lab_05/data
\t
\a
\o accs.json
SELECT ROW_TO_JSON(r) FROM accs r;
\t
\a
\o apps.json
SELECT ROW_TO_JSON(r) FROM apps r;
\t
\a
\o inventory.json
SELECT ROW_TO_JSON(r) FROM inventory r;
\t
\a
\o playtime.json
SELECT ROW_TO_JSON(r) FROM playtime r;

-- Выполнить загрузку и сохранение XML или JSON файла в таблицу.
-- Созданная таблица после всех манипуляций должна соответствовать таблице
-- базы данных, созданной в первой лабораторной работе.

create table apps_from_json (
	id bigint primary key,
	name varchar,
	author varchar,
	date date,
	title varchar,
	dlc boolean,
	parent bigint
);

create temp table temp_json (
	data jsonb
);

copy temp_json from 'lab_05/data/apps.json';

insert into apps_from_json(id, name, author, date, title, dlc, parent)
select (data->>'id')::bigint, data->'name', data->'author', (data->>'date')::date, data->'title', (data->>'dlc')::boolean, (data->>'parent')::bigint
from temp_json;

select * from apps_from_json;

-- Создать таблицу, в которой будет атрибут(-ы) с типом XML или JSON, или
-- добавить атрибут с типом XML или JSON к уже существующей таблице.
-- Заполнить атрибут правдоподобными данными с помощью команд INSERT
-- или UPDATE.

create table if not exists game_json (
	data jsonb
);

insert into game_json (data) values
('{"id": 1234, "name": "portal", "author": {"publisher": "Valve", "developer": "Valve"}}'),
('{"id": 4321, "name": "left 4 dead", "author": {"publisher": "Valve", "developer": "Valve"}}');

-- Извлечь JSON фрагмент из JSON документа.
SELECT data->'author' as author
FROM game_json;

-- Извлечь значения конкретных узлов или атрибутов JSON документа.
select data->'author'->'developer' as developer
from game_json;

-- Выполнить проверку существования узла или атрибута.
create or replace function key_exists(json jsonb, key text)
returns boolean 
as $$
begin
    return (json->key) is not null;
END;
$$ language PLPGSQL;

select key_exists(game_json.data, 'auth')
from game_json;

-- Изменить JSON документ.
update context
set data = data || '{"name": "Left 4 Dead 2"}'::jsonb where (data->>'name') = 'left 4 dead'

-- Разделить JSON документ на несколько строк по узлам.
select *
from jsonb_array_elements('[{"id": 1234, "name": "portal", "author": {"publisher": "Valve", "developer": "Valve"}},
{"id": 4321, "name": "left 4 dead", "author": {"publisher": "Valve", "developer": "Valve"}}]')
