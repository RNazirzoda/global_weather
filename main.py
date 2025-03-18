import streamlit as st
import importlib.util
from ddl import create_n_insert

st.set_page_config(layout="wide", page_title="Глобальная погода")

create_n_insert()

st.sidebar.title("Глобальная погода")

page = st.sidebar.selectbox("Выберите страницу:", ["Главная", "Погода", "Качество воздуха"])

def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except FileNotFoundError:
        st.error(f"Файл {file_path} не найден.")

if page == "Главная":
    st.title("Добро пожаловать в дашборд 'Глобальная погода'")
    st.markdown("""
    Этот дашборд позволяет анализировать глобальные погодные данные, качество воздуха и климатические изменения.  
    Выберите категорию слева, чтобы увидеть данные.
    """)
elif page == "Погода":
    load_module("weather", "weather.py")
elif page == "Качество воздуха":
    load_module("air_quality", "air_quality.py")

st.markdown("**Данные предоставлены на основе глобальных погодных записей.**")