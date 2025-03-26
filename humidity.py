import pandas as pd
import plotly.express as px
import streamlit as st
import db



st.title("Анализ влажности воздуха")
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

if weather_df is None or weather_df.empty:
    st.warning("Данные о влажности за выбранную дату отсутствуют.")
else:
    st.write("### Влажность по странам")

    col1, col2 = st.columns(2)
    col1.metric("Макс. влажность (%)", round(float(weather_df["humidity"].max()), 2))
    col2.metric("Мин. влажность (%)", round(float(weather_df["humidity"].min()), 2))

    humidity_fig = px.bar(
        data_frame=weather_df.groupby("country")["humidity"].mean().reset_index(),
        x="country",
        y="humidity",
        title="Средняя влажность по странам",
        labels={"humidity": "Влажность (%)", "country": "Страна"},
        color="humidity",
        color_continuous_scale="greens"
    )
    st.plotly_chart(humidity_fig)

    humidity_hist = px.histogram(
        weather_df,
        x="humidity",
        title="Распределение влажности",
        labels={"humidity": "Влажность (%)"},
        nbins=20
    )
    st.plotly_chart(humidity_hist)