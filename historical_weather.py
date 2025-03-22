import pandas as pd
import plotly.express as px
import streamlit as st
import db  

st.title("Исторические погодные данные")
st.write("---")


historical_df = db.fetch_historical_data()


if historical_df is None or historical_df.empty:
    st.warning("Исторические данные о погоде отсутствуют.")
else:
    st.write("### Историческая температура по странам")

    
    col1, col2 = st.columns(2)
    col1.metric("Макс. температура", round(float(historical_df["temperature_celsius"].max()), 2))
    col2.metric("Мин. температура", round(float(historical_df["temperature_celsius"].min()), 2))

    
    fig = px.line(
        historical_df,
        x="last_updated",
        y="temperature_celsius",
        color="country",
        title="Исторические изменения температуры",
        labels={"temperature_celsius": "Температура (°C)", "last_updated": "Дата"},
    )
    st.plotly_chart(fig)
