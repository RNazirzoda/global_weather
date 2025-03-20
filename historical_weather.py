import pandas as pd
import plotly.express as px
import streamlit as st
import db 

st.title("Исторические данные о погоде")
st.write("---")

historical_df = db.fetch_historical_data()

if historical_df.empty:
    st.warning("Данные отсутствуют.")
else:
    st.write("###Тренд средней температуры")

    trend_fig = px.line(
        historical_df,
        x="last_updated",
        y="temperature_celsius",
        color="country",
        title="Средняя температура по времени",
        labels={"temperature_celsius": "Температура (°C)", "last_updated": "Дата"},
    )
    st.plotly_chart(trend_fig)

    st.write("###Средняя скорость ветра по странам")

    wind_speed_fig = px.bar(
        data_frame=historical_df.groupby("country")["wind_kph"].mean().reset_index(),
        x="country",
        y="wind_kph",
        title="Средняя скорость ветра по странам",
        labels={"wind_kph": "Скорость ветра (км/ч)", "country": "Страна"},
        color="wind_kph",
        color_continuous_scale="blues"
    )
    st.plotly_chart(wind_speed_fig)
