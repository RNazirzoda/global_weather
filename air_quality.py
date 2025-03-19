import streamlit as st
import pandas as pd
import duckdb
import matplotlib.pyplot as plt
import seaborn as sns

db_file = "my.db"

st.title("🌍 Анализ качества воздуха")

# Выбор даты пользователем
selected_date = st.date_input("📅 Выберите дату", value=pd.to_datetime("2025-03-06"))
selected_date_str = selected_date.strftime('%Y-%m-%d')  # Преобразуем в строку

with duckdb.connect(db_file) as conn:
    df_air = conn.execute(f"""
        select l.country, avg(a."air_quality_pm2.5") as avg_pm2_5
        from air_quality a
        join locations l on a.location_id = l.location_id
        where cast(a.last_updated as date) = '{selected_date_str}'
        group by l.country
        order by avg_pm2_5 desc
        limit 10
    """).fetchdf()

if df_air.empty:
    st.warning("❌ Нет данных для выбранной даты.")
else:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=df_air["country"], y=df_air["avg_pm2_5"], ax=ax, palette="magma")
    ax.set_title(f"🌍 Загрязнение воздуха (PM2.5) по странам ({selected_date_str})")
    ax.set_xlabel("Страна")
    ax.set_ylabel("Средний PM2.5")
    plt.xticks(rotation=45)
    st.pyplot(fig)
