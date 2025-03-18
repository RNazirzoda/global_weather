import streamlit as st
from db import fetch_weather_data, fetch_date_boundaries

st.title("Анализ погоды")

min_date, max_date = fetch_date_boundaries()

# выбор даты
selected_date = st.date_input(
    "Выберите дату", 
    value=max_date, 
    min_value=min_date, 
    max_value=max_date
    )

weather_df = fetch_weather_data(selected_date)

if weather_df is not None and not weather_df.empty:
    st.dataframe(weather_df)
else:
    st.warning("Данные за выбранную дату отсутствуют.")