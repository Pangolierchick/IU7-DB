with RECURSIVE r as (
	select id, parent, name
	from apps
	
	union
	
	select apps.id, apps.parent, apps.name
	from apps
		join r
			on apps.parent = r.id
)

select * from r
order by id;
