import pandas as pd
import duckdb

db_file = "my.db"

def create_tables():
    """создание таблиц на основе schema.sql"""
    try:
        with open("queries/schema.sql", "r", encoding="utf-8") as f:
            schema_query = f.read()

        with duckdb.connect(db_file) as conn:
            conn.execute(schema_query)

        print("✅ таблицы успешно созданы!")
    except Exception as e:
        print(f"❌ ошибка при создании таблиц: {e}")

def read_xl(sheet_name, columns_dict):
    """чтение данных из excel"""
    try:
        temp_df = pd.read_excel(
            "source/extendedglobalweatherdata.xlsx",
            sheet_name=sheet_name,
            usecols=columns_dict.keys()
        ).rename(columns=columns_dict)
        return temp_df
    except Exception as e:
        print(f"❌ ошибка при чтении {sheet_name}: {e}")
        return None

def insert_to_db(temp_df, tbl_name):
    """вставка данных в таблицу duckdb"""
    try:
        if temp_df is None or temp_df.empty:
            print(f"⚠ данные для {tbl_name} отсутствуют.")
            return

        with duckdb.connect(db_file) as conn:
            for _, row in temp_df.iterrows():
                placeholders = ', '.join(['?'] * len(row))
                columns = ', '.join(temp_df.columns)
                query = f"insert into {tbl_name} ({columns}) values ({placeholders})"
                conn.execute(query, tuple(row))

        print(f"✅ данные вставлены в таблицу {tbl_name}")
    except Exception as e:
        print(f"❌ ошибка при вставке в {tbl_name}: {e}")

def create_views():
    """создание вьюшек на основе views.sql"""
    try:
        with open("queries/views.sql", "r", encoding="utf-8") as f:
            views_query = f.read()

        with duckdb.connect(db_file) as conn:
            conn.execute(views_query)

        print("✅ вьюшки успешно созданы!")
    except Exception as e:
        print(f"❌ ошибка при создании вьюшек: {e}")

def create_n_insert():
    """основная функция: проверка данных, создание таблиц, загрузка данных"""
    try:
        print("📌 проверка существования таблицы weather...")
        with duckdb.connect(db_file) as conn:
            conn.execute("select 1 from weather").fetchone()
        print("✅ данные уже загружены, пропускаем этап загрузки.")
    except:
        print("⚠ данные отсутствуют, начинаем загрузку...")
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
            }
        }

        for sheet, details in tables_dict.items():
            temp_df = read_xl(sheet, details["columns"])
            insert_to_db(temp_df, details["table_name"])

        print("✅ все данные успешно загружены!")
        create_views()

# запускаем процесс загрузки данных
create_n_insert()
