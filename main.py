import streamlit as st
from ddl import create_n_insert
from streamlit_extras.switch_page_button import switch_page

create_n_insert()

st.set_page_config(
    layout="wide", 
    page_title="Глобальная погода"
    )

st.sidebar.title("Глобальная погода")

if st.sidebar.button("Погода"):
    switch_page("weather")

if st.sidebar.button("Качество воздуха"):
    switch_page("air_quality")

st.title("Добро пожаловать в дашборд 'Глобальная погода'")
st.markdown("""
Этот дашборд позволяет анализировать глобальные погодные данные, качество воздуха и климатические изменения.  
Выберите категорию слева, чтобы увидеть данные.
""")

#st.markdown("📊 **Данные предоставлены на основе глобальных погодных записей.**")