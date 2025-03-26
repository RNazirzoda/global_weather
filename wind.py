import pandas as pd
import plotly.express as px
import streamlit as st
import db  

st.title("Анализ скорости ветра")
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
    st.warning("Данные о ветре за выбранную дату отсутствуют.")
else:
    st.write("### Скорость ветра по странам")

    col1, col2 = st.columns(2)
    col1.metric("Макс. скорость ветра (км/ч)", round(float(weather_df["wind_kph"].max()), 2))
    col2.metric("Мин. скорость ветра (км/ч)", round(float(weather_df["wind_kph"].min()), 2))

    wind_fig = px.bar(
        data_frame=weather_df.groupby("country")["wind_kph"].mean().reset_index(),
        x="country",
        y="wind_kph",
        title="Средняя скорость ветра по странам",
        labels={"wind_kph": "Скорость ветра (км/ч)", "country": "Страна"},
        color="wind_kph",
        color_continuous_scale="oranges"
    )
    st.plotly_chart(wind_fig)

    wind_hist = px.histogram(
        weather_df,
        x="wind_kph",
        title="Распределение скорости ветра",
        labels={"wind_kph": "Скорость ветра (км/ч)"},
        nbins=20
    )
    st.plotly_chart(wind_hist)
