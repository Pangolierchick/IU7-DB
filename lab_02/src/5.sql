SELECT playtime.forever
FROM playtime
WHERE EXISTS (
                        SELECT inventory.playtime_id 
                        FROM inventory
                        WHERE inventory.appid = 12120
                          )
order by playtime.forever;    
