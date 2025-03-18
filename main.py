import streamlit as st
from ddl import create_n_insert

create_n_insert()

st.title("Добро пожаловать в дашборд 'Глобальная погода'")

st.markdown("""
Этот дашборд позволяет анализировать глобальные погодные данные, качество воздуха и климатические изменения.  
Выберите категорию слева, чтобы увидеть данные.
""")

st.set_page_config(layout="wide", page_title="Глобальная погода")

st.sidebar.title("Глобальная погода")

weather_page = st.Page(
    "pages/weather.py",
    title="Погода",
    default=True
)

air_quality_page = st.Page(
    "pages/air_quality.py",
    title="Качество воздуха"
)

pgs = st.navigation([weather_page, air_quality_page])

pgs.run()

#st.markdown("**Данные предоставлены на основе глобальных погодных записей.**")