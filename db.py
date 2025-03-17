import duckdb

DB_FILE = 'my.db'

def fetch_date_boundaries():
    with duckdb.connect(DB_FILE) as duck:
        min_date, max_date = duck.query("""
            select
                min(order_date) as min_date
                , max(order_date) as max_date
            from sales
        """).fetchone() 
        return min_date, max_date


def fetch_customers(edate):
    with open('queries/customers.sql') as f:
        custs_query = f.read().format(report_date = edate)

    with duckdb.connect(DB_FILE) as duck:
        custs_df = duck.query(custs_query).to_df()
        return custs_df