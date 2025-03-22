import pandas as pd
import plotly.express as px
import streamlit as st
import db 

st.title("Анализ погоды в Центральной Азии")
st.write("---")

min_date, max_date = db.fetch_date_boundaries()

# Только дата — без выбора отдельной страны
with st.sidebar:
    st.write("### Основной фильтр")
    selected_date = st.date_input(
        label="Выберите дату",
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )

# Получаем данные по всем странам ЦА
weather_df = db.fetch_central_asia_data(selected_date)
air_df = db.fetch_central_asia_air_quality(selected_date)

if weather_df.empty and air_df.empty:
    st.warning(f"Данные по Центральной Азии за {selected_date} отсутствуют.")
else:
    st.subheader(f"Погода в странах Центральной Азии за {selected_date}")
    
    col1, col2 = st.columns(2)
    col1.metric("Макс. температура (°C)", round(float(weather_df["temperature_celsius"].max()), 2))
    col2.metric("Мин. температура (°C)", round(float(weather_df["temperature_celsius"].min()), 2))

    st.plotly_chart(px.bar(
        weather_df,
        x="country", 
        y="temperature_celsius",
        title="Средняя температура (°C)",
        color="temperature_celsius", 
        color_continuous_scale="blues"
    ))

    st.plotly_chart(px.bar(
        weather_df,
        x="country", 
        y="humidity",
        title="Влажность (%) по странам",
        color="humidity", 
        color_continuous_scale="greens"
    ))

    st.plotly_chart(px.bar(
        weather_df,
        x="country", 
        y="wind_kph",
        title="Скорость ветра (км/ч) по странам",
        color="wind_kph", 
        color_continuous_scale="oranges"
    ))

    if not air_df.empty:
        st.subheader("Загрязнение воздуха")
        a1, a2 = st.columns(2)
        a1.metric("Макс. PM2.5", round(float(air_df["air_quality_pm2_5"].max()), 2))
        a2.metric("Мин. PM2.5", round(float(air_df["air_quality_pm2_5"].min()), 2))

        st.plotly_chart(px.bar(
            air_df,
            x="country", 
            y="air_quality_pm2_5",
            title="Уровень PM2.5 по странам", 
            color="air_quality_pm2_5", 
            color_continuous_scale="reds"
        ))

        st.plotly_chart(px.bar(
            air_df,
            x="country", 
            y="air_quality_pm10",
            title="Уровень PM10 по странам", 
            color="air_quality_pm10", 
            color_continuous_scale="purples"
        ))
