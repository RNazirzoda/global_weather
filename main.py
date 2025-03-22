import streamlit as st
import importlib.util
from ddl import create_n_insert

st.set_page_config(layout="wide", page_title="Глобальная погода")

create_n_insert()

st.sidebar.title("Глобальная погода")

#Выбор страницы
page = st.sidebar.selectbox(
    "Выберите страницу:",
    [
        "Главная", 
        "Погода", 
        "Качество воздуха", 
        "Прогноз погоды", 
        "Центральная Азия"
    ]
)

def load_module(module_name, file_path):
    """Функция загрузки модулей с обработкой ошибок"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except FileNotFoundError:
        st.error(f"Ошибка: файл `{file_path}` не найден.")
    except Exception as e:
        st.error(f"Ошибка при загрузке `{module_name}`: {e}")

#Обработка выбора страницы
if page == "Главная":
    st.title("Добро пожаловать в дашборд 'Глобальная погода'!")
    st.markdown("""
    Этот дашборд позволяет анализировать глобальные погодные данные, прогнозы, качество воздуха и исторические климатические изменения.  
    Выберите категорию слева, чтобы увидеть данные.
    """)

elif page == "Погода":
    load_module("weather", "weather.py")

elif page == "Качество воздуха":
    load_module("air_quality", "air_quality.py")

elif page == "Прогноз погоды":
    load_module("weather_forecast", "weather_forecast.py")

elif page == "Центральная Азия":
    load_module("central_asia", "central_asia.py")

st.markdown("**Данные предоставлены на основе глобальных погодных записей.**")
