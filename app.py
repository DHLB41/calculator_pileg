# app.py

import streamlit as st
import pandas as pd

# === SETTING AWAL APLIKASI ===
st.set_page_config(page_title="Kalkulator Kebutuhan Suara Pemilu 2029", layout="wide")

# Load custom CSS
with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === IMPORT COMPONENTS ===
from components import (
    tampilkan_judul_aplikasi,
    tampilkan_formulir_partai,
    tampilkan_tabel_dapil,
    tampilkan_input_target_kursi,
    tampilkan_ringkasan_dapil_terpilih,
    tampilkan_rangkuman_metrik,
    tampilkan_download_section,
    tampilkan_detail_dapil_terpilih,
    tampilkan_dapil_dieliminasi,
    tampilkan_hasil_sainte_lague,
    tampilkan_caleg_terpilih
)

# === IMPORT UTILS ===
from utils import (
    load_excel_data,
    validate_excel_structure,
    validate_selected_party,
    validate_kursi_target,
    validate_proporsi_input,
    format_ribuan
)

from utils.calculations import (
    get_all_kriteria_combined,
    proses_perhitungan_sp,
    proses_perhitungan_rab,
    filter_dapil_terpilih
)

# === HEADER UTAMA ===
tampilkan_judul_aplikasi()

# === LOAD DATA EXCEL ===
df_suara, df_kursi, df_dapil, df_detail_sl = load_excel_data("data_calculated.xlsx")
validate_excel_structure(df_suara, df_kursi, df_dapil)

# === STEP 1: PILIH PARTAI ===
selected_party, votes_2024, seats_2024 = tampilkan_formulir_partai(df_suara, df_kursi)
validate_selected_party(selected_party, df_suara)

# === STEP 2: TABEL SEBARAN DAPIL ===
tampilkan_tabel_dapil(df_dapil, df_suara, df_kursi, selected_party)

# === STEP 3: INPUT TARGET KURSI & PROPORSI ===
target_kursi, kursi_input, kehilangan_2024, kehilangan_sp, target_suara_2029 = tampilkan_input_target_kursi()
validate_kursi_target(target_kursi)
validate_proporsi_input(kursi_input)

# === PROSES: KALKULASI DAPIL ===
df_all_kriteria = get_all_kriteria_combined(df_suara, df_kursi, df_dapil, selected_party)

# === PROSES SP & TARGET SUARA ===
df_all_kriteria = proses_perhitungan_sp(
    df_all_kriteria,
    kehilangan_2024,
    kehilangan_sp,
    kursi_input,
    target_suara_2029
)

# === SELEKSI DAPIL TERPILIH BERDASARKAN TARGET KURSI ===
df_terpilih = filter_dapil_terpilih(df_all_kriteria, target_kursi)

if df_terpilih.empty:
    st.error("Tidak ada DAPIL yang memenuhi kriteria seleksi.")
    st.stop()

# === SORTIR DAPIL TERPILIH BERDASARKAN TARGET SUARA 2029 TERENDAH ===
df_terpilih = df_terpilih.sort_values(by="TARGET_SUARA_2029", ascending=True).reset_index(drop=True)

# === INPUT ESTIMASI BIAYA ===
with st.expander("Input Estimasi Biaya Kampanye", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        angka_psikologis = st.number_input(
            "Angka Psikologis per Suara",
            min_value=0,
            step=1000,
            value=0,
            format="%d"
        )
    with col2:
        biaya_pendampingan = st.number_input(
            "Biaya Pendampingan per Dapil",
            min_value=0,
            step=100000,
            value=0,
            format="%d"
        )

# === HITUNG RAB ===
if not df_terpilih.empty:
    rata_rab_sp = int(df_terpilih["SP"].mean() * angka_psikologis)
    biaya_manajemen = rata_rab_sp // 3
else:
    biaya_manajemen = 0

df_terpilih = proses_perhitungan_rab(
    df_terpilih,
    angka_psikologis,
    biaya_pendampingan
)

# === TAMPILKAN RINGKASAN SEBARAN ===
tampilkan_ringkasan_dapil_terpilih(df_terpilih, angka_psikologis, biaya_pendampingan)

# === DETAIL DAPIL ===
if "dapil_page" not in st.session_state:
    st.session_state.dapil_page = 0
st.session_state.total_dapil = len(df_terpilih)

dapil_aktif = df_terpilih.iloc[st.session_state.dapil_page]

tampilkan_detail_dapil_terpilih(
    dapil_aktif,
    df_terpilih,
    angka_psikologis,
    biaya_manajemen,
    biaya_pendampingan
)

# === DAPIL YANG DIELIMINASI ===
tampilkan_dapil_dieliminasi(df_all_kriteria)

# === SAINTE-LAGUE ===
tampilkan_hasil_sainte_lague(
    dapil_nama=dapil_aktif['DAPIL'],
    alokasi=int(dapil_aktif['ALOKASI_KURSI']),
    df_suara=df_suara,
    partai_lolos=[
        "PKB", "GERINDRA", "PDIP", "GOLKAR",
        "NASDEM", "PKS", "PAN", "DEMOKRAT"
    ] + ([selected_party] if selected_party not in [
        "PKB", "GERINDRA", "PDIP", "GOLKAR",
        "NASDEM", "PKS", "PAN", "DEMOKRAT"
    ] else []),
    df_detail_sl=df_detail_sl
)

# === CALEG TERPILIH ===
tampilkan_caleg_terpilih(dapil_aktif['DAPIL'], df_detail_sl)

# === RANGKUMAN & UNDUHAN ===
tampilkan_rangkuman_metrik(df_terpilih)
tampilkan_download_section(df_terpilih, df_dapil, selected_party, votes_2024, seats_2024)
