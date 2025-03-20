import pandas as pd
import plotly.express as px
import streamlit as st
import db 

st.title("Прогноз погоды")
st.write("---")

forecast_df = db.fetch_forecast_data()

if forecast_df.empty:
    st.warning("Данные о прогнозе отсутствуют.")
else:
    st.write("### Средняя прогнозируемая температура по странам")

    forecast_fig = px.line(
        forecast_df,
        x="forecast_date",
        y="forecast_temperature",
        color="country",
        title="Прогноз температуры по странам",
        labels={"forecast_temperature": "Температура (°C)", "forecast_date": "Дата"},
    )
    st.plotly_chart(forecast_fig)
