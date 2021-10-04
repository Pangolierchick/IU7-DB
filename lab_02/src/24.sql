select id, appid,
avg(inventory.price) over (partition by appid) as avg_price,
min(inventory.price) over (partition by appid) as min_price,
max(inventory.price) over (partition by appid) as max_price
from inventory
order by appid;
