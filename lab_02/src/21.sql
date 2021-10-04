delete
from inventory
where price > all (SELECT avg(price)
                   from inventory);
