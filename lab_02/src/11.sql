select id, name
into temp dlcs
from apps
where dlc = true;
