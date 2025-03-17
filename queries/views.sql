create view if not exists avg_temperature_per_country as
select 
    l.country  -- country name
    , avg(w.temperature_celsius) as avg_temp  -- average temperature
from weather w
	join locations l 
		on w.location_id = l.location_id
group by l.country;

create view if not exists air_quality_summary as
select 
    l.location_name  -- city or location name
    , aq.air_quality_pm2_5, -- PM2.5 pollution level
    , aq.air_quality_pm10  -- PM10 pollution level
    , aq.air_quality_us_epa_index  -- US EPA air quality index
from air_quality aq
	join locations l 
		on aq.location_id = l.location_id;

create view if not exists temperature_trends as
select 
    h.location_id  -- foreign key reference to locations
    , l.location_name  -- city or location name
    , h.last_updated  -- recorded timestamp
    , h.temperature_celsius  -- historical temperature
from historical_data h
	join locations l 
		on h.location_id = l.location_id;