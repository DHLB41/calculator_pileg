import pandas as pd
import streamlit as st

def validate_excel_structure(df_suara, df_kursi, df_dapil):
    """
    Validasi struktur dasar file Excel (sheet & kolom utama).
    """
    required_sheets = [df_suara, df_kursi, df_dapil]
    required_columns = ["DAPIL"]

    for df, name in zip(required_sheets, ["perolehan_suara", "hasil_sl", "dapil"]):
        if df.empty:
            st.error(f"Sheet '{name}' kosong atau tidak terbaca.")
            st.stop()
        for col in required_columns:
            if col not in df.columns:
                st.error(f"Sheet '{name}' tidak memiliki kolom wajib: '{col}'")
                st.stop()


def validate_selected_party(selected_party, df_suara):
    """
    Validasi apakah partai yang dipilih ada di kolom df_suara.
    """
    if selected_party not in df_suara.columns:
        st.error(f"Partai '{selected_party}' tidak ditemukan dalam data suara.")
        st.stop()


def validate_kursi_target(target_kursi):
    """
    Validasi apakah target kursi lebih dari 0.
    """
    if target_kursi <= 0:
        st.error("Target perolehan kursi harus lebih dari 0.")
        st.stop()


def validate_proporsi_input(proporsi_dict):
    """
    Validasi nilai proporsi kursi per dapil (tiap kombinasi proporsi).
    Total tiap kombinasi kursi (2,3,4) sebaiknya 100%.
    """
    for jumlah_kursi in [2, 3, 4]:
        total = sum([v for k, v in proporsi_dict.items() if f"proporsi_{jumlah_kursi}_" in k])
        if total > 0 and (total < 95 or total > 105):
            st.warning(f"Total proporsi untuk kursi ke-{jumlah_kursi} tidak mendekati 100%. Saat ini: {total:.2f}%")
