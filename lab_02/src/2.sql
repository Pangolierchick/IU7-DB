SELECT playtime.id, playtime.forever
from playtime
where playtime.forever between 100 and 1000
order by playtime.forever;
