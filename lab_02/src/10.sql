select appid,
case
	when price < 5 then 'Inexpensive'
	when price < 10 then 'Fair'
	when price < 20 then 'Expensive'
	else 'Very expensive'
end price
from inventory;
