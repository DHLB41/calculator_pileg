import streamlit as st

# Hanya satu tema yang digunakan (Terang)
THEME_CSS_PATH = "assets/styles.css"

def init_theme():
    # Tidak lagi menyimpan pilihan tema karena hanya ada satu
    pass

def render_theme_selector():
    # Tidak menampilkan pilihan tema apa pun
    pass

def load_theme_css():
    # Memuat file styles.css saja
    with open(THEME_CSS_PATH) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_theme():
    # Mengembalikan nilai default saja
    return "Terang"