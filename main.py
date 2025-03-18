import streamlit as st
from ddl import create_n_insert

create_n_insert()

st.set_page_config(layout="wide", page_title="Глобальная погода")

st.sidebar.title("Глобальная погода")

st.sidebar.page_link("pages/weather", label="Погода")
st.sidebar.page_link("pages/air_quality", label="Качество воздуха")

st.title("Добро пожаловать в дашборд 'Глобальная погода'")
st.markdown("""
Этот дашборд позволяет анализировать глобальные погодные данные, качество воздуха и климатические изменения.  
Выберите категорию слева, чтобы увидеть данные.
""")

#st.markdown("**Данные предоставлены на основе глобальных погодных записей.**")