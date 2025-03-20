import pandas as pd
import duckdb

DB_FILE = "my.db"

def create_tables():
    
    try:
        with open("queries/schema.sql", "r", encoding="utf-8") as f:
            schema_query = f.read()

        with duckdb.connect(DB_FILE) as conn:
            conn.execute(schema_query)

        print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")

def read_xl(sheet_name, columns_dict):
    
    try:
        temp_df = pd.read_excel(
            "source/extendedglobalweatherdata.xlsx",
            sheet_name=sheet_name,
            usecols=columns_dict.keys()
        ).rename(columns=columns_dict)
        return temp_df
    except Exception as e:
        print(f"Ошибка при чтении {sheet_name}: {e}")
        return None

def insert_to_db(temp_df, tbl_name):
    
    try:
        if temp_df is None or temp_df.empty:
            print(f"Данные для {tbl_name} отсутствуют.")
            return

        print(f"📌 Вставка {len(temp_df)} строк в таблицу {tbl_name}...")
        
        with duckdb.connect(DB_FILE) as conn:
            for _, row in temp_df.iterrows():
                placeholders = ', '.join(['?'] * len(row))
                columns = ', '.join(temp_df.columns)
                query = f"insert into {tbl_name} ({columns}) values ({placeholders})"
                conn.execute(query, tuple(row))

        print(f"Данные вставлены в таблицу {tbl_name}")
    except Exception as e:
        print(f"Ошибка при вставке в {tbl_name}: {e}")

def create_views():
    
    try:
        with open("queries/views.sql", "r", encoding="utf-8") as f:
            views_query = f.read()

        with duckdb.connect(DB_FILE) as conn:
            conn.execute(views_query)

        print("Вьюшки успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании вьюшек: {e}")

def create_n_insert():
    
    try:
        print("Проверка существования таблицы weather...")
        with duckdb.connect(DB_FILE) as conn:
            conn.execute("select 1 from weather").fetchone()
        print("Данные уже загружены, пропускаем этап загрузки.")
    except:
        print("Данные отсутствуют, начинаем загрузку...")
        create_tables()

        tables_dict = {
            "locations": {  
                "columns": {
                    "location_id": "location_id",
                    "country": "country",
                    "location_name": "location_name",
                    "latitude": "latitude",
                    "longitude": "longitude",
                    "timezone": "timezone"
                },
                "table_name": "locations"
            },
            "weather": {  
                "columns": {
                    "weather_id": "weather_id",
                    "location_id": "location_id",
                    "last_updated": "last_updated",
                    "temperature_celsius": "temperature_celsius",
                    "condition_text": "condition_text",
                    "humidity": "humidity",
                    "wind_kph": "wind_kph"
                },
                "table_name": "weather"
            },
            "air_quality": {
                "columns": {
                    "air_quality_id": "air_quality_id",
                    "location_id": "location_id",
                    "last_updated": "last_updated",
                    "air_quality_pm2.5": "air_quality_pm2_5",
                    "air_quality_pm10": "air_quality_pm10"
                },
                "table_name": "air_quality"
            },
            "weather_forecast": {
                "columns": {
                    "forecast_id": "forecast_id",
                    "location_id": "location_id",
                    "forecast_date": "forecast_date",
                    "forecast_temperature": "forecast_temperature",
                    "forecast_condition": "forecast_condition"
                },
                "table_name": "weather_forecast"
            },
            "historical_data": {
                "columns": {
                    "history_id": "history_id",
                    "location_id": "location_id",
                    "last_updated": "last_updated",
                    "temperature_celsius": "temperature_celsius",
                    "condition_text": "condition_text",
                    "humidity": "humidity",
                    "wind_kph": "wind_kph"
                },
                "table_name": "historical_data"
            }
        }

        for sheet, details in tables_dict.items():
            temp_df = read_xl(sheet, details["columns"])
            print(f"📌 Лист {sheet}: загружено {len(temp_df) if temp_df is not None else 0} строк")
            
            insert_to_db(temp_df, details["table_name"])

        print("Все данные успешно загружены!")
        create_views()


create_n_insert()
