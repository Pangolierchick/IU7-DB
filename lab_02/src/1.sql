SELECT inventory.playtime_id, inventory.gifted
FROM inventory JOIN apps ON inventory.appid = apps.id
where apps.id <> 70;
