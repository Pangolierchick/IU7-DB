select user_id, sum(price)
from inventory
group by user_id
having sum(price) > 100;
