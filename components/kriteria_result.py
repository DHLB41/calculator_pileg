import streamlit as st
from utils.formatters import format_ribuan

def tampilkan_ringkasan_dapil_terpilih(df_terpilih):
    """
    Menampilkan tabel rekap dapil terpilih dari hasil seleksi kriteria.
    """

    if df_terpilih.empty:
        st.markdown("<div class='empty-state'>Tidak ada DAPIL yang memenuhi kriteria seleksi.</div>", unsafe_allow_html=True)
        return

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

    # Format angka ribuan
    angka_cols = ["Suara 2024", "Target Suara 2029", "Total RAB (Rp)"]
    for kolom in angka_cols:
        df_display[kolom] = df_display[kolom].apply(format_ribuan)

    # === TAMPILKAN TABEL ===
    st.markdown(f"""
        <div class="scrollable-table">
            {df_display.to_html(index=False, classes="centered-table", escape=False)}
        </div>
    """, unsafe_allow_html=True)

    # Footer info
    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
    st.caption(f"Menampilkan {len(df_display)} DAPIL dari hasil seleksi seluruh kriteria.")