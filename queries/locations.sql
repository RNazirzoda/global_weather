-- Top 5 coutnries with the highest average temperature 
select 
    country
    , avg_temp
from 
    avg_temperature_per_country
order by 
    avg_temp desc
limit 5;

-- cities with the most polluted air (pm2.5) 
select 
    location_name
    , air_quality_pm2_5
from 
    air_quality_summary
order by 
    air_quality_pm2_5 desc
limit 5;

-- average temperature by month
select 
    strftime('%Y-%m', last_updated) as year_month  -- extract year and month
    , avg(temperature_celsius) as avg_temp  -- calculate average temperature
from 
    historical_data
group by 
    year_month
order by 
    year_month;