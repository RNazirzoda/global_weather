import json
import pandas as pd
import duckdb


DB_FILE = 'my.db'

def create_tables():
    try:
        # читаем содержимое файла 'queries/tables.sql'
        with open('queries/tables.sql') as f:
            tables_query = f.read()
        
        # создаём схему и таблицы
        with duckdb.connect(DB_FILE) as duck:
            duck.execute(tables_query)
        
        print("Tables created successfully")
    except Exception as e:
        print(e)


def read_xl(sheet_name, columns_dict):
    temp_df = pd.read_excel(
        'source/adventure_works.xlsx',
        sheet_name=sheet_name,
        usecols=columns_dict.keys()
    ).rename(columns=columns_dict)
    return temp_df


with open('tables.json') as f:
    tables_dict = json.load(f) 


def insert_to_db(temp_df, tbl_name):
    with duckdb.connect(DB_FILE) as duck:
        duck.execute(f"""
            insert into {tbl_name}
            select * from temp_df
        """)
        # temp_df.to_sql(
        #     schema=SCHEMA,
        #     name=tbl_name,
        #     con=psg,
        #     index=False,
        #     if_exists='append'
        # )


def create_views():
    with open('queries/views.sql') as f:
        views = f.read()

    with duckdb.connect(DB_FILE) as duck:
        duck.execute(views)
        duck.commit()

    print("Views were successfully created")


def xl_etl(sheet_name, columns_dict, tbl_name):
    print(f"inserting data to {tbl_name}...")
    temp_df = read_xl(sheet_name, columns_dict)
    insert_to_db(temp_df, tbl_name)
    


def create_n_insert():    
    try:
        print('try entrypoint')
        with duckdb.connect(DB_FILE) as duck:
            duck.execute("select 1 from sales").fetchone()
    except:
        print('except entrypoint')
        create_tables()
        for k, v in tables_dict.items():
            xl_etl(k, v["columns"], v["table_name"])
        print('data inserted successfully')

        create_views()


create_n_insert()
