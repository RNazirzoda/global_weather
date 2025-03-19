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
            select l.country, a."air_quality_pm2.5", a."air_quality_pm10"
            from air_quality a
            join locations l on a.location_id = l.location_id
            where cast(a.last_updated as date) = '{report_date}'
        """).fetchdf()
    return air_quality_df
