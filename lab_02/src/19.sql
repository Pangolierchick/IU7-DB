update inventory
set price = price + (select avg(price) from inventory);
