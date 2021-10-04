with table_qte (id, appid, price) as
(
	select id, appid, price
	from inventory
)

select appid, sum(price)
from table_qte
group by appid;
