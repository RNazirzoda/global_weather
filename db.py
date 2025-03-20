import duckdb
import pandas as pd

DB_FILE = "my.db"

def fetch_date_boundaries():
    """Получает минимальную и максимальную даты в таблице weather."""
    with duckdb.connect(DB_FILE) as conn:
        min_date, max_date = conn.execute("""
            select min(cast(last_updated as date)), max(cast(last_updated as date))
            from weather
        """).fetchone()
    return min_date, max_date

def fetch_weather_data(report_date):
    """Получает данные о погоде для выбранной даты."""
    with duckdb.connect(DB_FILE) as conn:
        weather_df = conn.execute(f"""
            select l.country, w.temperature_celsius, w.humidity, w.wind_kph
            from weather w
            join locations l on w.location_id = l.location_id
            where cast(w.last_updated as date) = '{report_date}'
        """).fetchdf()
    return weather_df

def fetch_air_quality_data(report_date):
    """Получает данные о качестве воздуха для выбранной даты."""
    with duckdb.connect(DB_FILE) as conn:
        air_quality_df = conn.execute(f"""
            select l.country, a."air_quality_pm2_5", a."air_quality_pm10"
            from air_quality a
            join locations l on a.location_id = l.location_id
            where cast(a.last_updated as date) = '{report_date}'
        """).fetchdf()
    return air_quality_df

def fetch_forecast_data():
    """Получает прогноз погоды из weather_forecast."""
    with duckdb.connect(DB_FILE) as conn:
        forecast_df = conn.execute("""
            select l.country, f.forecast_date, f.forecast_temperature, f.forecast_condition
            from weather_forecast f
            join locations l on f.location_id = l.location_id
            where cast(f.forecast_date as date) = '{selected_date}'
            order by f.forecast_date
        """).fetchdf()
    return forecast_df

def fetch_historical_data():
    """Получает исторические данные о погоде."""
    with duckdb.connect(DB_FILE) as conn:
        historical_df = conn.execute("""
            select l.country, h.last_updated, h.temperature_celsius, h.humidity, h.wind_kph
            from historical_data h
            join locations l on h.location_id = l.location_id
            order by h.last_updated
        """).fetchdf()
    return historical_df
