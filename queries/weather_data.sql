select 
    w.weather_id 
    , w.location_id 
    , l.country 
    , l.location_name 
    , w.last_updated 
    , w.temperature_celsius 
    , w.condition_text 
    , w.humidity 
    , w.wind_kph
from weather w
join locations l 
    on w.location_id = l.location_id
;