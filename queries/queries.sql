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

-- moving average temperature (оконная функция)
select 
    location_id,
    last_updated,
    temperature_celsius,
    avg(temperature_celsius) over (
        partition by location_id 
        order by last_updated 
        rows between 6 preceding 
        and current row
        ) as moving_avg_temp
from weather;

-- find locations with above average temperatures (подзапрос)
select location_name, temperature_celsius
from weather
where temperature_celsius > (
    select avg(temperature_celsius) 
    from weather
);