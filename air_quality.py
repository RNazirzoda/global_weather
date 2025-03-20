import pandas as pd
import plotly.express as px
import streamlit as st
import db  

st.title("🌍 Анализ качества воздуха")
st.write("---")


min_date, max_date = db.fetch_date_boundaries()


with st.sidebar:
    st.write("---")
    st.write("📅 Основной фильтр")
    selected_date = st.date_input(
        label="Выберите дату",
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )


air_quality_df = db.fetch_air_quality_data(selected_date)

if air_quality_df.empty:
    st.warning("❌ Данные за выбранную дату отсутствуют.")
else:
    st.write("### 🌍 Загрязнение воздуха (PM2.5) по странам")

    
    col1, col2 = st.columns(2)
    col1.metric("Макс. PM2.5", round(air_quality_df["air_quality_pm2_5"].max(), 2))
    col2.metric("Мин. PM2.5", round(air_quality_df["air_quality_pm2_5"].min(), 2))

    
    air_quality_fig = px.bar(
        data_frame=air_quality_df.groupby("country")["air_quality_pm2_5"].mean().reset_index(),
        x="country",
        y="air_quality_pm2_5",
        title="🌎 Средний уровень PM2.5 по странам",
        labels={"air_quality_pm2_5": "PM2.5", "country": "Страна"},
        color="air_quality_pm2_5",
        color_continuous_scale="reds"
    )
    st.plotly_chart(air_quality_fig)

    
    pm2_hist = px.histogram(
        air_quality_df,
        x="air_quality_pm2_5",
        title="📊 Распределение PM2.5",
        labels={"air_quality_pm2_5": "PM2.5"},
        nbins=20
    )
    st.plotly_chart(pm2_hist)
