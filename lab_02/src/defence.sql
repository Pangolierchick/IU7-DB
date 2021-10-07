select accs.name, playtime.linux
from inventory as inv 
join playtime on inv.playtime_id = playtime.id
join accs on accs.id = inv.user_id
where linux < all (select avg(forever)
					from playtime
					where mac <> 0) and linux <> 0;

