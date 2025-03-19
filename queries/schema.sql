create table if not exists locations (
    location_id integer not null unique  -- primary key
    , country text not null  -- country name
    , location_name text not null  -- city or location name
    , latitude real not null  -- geographic latitude
    , longitude real not null  -- geographic longitude
    , timezone text not null  -- timezone
    , primary key(location_id)
);

create table if not exists weather (
    weather_id integer not null unique  -- primary key
    , location_id integer not null  -- foreign key reference to locations
    , last_updated timestamp not null  -- timestamp of last update
    , temperature_celsius real  -- temperature in Celsius
    , condition_text text  -- weather condition description
    , humidity integer  -- humidity percentage
    , wind_kph real  -- wind speed in kph
    , primary key(weather_id)
    , foreign key(location_id) references locations(location_id)
);

create table if not exists air_quality (
    air_quality_id integer not null unique  -- primary key
    , location_id integer not null  -- foreign key reference to locations
    , last_updated timestamp not null  -- timestamp of last update
    , air_quality_pm2_5 real  -- PM2.5 pollution level
    , air_quality_pm10 real  -- PM10 pollution level
    , air_quality_us_epa_index integer  -- US EPA air quality index
    , air_quality_gb_defra_index integer  -- UK DEFRA air quality index
    , primary key(air_quality_id)
    , foreign key(location_id) references locations(location_id)
);

create table if not exists climate_zones (
    climate_zone_id integer not null unique  -- primary key
    , location_id integer not null  -- foreign key reference to locations
    , climate_zone text not null  -- climate zone classification
    , primary key(climate_zone_id)
    , foreign key(location_id) references locations(location_id)
);

create table if not exists weather_forecast (
    forecast_id integer not null unique  -- primary key
    , location_id integer not null  -- foreign key reference to locations
    , forecast_date timestamp not null  -- forecasted date
    , forecast_temperature real  -- predicted temperature in Celsius
    , forecast_condition text  -- predicted weather condition
    , primary key(forecast_id)
    , foreign key(location_id) references locations(location_id)
);

create table if not exists historical_data (
    history_id integer not null unique  -- primary key
    , location_id integer not null  -- foreign key reference to locations
    , last_updated timestamp not null  -- recorded timestamp
    , temperature_celsius real  -- historical temperature in Celsius
    , condition_text text  -- historical weather condition
    , humidity integer  -- historical humidity percentage
    , primary key(history_id)
    , foreign key(location_id) references locations(location_id)
);

create table if not exists time_dimensions (
    time_id integer not null unique  -- primary key
    , last_updated timestamp not null  -- recorded timestamp
    , date date not null  -- extracted date part
    , time time not null  -- extracted time part
    , primary key(time_id)
);