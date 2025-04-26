import streamlit as st

def tampilkan_judul_aplikasi():
    """
    Menampilkan header aplikasi utama dengan gaya visual profesional.
    """
    st.markdown("""
        <h1 class='main-title' style='text-align:center; margin-bottom:0.2rem;'>
            Simulasi Perhitungan Kebutuhan Suara Pemilu 2029
        </h1>
        <p style='text-align:center; font-size:16px; color:#555; margin-top:0; max-width:800px; margin-left:auto; margin-right:auto;'>
            Perhitungan interaktif untuk simulasi target kursi dan suara partai pada Pemilu 2029.
        </p>
        <div class='divider'></div>
    """, unsafe_allow_html=True)