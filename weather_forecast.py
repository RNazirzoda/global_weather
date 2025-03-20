import pandas as pd
import plotly.express as px
import streamlit as st
import db  

st.title("Прогноз погоды")
st.write("---")


min_date, max_date = db.fetch_date_boundaries()


with st.sidebar:
    st.write("Основной фильтр")
    selected_date = st.date_input(
        label="Выберите дату прогноза",
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )


forecast_df = db.fetch_forecast_data(selected_date)


if forecast_df is None or forecast_df.empty:
    st.warning("Данные о прогнозе отсутствуют.")
else:
    st.write("### Прогноз температуры по странам")
    
    
    col1, col2 = st.columns(2)
    col1.metric("Макс. температура", round(forecast_df["forecast_temperature"].max(), 2))
    col2.metric("Мин. температура", round(forecast_df["forecast_temperature"].min(), 2))

    
    fig = px.bar(
        forecast_df,
        x="country",
        y="forecast_temperature",
        title="Средняя прогнозируемая температура по странам",
        labels={"forecast_temperature": "Температура (°C)", "country": "Страна"},
        color="forecast_temperature",
        color_continuous_scale="thermal"
    )
    st.plotly_chart(fig)
