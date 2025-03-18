import streamlit as st
from db import get_air_quality_summary

st.title("Качество воздуха")

air_quality_df = get_air_quality_summary()

if air_quality_df is not None and not air_quality_df.empty:
    st.dataframe(air_quality_df)
else:
    st.warning("Данные о качестве воздуха отсутствуют.")