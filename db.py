import duckdb
import pandas as pd

DB_FILE = "my.db"

def fetch_date_boundaries():
    """Получаем минимальную и максимальную даты в таблице weather."""
    try:
        with duckdb.connect(DB_FILE) as conn:
            min_date, max_date = conn.execute("""
                select min(cast(last_updated as date)), max(cast(last_updated as date))
                from weather
            """).fetchone()
        return min_date, max_date
    except Exception as e:
        print(f"Ошибка при получении границ дат: {e}")
        return None, None

def fetch_weather_data(report_date):
    """Получаем данные о погоде для выбранной даты."""
    try:
        with duckdb.connect(DB_FILE) as conn:
            weather_df = conn.execute(f"""
                select l.country, w.temperature_celsius, w.humidity, w.wind_kph
                from weather w
                join locations l on w.location_id = l.location_id
                where cast(w.last_updated as date) = '{report_date}'
            """).fetchdf()
        return weather_df if not weather_df.empty else None
    except Exception as e:
        print(f"Ошибка при загрузке погодных данных: {e}")
        return None

def fetch_air_quality_data(report_date):
    """Получаем данные о качестве воздуха для выбранной даты."""
    try:
        with duckdb.connect(DB_FILE) as conn:
            air_quality_df = conn.execute(f"""
                select l.country, a.air_quality_pm2_5, a.air_quality_pm10
                from air_quality a
                join locations l on a.location_id = l.location_id
                where cast(a.last_updated as date) = '{report_date}'
            """).fetchdf()
        return air_quality_df if not air_quality_df.empty else None
    except Exception as e:
        print(f"Ошибка при загрузке данных о качестве воздуха: {e}")
        return None

def fetch_forecast_data(selected_date):
    """Получаем прогноз погоды для выбранной даты."""
    try:
        selected_date = selected_date.strftime("%Y-%m-%d")
        with duckdb.connect(DB_FILE) as conn:
            forecast_df = conn.execute(f"""
                select l.country, f.forecast_date, f.forecast_temperature, f.forecast_condition
                from weather_forecast f
                join locations l on f.location_id = l.location_id
                where cast(f.forecast_date as date) = '{selected_date}'
                order by f.forecast_date
            """).fetchdf()
        return forecast_df if not forecast_df.empty else None
    except Exception as e:
        print(f"Ошибка при загрузке прогноза погоды: {e}")
        return None

def fetch_historical_data(selected_date):
    """Получаем исторические данные о погоде для выбранной даты."""
    try:
        selected_date = selected_date.strftime("%Y-%m-%d")
        with duckdb.connect(DB_FILE) as conn:
            historical_df = conn.execute(f"""
                select l.country, h.last_updated, h.temperature_celsius, h.humidity
                from historical_data h
                join locations l on h.location_id = l.location_id
                where cast(h.last_updated as date) = '{selected_date}'
                order by h.last_updated
            """).fetchdf()
        return historical_df if not historical_df.empty else None
    except Exception as e:
        print(f"Ошибка при загрузке исторических данных: {e}")
        return None

def fetch_central_asia_data(report_date, country="Все"):
    """Получает данные о погоде для стран Центральной Азии."""
    try:
        central_asian_countries = ["Kazakhstan", "Uzbekistan", "Tajikistan", "Kyrgyzstan", "Turkmenistan"]

        query = f"""
            select l.country, w.temperature_celsius, w.humidity, w.wind_kph
            from weather w
            join locations l on w.location_id = l.location_id
            where cast(w.last_updated as date) = '{report_date}'
            and l.country in {tuple(central_asian_countries)}
        """
        if country != "Все":
            query += f" and l.country = '{country}'"

        with duckdb.connect(DB_FILE) as conn:
            weather_df = conn.execute(query).fetchdf()

        return weather_df if not weather_df.empty else pd.DataFrame()
    except Exception as e:
        print(f"Ошибка при загрузке данных о погоде для Центральной Азии: {e}")
        return pd.DataFrame()


def fetch_central_asia_air_quality(report_date, country="Все"):
    """Получает данные о качестве воздуха для стран Центральной Азии."""
    try:
        central_asian_countries = ["Kazakhstan", "Uzbekistan", "Tajikistan", "Kyrgyzstan", "Turkmenistan"]

        query = f"""
            select l.country, a.air_quality_pm2_5, a.air_quality_pm10
            from air_quality a
            join locations l on a.location_id = l.location_id
            where cast(a.last_updated as date) = '{report_date}'
            and l.country in {tuple(central_asian_countries)}
        """
        if country != "Все":
            query += f" and l.country = '{country}'"

        with duckdb.connect(DB_FILE) as conn:
            air_quality_df = conn.execute(query).fetchdf()

        return air_quality_df if not air_quality_df.empty else pd.DataFrame()
    except Exception as e:
        print(f"Ошибка при загрузке качества воздуха для Центральной Азии: {e}")
        return pd.DataFrame()
