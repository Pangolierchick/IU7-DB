with cte (row_nu, id, appid, price) as (
	select row_number() over (partition by inventory.appid order by inventory.appid), id, appid, price
	from inventory
)

select *
from cte
where row_nu = 1;
