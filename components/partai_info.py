import streamlit as st
from utils import get_total_suara, get_total_kursi, format_ribuan

def tampilkan_formulir_partai(df_suara, df_kursi):
    """
    UI bagian 1: Pemilihan partai & informasi suara/kursi Pemilu 2024.
    """

    # === HEADER ===
    st.markdown("""
        <div class='section-header'>
            <h2 class='section-heading'>1. Data Umum Partai</h2> 
            <span class='badge'>Pemilu 2024</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

    # === PILIH PARTAI ===
    partai_list = df_suara.columns[1:].tolist()
    selected_party = st.selectbox("🗳️ Pilih Partai", partai_list)

    # === AMBIL DATA SUARA DAN KURSI ===
    votes_2024 = get_total_suara(df_suara, selected_party)
    seats_2024 = get_total_kursi(df_kursi, selected_party)

    # === TAMPILKAN DATA ===
    col1, col2 = st.columns(2)
    with col1:
        st.text_input(
            label="🔢 Perolehan Suara Pemilu 2024",
            value=format_ribuan(votes_2024),
            disabled=True
        )
    with col2:
        st.text_input(
            label="🎯 Perolehan Kursi Pemilu 2024",
            value=format_ribuan(seats_2024),
            disabled=True
        )

    # === DIVIDER ===
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    return selected_party, votes_2024, seats_2024