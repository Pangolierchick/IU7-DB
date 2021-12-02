drop table if exists SwPr;
drop table if exists PrSh;
drop table if exists ShSw;
drop table if exists Sweets;
drop table if exists Providers;
drop table if exists Shops;

create table if not exists Sweets (
    id bigint primary key,
    name varchar(50),
    compos varchar(50),
    about varchar(100)
);

create table if not exists Providers (
    id bigint primary key,
    name varchar(50),
    inn bigint,
    address varchar(50)
);

create table if not exists Shops (
    id bigint primary key,
    name varchar(50),
    address varchar(50),
    date varchar(30),
    rating int
);

create table if not exists SwPr (
    id bigint primary key,
    sw_id bigint references Sweets (id),
    pr_id bigint references Providers (id)
);

create table if not exists PrSh (
    id bigint primary key,
    sh_id bigint references Shops (id),
    pr_id bigint references Providers (id)
);

create table if not exists ShSw (
    id bigint primary key,
    sh_id bigint references Shops (id),
    sw_id bigint references Sweets (id)
);

insert into Providers(id, name, inn, address) values (1, 'ИП Андрей', 123456789123, 'Улица Госпитальная'),
(2, 'ИП Владимир', 123456789123, 'Улица Боровский проезд'),
(3, 'ИП Степан', 123456789123, 'Улица Госпитальная'),
(4, 'ООО Невероятные конфеты', 123456789123, 'Улица Солнцевский проспект'),
(5, 'ООО так себе конфеты', 123456789123, 'Улица Госпитальная'),
(6, 'ИП Валерий', 123456789123, 'Улица Госпитальная'),
(7, 'ООО Шоколадные конфеты', 123456789123, 'Улица Бауманская'),
(8, 'ООО Карамельные конфеты', 123456789123, 'Улица 50 лет октября'),
(9, 'ООО Просто конфеты', 123456789123, 'Улица Богданово'),
(10, 'ООО Конфеты', 123456789123, 'Улица Госпитальная');

insert into Sweets(id, name, compos, about) values (1, 'Коровка', 'Сахар, молоко', 'ab 1'),
(2, 'Красные батончики', 'Сахар, молоко', 'ab 2'),
(3, 'Зеленые батончики', 'Сахар, молоко', 'ab 3'),
(4, 'Черно-белые батончики', 'Сахар, молоко', 'ab 4'),
(5, 'Птичье молоко', 'Сахар, молоко', 'ab 5'),
(6, 'Raffaelo', 'Сахар, молоко', 'ab 6'),
(7, 'Merci', 'Сахар, молоко', 'ab 7'),
(8, 'Snickers', 'Сахар, молоко', 'ab 8'),
(9, 'MilkiWay', 'Сахар, молоко', 'ab 9'),
(10, 'Kinder surprise', 'Сахар, молоко', 'ab 10');

insert into Shops(id, name, address, date, rating) values(1, 'Пятерочка', 'Колотушкина', '13.12.2010', '8'),
(2, 'Перекросток', 'Пушкина', '13.9.2010', '4'),
(3, 'Фикс прайс', 'Колотушкина', '13.10.2010', '8'),
(4, 'Вкусвилл', 'Пушкина', '13.6.2010', '6'),
(5, 'Магнит', 'Пушкина', '13.10.2010', '1'),
(6, 'Деревенский', 'Колотушкина', '13.10.2010', '10'),
(7, 'Азбука вкуса', 'Пушкина', '13.10.2010', '3'),
(8, 'ЦУМ', 'Пушкина', '13.10.2010', '7'),
(9, 'Дикси', 'Колотушкина', '13.6.2010', '9'),
(10, 'Магазин', 'Пушкина', '13.1.2010', '0');

insert into prsh(id, pr_id, sh_id) values(1, 5, 2),
(2, 1, 5),
(3, 1, 1),
(4, 10, 3),
(5, 6, 3),
(6, 8, 3),
(7, 1, 9),
(8, 5, 10),
(9, 2, 8),
(10, 4, 7);

insert into shsw(id, sh_id, sw_id) values(1, 5, 2),
(2, 1, 5),
(3, 1, 1),
(4, 10, 3),
(5, 6, 3),
(6, 8, 3),
(7, 1, 9),
(8, 5, 10),
(9, 2, 8),
(10, 4, 7);

insert into swpr(id, sw_id, pr_id) values(1, 5, 2),
(2, 1, 5),
(3, 1, 1),
(4, 10, 3),
(5, 6, 3),
(6, 8, 3),
(7, 1, 9),
(8, 5, 10),
(9, 2, 8),
(10, 4, 7);

-- Выводит список магазинов с рейтингом выше 5
select id, name
from shops
where (rating > 5);

-- Выводит все конфеты пронумеровывая их
select ROW_NUMBER() OVER() as rn, name, about
from sweets;

-- Выводит все магазины, которые торгуют конфетами под номером 5

select id, name
from shops
where id in (select sh_id
            from shsw
            where sw_id = 5);



-- Удаление процедуры
DROP PROCEDURE IF EXISTS funcs_like(needle TEXT);

DROP TABLE IF exists out;

CREATE TEMP TABLE IF NOT EXISTS out
(
	type TEXT NOT NULL,
	name Name NOT NULL
);

-- Процедура выводит функции, процедуры в тексте которых есть needle
CREATE OR REPLACE PROCEDURE funcs_like(needle TEXT)
AS $$
BEGIN
INSERT INTO out
(SELECT routine_name, routine_type 
FROM information_schema.routines
WHERE specific_schema='public' AND routine_definition LIKE concat('%', needle, '%'));
END;
$$ LANGUAGE PLPGSQL;

CALL funcs_like('cur');

select *
from out;
