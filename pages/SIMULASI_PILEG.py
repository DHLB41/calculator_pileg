import streamlit as st
from utils.data_loader import load_excel_data
from components.simulasi_view import tampilkan_simulasi_view
from components.header_section import tampilkan_judul_simulasi

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === HEADER UTAMA ===
tampilkan_judul_simulasi()

# === LOAD DATA ===
df_suara, df_kursi, df_dapil, _ = load_excel_data("data_calculated.xlsx")

# === TAMPILKAN VIEW SIMULASI ===
tampilkan_simulasi_view(df_suara, df_kursi, df_dapil)