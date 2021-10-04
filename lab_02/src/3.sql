SELECT apps.id, apps.name, apps.author
FROM apps
WHERE apps.name LIKE '%LEGO%'
order by apps.id;
