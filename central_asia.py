import pandas as pd
import plotly.express as px
import streamlit as st
import db 

st.title("Анализ погоды в Центральной Азии")
st.write("---")

min_date, max_date = db.fetch_date_boundaries()

# **Фильтр по дате и стране в боковой панели**
with st.sidebar:
    st.write("📅 Основной фильтр")
    selected_date = st.date_input(
        label="Выберите дату",
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )

    # **Выбор страны**
    country_options = ["Все"] + ["Kazakhstan", "Uzbekistan", "Tajikistan", "Kyrgyzstan", "Turkmenistan"]
    selected_country = st.selectbox("Выберите страну", country_options)

#Получаем данные по погоде и качеству воздуха
central_asia_weather = db.fetch_central_asia_data(selected_date, selected_country)
central_asia_air_quality = db.fetch_central_asia_air_quality(selected_date, selected_country)

if central_asia_weather.empty and central_asia_air_quality.empty:
    st.warning(f"Данные по {selected_country} за {selected_date} отсутствуют.")
else:
    st.write(f"###Погодные данные по {selected_country} за {selected_date}")

    # **Метрики температуры**
    col1, col2 = st.columns(2)
    col1.metric("Макс. температура (°C)", round(float(central_asia_weather["temperature_celsius"].max()), 2))
    col2.metric("Мин. температура (°C)", round(float(central_asia_weather["temperature_celsius"].min()), 2))

    # **Столбчатая диаграмма температуры по странам**
    temp_fig = px.bar(
        data_frame=central_asia_weather,
        x="country",
        y="temperature_celsius",
        title="Температура по странам Центральной Азии",
        labels={"temperature_celsius": "Температура (°C)", "country": "Страна"},
        color="temperature_celsius",
        color_continuous_scale="blues"
    )
    st.plotly_chart(temp_fig)

    # **Диаграмма влажности**
    humidity_fig = px.bar(
        data_frame=central_asia_weather,
        x="country",
        y="humidity",
        title="Влажность по странам Центральной Азии",
        labels={"humidity": "Влажность (%)", "country": "Страна"},
        color="humidity",
        color_continuous_scale="greens"
    )
    st.plotly_chart(humidity_fig)

    # **Скорость ветра**
    wind_fig = px.bar(
        data_frame=central_asia_weather,
        x="country",
        y="wind_kph",
        title="Скорость ветра по странам Центральной Азии",
        labels={"wind_kph": "Скорость ветра (км/ч)", "country": "Страна"},
        color="wind_kph",
        color_continuous_scale="oranges"
    )
    st.plotly_chart(wind_fig)

    # **Анализ качества воздуха**
    if not central_asia_air_quality.empty:
        st.write(f"###Загрязнение воздуха в {selected_country}")

        # **Метрики загрязнения**
        aq_col1, aq_col2 = st.columns(2)
        aq_col1.metric("Макс. PM2.5", round(float(central_asia_air_quality["air_quality_pm2_5"].max()), 2))
        aq_col2.metric("Мин. PM2.5", round(float(central_asia_air_quality["air_quality_pm2_5"].min()), 2))

        # **Столбчатая диаграмма PM2.5**
        pm2_fig = px.bar(
            data_frame=central_asia_air_quality,
            x="country",
            y="air_quality_pm2_5",
            title="Средний уровень PM2.5 по странам Центральной Азии",
            labels={"air_quality_pm2_5": "PM2.5", "country": "Страна"},
            color="air_quality_pm2_5",
            color_continuous_scale="reds"
        )
        st.plotly_chart(pm2_fig)

        # **Столбчатая диаграмма PM10**
        pm10_fig = px.bar(
            data_frame=central_asia_air_quality,
            x="country",
            y="air_quality_pm10",
            title="Средний уровень PM10 по странам Центральной Азии",
            labels={"air_quality_pm10": "PM10", "country": "Страна"},
            color="air_quality_pm10",
            color_continuous_scale="purples"
        )
        st.plotly_chart(pm10_fig)
