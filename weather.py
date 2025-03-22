import pandas as pd
import plotly.express as px
import streamlit as st
import db

st.title("Анализ погоды")
st.write("---")


min_date, max_date = db.fetch_date_boundaries()


with st.sidebar:
    st.write("---")
    st.write("Основной фильтр")
    selected_date = st.date_input(
        label="Выберите дату",
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )


weather_df = db.fetch_weather_data(selected_date)

if weather_df.empty:
    st.warning("Данные за выбранную дату отсутствуют.")
else:
    st.write("### Средняя температура по странам")

    
    col1, col2 = st.columns(2)
    col1.metric("Макс. температура (°C)", round(float(weather_df["temperature_celsius"].max()), 2))
    col2.metric("Мин. температура (°C)", round(float(weather_df["temperature_celsius"].min()), 2))

    
    avg_temp_fig = px.bar(
        data_frame=weather_df.groupby("country")["temperature_celsius"].mean().reset_index(),
        x="country",
        y="temperature_celsius",
        title="Средняя температура по странам",
        labels={"temperature_celsius": "Температура (°C)", "country": "Страна"},
        color="temperature_celsius",
        color_continuous_scale="blues"
    )
    st.plotly_chart(avg_temp_fig)

    
    temp_hist = px.histogram(
        weather_df,
        x="temperature_celsius",
        title="Распределение температур",
        labels={"temperature_celsius": "Температура (°C)"},
        nbins=20
    )
    st.plotly_chart(temp_hist)
