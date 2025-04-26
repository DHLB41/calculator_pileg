import streamlit as st
import pandas as pd

st.set_page_config(page_title="🗳️ Kalkulator Kebutuhan Suara Pemilu 2029", layout="wide")

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

from components import (
    tampilkan_judul_aplikasi,
    tampilkan_formulir_partai,
    tampilkan_tabel_dapil,
    tampilkan_input_target_kursi,
    tampilkan_ringkasan_dapil_terpilih,
    tampilkan_rangkuman_metrik,
    tampilkan_download_section,
    tampilkan_detail_dapil_terpilih,
    tampilkan_hasil_sainte_lague,
    tampilkan_dapil_dieliminasi,
    tampilkan_caleg_terpilih
)
from utils import (
    load_excel_data,
    validate_excel_structure,
    validate_selected_party,
    validate_kursi_target,
    validate_proporsi_input,
    generate_kriteria_1,
    generate_kriteria_2,
    generate_kriteria_3,
    generate_kriteria_4,
    get_all_kriteria_combined,
    hitung_suara_tambahan,
    hitung_total_suara_tambahan,
    hitung_sp,
    hitung_sp_per_kursi,
    hitung_total_rab_all,
    format_ribuan
)

# === HEADER UTAMA ===
tampilkan_judul_aplikasi()

# === LOAD EXCEL DATA ===
df_suara, df_kursi, df_dapil, df_detail_sl = load_excel_data("data_calculated.xlsx")
validate_excel_structure(df_suara, df_kursi, df_dapil)

# === STEP 1: PILIH PARTAI ===
selected_party, votes_2024, seats_2024 = tampilkan_formulir_partai(df_suara, df_kursi)
validate_selected_party(selected_party, df_suara)

# === STEP 2: TABEL SEBARAN DAPIL ===
tampilkan_tabel_dapil(df_dapil, df_suara, df_kursi, selected_party)

# === STEP 3: INPUT TARGET KURSI DAN PROPORSI ===
target_kursi, kursi_input, kehilangan_2024, kehilangan_sp, target_suara_2029 = tampilkan_input_target_kursi()
validate_kursi_target(target_kursi)
validate_proporsi_input(kursi_input)

# === PROSES: SELEKSI DAPIL POTENSIAL ===
df_all_kriteria = get_all_kriteria_combined(df_suara, df_kursi, df_dapil, selected_party)

# === SESSION STATE UNTUK ELIMINASI DAPIL ===
if "eliminated_dapil" not in st.session_state:
    st.session_state.eliminated_dapil = set()
if "alasan_eliminasi" not in st.session_state:
    st.session_state.alasan_eliminasi = {}

# === LOGIKA PEMILIHAN DAPIL TERPILIH ===
def perbarui_df_terpilih(df_all_kriteria, eliminated_dapil, target_kursi):
    df_filtered = df_all_kriteria[~df_all_kriteria["DAPIL"].isin(eliminated_dapil)]
    selected_rows = []
    total_kursi = 0
    for _, row in df_filtered.iterrows():
        if total_kursi >= target_kursi:
            break
        selected_rows.append(row.to_dict())
        total_kursi += row["TARGET_TAMBAHAN_KURSI"]
    return pd.DataFrame(selected_rows)

df_terpilih = perbarui_df_terpilih(df_all_kriteria, st.session_state.eliminated_dapil, target_kursi)

if df_terpilih.empty or "TOTAL_TARGET_SUARA_2029" not in df_terpilih.columns:
    st.error(" Tidak ada DAPIL yang memenuhi kriteria.")
    st.stop()

# === INPUT BIAYA KAMPANYE ===
with st.expander(" Input Estimasi Biaya", expanded=True):
    col1, col2, col3 = st.columns(3)
    angka_psikologis = col1.number_input("Angka Psikologis per Suara", min_value=0, step=1000, value=0, format="%d")
    biaya_manajemen = col2.number_input("Biaya Manajemen per Dapil", min_value=0, step=100000, value=0, format="%d")
    biaya_pendampingan = col3.number_input("Biaya Pendampingan per Dapil", min_value=0, step=100000, value=0, format="%d")

# === HITUNG NILAI-NILAI KEBUTUHAN ===
df_terpilih["TARGET_KEBUTUHAN"] = df_terpilih["TOTAL_TARGET_SUARA_2029"]
df_terpilih["SUARA_TAMBAHAN"] = df_terpilih.apply(hitung_suara_tambahan, axis=1)
df_terpilih["TOTAL_SUARA_TAMBAHAN"] = df_terpilih.apply(lambda row: hitung_total_suara_tambahan(row, kehilangan_2024), axis=1)
df_terpilih["SP"] = df_terpilih.apply(lambda row: hitung_sp(row, kehilangan_sp), axis=1)
df_terpilih[["SP_KURSI_1", "SP_KURSI_2", "SP_KURSI_3", "SP_KURSI_4"]] = df_terpilih.apply(lambda row: hitung_sp_per_kursi(row, kursi_input), axis=1)
df_terpilih["TOTAL_RAB"] = df_terpilih.apply(lambda row: hitung_total_rab_all(row, angka_psikologis, biaya_manajemen, biaya_pendampingan), axis=1)

# === TAMPILKAN RINGKASAN DAPIL POTENSIAL ===
tampilkan_ringkasan_dapil_terpilih(df_terpilih)

# === HALAMAN DETAIL DAPIL ===
if "dapil_page" not in st.session_state:
    st.session_state.dapil_page = 0
st.session_state.total_dapil = len(df_terpilih)
dapil_aktif = df_terpilih.iloc[st.session_state.dapil_page]
tampilkan_detail_dapil_terpilih(dapil_aktif, df_terpilih, angka_psikologis, biaya_manajemen, biaya_pendampingan)

# === DAFTAR DAPIL YANG DIELIMINASI ===
tampilkan_dapil_dieliminasi(df_all_kriteria)

# === SIMULASI SAINTE-LAGUE ===
tampilkan_hasil_sainte_lague(
    dapil_nama=dapil_aktif['DAPIL'],
    alokasi=int(dapil_aktif['ALOKASI_KURSI']),
    df_suara=df_suara,
    partai_lolos=["PKB", "GERINDRA", "PDIP", "GOLKAR", "NASDEM", "PKS", "PAN", "DEMOKRAT"] +
        ([selected_party] if selected_party not in ["PKB", "GERINDRA", "PDIP", "GOLKAR", "NASDEM", "PKS", "PAN", "DEMOKRAT"] else []),
    df_detail_sl=df_detail_sl
)

# === TAMPILKAN DAFTAR CALEG TERPILIH ===
tampilkan_caleg_terpilih(dapil_aktif['DAPIL'], df_detail_sl)

# === METRIK AKHIR & DOWNLOAD HASIL ===
tampilkan_rangkuman_metrik(df_terpilih)
tampilkan_download_section(df_terpilih, df_dapil, selected_party, votes_2024, seats_2024)