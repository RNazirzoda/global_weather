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

        with duckdb.connect(DB_FILE) as conn:
            conn.execute(f"insert into {tbl_name} select * from temp_df")

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

def xl_etl(sheet_name, columns_dict, tbl_name):
    
    print(f"🔄 загрузка данных в {tbl_name}...")
    temp_df = read_xl(sheet_name, columns_dict)
    insert_to_db(temp_df, tbl_name)

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
            "Locations": {  
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
            "Weather": {  
                "columns": {
                    "weather_id": "weather_id",
                    "location_id": "location_id",
                    "last_updated": "last_updated",
                    "temperature_celsius": "temperature_celsius",
                    "humidity": "humidity",
                    "wind_kph": "wind_kph"
                },
                "table_name": "weather"
            },
            "AirQuality": {
                "columns": {
                    "air_quality_id": "air_quality_id",
                    "location_id": "location_id",
                    "air_quality_pm2.5": "air_quality_pm2_5",
                    "air_quality_pm10": "air_quality_pm10"
                },
                "table_name": "air_quality"
            }
        }

        for sheet, details in tables_dict.items():
            xl_etl(sheet, details["columns"], details["table_name"])

        print("Все данные успешно загружены!")

        create_views()


create_n_insert()
