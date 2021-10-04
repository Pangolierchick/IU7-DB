SELECT playtime.forever
FROM playtime
WHERE playtime.id IN (
                        SELECT inventory.playtime_id 
                        FROM inventory
                        WHERE inventory.appid = 620
                          );    
