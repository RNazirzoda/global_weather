import pandas as pd
import plotly.express as px
import streamlit as st
import db  # Импортируем наш модуль с функциями работы с базой

st.title("📊 Анализ погоды")
st.write("---")

# Получаем диапазон доступных дат
min_date, max_date = db.fetch_date_boundaries()

# **Фильтр по дате в боковой панели**
with st.sidebar:
    st.write("---")
    st.write("📅 Основной фильтр")
    selected_date = st.date_input(
        label="Выберите дату",
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )

# Получаем данные о погоде по выбранной дате
weather_df = db.fetch_weather_data(selected_date)

if weather_df.empty:
    st.warning("❌ Данные за выбранную дату отсутствуют.")
else:
    st.write("### 🌡 Средняя температура по странам")

    # **Метрики**
    col1, col2 = st.columns(2)
    col1.metric("Макс. температура (°C)", round(weather_df["temperature_celsius"].max(), 2))
    col2.metric("Мин. температура (°C)", round(weather_df["temperature_celsius"].min(), 2))

    # **Столбчатая диаграмма: Средняя температура по странам**
    avg_temp_fig = px.bar(
        data_frame=weather_df.groupby("country")["temperature_celsius"].mean().reset_index(),
        x="country",
        y="temperature_celsius",
        title="🌎 Средняя температура по странам",
        labels={"temperature_celsius": "Температура (°C)", "country": "Страна"},
        color="temperature_celsius",
        color_continuous_scale="blues"
    )
    st.plotly_chart(avg_temp_fig)

    # **Гистограмма: Распределение температур**
    temp_hist = px.histogram(
        weather_df,
        x="temperature_celsius",
        title="📊 Распределение температур",
        labels={"temperature_celsius": "Температура (°C)"},
        nbins=20
    )
    st.plotly_chart(temp_hist)
