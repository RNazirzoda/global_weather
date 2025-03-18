import duckdb
import pandas as pd

DB_FILE = "my.db"

def fetch_date_boundaries():
    try:
        with duckdb.connect(DB_FILE) as conn:
            min_date, max_date = conn.execute("""
                select
                    min(last_updated) as min_date,
                    max(last_updated) as max_date
                from weather
            """).fetchone()
        return min_date, max_date
    except Exception as e:
        print(f"Ошибка при получении временных границ: {e}")
        return None, None

def fetch_weather_data(report_date):
    try:
        with open("queries/weather_data.sql", "r", encoding="utf-8") as f:
            weather_query = f.read().format(report_date=report_date)

        with duckdb.connect(DB_FILE) as conn:
            weather_df = conn.execute(weather_query).fetchdf()
        
        return weather_df
    except fileNotFoundError:
        print("Ошибка: файл queries/weather_data.sql не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при загрузке погодных данных: {e}")
        return None