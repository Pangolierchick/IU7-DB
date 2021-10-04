select *
from playtime
where forever > all (select forever
					from playtime
					where mac <> 0);
