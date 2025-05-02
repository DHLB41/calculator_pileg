import streamlit as st
from utils.formatters import format_ribuan
from utils.calculations.rab_calculator import proses_perhitungan_rab

def tampilkan_ringkasan_dapil_terpilih(df_terpilih, angka_psikologis, biaya_pendampingan):
    """
    Menampilkan tabel rekap dapil terpilih dari hasil seleksi kriteria.
    Kolom Total RAB akan diperbarui berdasarkan angka psikologis terkini.
    """

    if df_terpilih.empty:
        st.markdown("<div class='empty-state'>Tidak ada DAPIL yang memenuhi kriteria seleksi.</div>", unsafe_allow_html=True)
        return

    # === HITUNG ULANG TOTAL RAB TERKINI ===
    angka_psikologis_dapil = st.session_state.get("angka_psikologis_dapil", {})
    df_rab = proses_perhitungan_rab(
        df=df_terpilih,
        angka_psikologis=angka_psikologis,
        biaya_pendampingan=biaya_pendampingan,
        angka_psikologis_dapil=angka_psikologis_dapil
    )

    df_terpilih["TOTAL_RAB"] = df_rab["TOTAL_RAB"]

    # === HEADER ===
    st.markdown("""
        <div class='section-header'>
            <h2 class='section-heading'>4. Sebaran Dapil Potensial</h2> 
            <span class='badge'>SP & RAB per Kursi</span>
        </div>
    """, unsafe_allow_html=True)

    # === PREPARE TABEL ===
    df_display = df_terpilih[[
        "DAPIL", "ALOKASI_KURSI", "SUARA_2024", "KURSI_2024",
        "TARGET_TAMBAHAN_KURSI", "TARGET_SUARA_2029", "TOTAL_RAB"
    ]].copy()

    df_display.columns = [
        "Dapil", "Alokasi Kursi", "Suara 2024", "Kursi 2024",
        "Target Kursi 2029", "Target Suara 2029", "Total RAB (Rp)"
    ]

    angka_cols = ["Suara 2024", "Target Suara 2029", "Total RAB (Rp)"]
    for kolom in angka_cols:
        df_display[kolom] = df_display[kolom].apply(format_ribuan)

    # === TAMPILKAN TABEL ===
    st.markdown(f"""
        <div class="scrollable-table">
            {df_display.to_html(index=False, classes="centered-table", escape=False)}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
    st.caption(f"Menampilkan {len(df_display)} DAPIL dari hasil seleksi seluruh kriteria.")