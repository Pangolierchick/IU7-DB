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


