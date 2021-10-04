select id, name, profilestate,
case 
	when profilestate = 0
	then 'Не в сети'
	else 'В сети'
	end profilestate
from accs;
