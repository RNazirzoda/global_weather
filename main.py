import streamlit as st
from ddl import create_n_insert

# Устанавливаем конфигурацию страницы
st.set_page_config(layout="wide", page_title="Глобальная погода")

# Загружаем данные в базу перед запуском дашборда
create_n_insert()

# Боковая панель навигации
st.sidebar.title("🌍 Глобальная погода")

# Выпадающий список для навигации
page = st.sidebar.selectbox("Выберите страницу:", ["Главная", "📊 Погода", "🌫️ Качество воздуха"])

# Отображаем выбранную страницу
if page == "Главная":
    st.title("Добро пожаловать в дашборд 'Глобальная погода' 🌎")
    st.markdown("""
    Этот дашборд позволяет анализировать глобальные погодные данные, качество воздуха и климатические изменения.  
    Выберите категорию слева, чтобы увидеть данные.
    """)
elif page == "📊 Погода":
    try:
        exec(open("weather.py").read())  # Загружаем weather.py
    except FileNotFoundError:
        st.error("Файл weather.py не найден.")
elif page == "🌫️ Качество воздуха":
    try:
        exec(open("air_quality.py").read())  # Загружаем air_quality.py
    except FileNotFoundError:
        st.error("Файл air_quality.py не найден.")

# Нижний колонтитул
st.markdown("📊 **Данные предоставлены на основе глобальных погодных записей.**")