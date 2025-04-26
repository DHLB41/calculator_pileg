import streamlit as st
from utils.sainte_lague import hitung_detail_kursi
from utils.formatters import format_ribuan
import pandas as pd


def tampilkan_hasil_sainte_lague(dapil_nama, alokasi, df_suara, partai_lolos, df_detail_sl=None):
    """
    Menampilkan hasil simulasi Sainte-Laguë dalam format tabel elegan.
    """
    with st.expander(f"Hasil Sainte-Laguë – {dapil_nama}", expanded=False):
        st.markdown(f"<div class='badge'>Sainte-Laguë - Alokasi {alokasi} Kursi</div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

        df_hasil = hitung_detail_kursi(
            dapil_nama=dapil_nama,
            alokasi_kursi=alokasi,
            df_suara=df_suara,
            partai_lolos=partai_lolos,
            df_detail_sl=df_detail_sl
        )

        if df_hasil.empty:
            st.warning("Data hasil Sainte-Laguë kosong.")
            return

        # Format angka & kolom
        df_display = df_hasil.copy()
        df_display["PEROLEHAN SUARA"] = df_display["PEROLEHAN SUARA"].apply(format_ribuan)
        df_display["NILAI BAGI"] = df_display["NILAI BAGI"].apply(lambda x: f"{x:,.2f}")
        if "URUTAN KURSI" in df_display.columns:
            df_display["URUTAN KURSI"] = df_display["URUTAN KURSI"].apply(
                lambda x: str(int(x)) if pd.notna(x) and x != "" else ""
            )

        # Pilih kolom tampil
        kolom_tampil = ["DAPIL", "URUTAN KURSI", "PARTAI", "PEMBAGI", "PEROLEHAN SUARA", "NILAI BAGI"]
        df_display = df_display[kolom_tampil]

        # Tampilkan tabel
        st.markdown(f'<div class="scrollable-table">{df_display.to_html(index=False, classes="centered-table", escape=False)}</div>', unsafe_allow_html=True)
        st.caption("*Partai yang mendapatkan kursi akan memiliki angka pada kolom 'Urutan Kursi'*")


def tampilkan_caleg_terpilih(dapil_nama: str, df_detail_sl: pd.DataFrame):
    """
    Menampilkan daftar caleg terpilih untuk Dapil aktif.
    """
    with st.expander(f"Daftar Caleg Terpilih – {dapil_nama}", expanded=False):
        if df_detail_sl is None or df_detail_sl.empty:
            st.info("Data caleg belum tersedia.")
            return

        df_detail = df_detail_sl.copy()
        df_detail.columns = df_detail.columns.str.strip().str.upper().str.replace("–", "-")
        df_detail.rename(columns={"KURSI KE": "URUTAN KURSI", "KURSI KE-": "URUTAN KURSI"}, inplace=True)

        kolom_diperlukan = ["DAPIL", "URUTAN KURSI", "PARTAI", "NAMA CALEG", "NOMOR URUT DALAM DCT", "PEROLEHAN SUARA CALEG"]
        if not all(col in df_detail.columns for col in kolom_diperlukan):
            st.warning("Struktur kolom pada sheet 'detail_sl' tidak sesuai.")
            return

        df_filtered = df_detail[df_detail["DAPIL"] == dapil_nama][kolom_diperlukan].copy()
        if df_filtered.empty:
            st.info(f"Tidak ada data caleg untuk dapil {dapil_nama}")
            return

        df_filtered["PEROLEHAN SUARA CALEG"] = df_filtered["PEROLEHAN SUARA CALEG"].apply(format_ribuan)

        # Tampilkan tabel
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("<div class='badge success'>Caleg Terpilih</div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
        st.markdown(f'<div class="scrollable-table">{df_filtered.to_html(index=False, classes="centered-table", escape=False)}</div>', unsafe_allow_html=True)
        st.caption(f"*Tabel ini hanya menampilkan caleg yang mendapatkan kursi di dapil {dapil_nama}*")