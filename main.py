import streamlit as st
from ddl import create_n_insert

create_n_insert()

st.set_page_config(layout='wide')

st.sidebar.title('Adventure Works')

custs_page = st.Page(
    'customers.py',
    title='Customers',
    default=True
)

sales_page = st.Page(
    'sales.py',
    title='Sales'
)

pgs = st.navigation([custs_page, sales_page])

pgs.run()