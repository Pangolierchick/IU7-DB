select *
from accs join (select user_id, count(*)
			   from inventory
			   group by user_id) as cnt on accs.id = cnt.user_id;
