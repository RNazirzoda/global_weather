import streamlit as st
from ddl import create_n_insert

st.set_page_config(layout="wide", page_title="Глобальная погода")

create_n_insert()

st.sidebar.title("Глобальная погода")

page = st.sidebar.selectbox("Выберите страницу:", ["Главная", "Погода", "Качество воздуха"])

if page == "Главная":
    st.title("Добро пожаловать в дашборд 'Глобальная погода'")
    st.markdown("""
    Этот дашборд позволяет анализировать глобальные погодные данные, качество воздуха и климатические изменения.  
    Выберите категорию слева, чтобы увидеть данные.
    """)
elif page == "Погода":
    try:
        exec(open("weather.py").read())
    except FileNotFoundError:
        st.error("Файл weather.py не найден.")
elif page == "🌫️ Качество воздуха":
    try:
        exec(open("air_quality.py").read())
    except FileNotFoundError:
        st.error("Файл air_quality.py не найден.")

st.markdown("**Данные предоставлены на основе глобальных погодных записей.**")