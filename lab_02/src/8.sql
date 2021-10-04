select id, forever
from playtime
where forever > (select avg(forever) from playtime)
