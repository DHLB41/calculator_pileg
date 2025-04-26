import streamlit as st
from utils.formatters import format_ribuan

def tampilkan_ringkasan_dapil_terpilih(df_terpilih):
    """
    Tampilkan tabel dapil terpilih dari hasil seleksi seluruh kriteria.
    """

    if df_terpilih.empty:
        st.markdown("<div class='empty-state'> Tidak ada DAPIL yang memenuhi kriteria seleksi.</div>", unsafe_allow_html=True)
        return

    st.markdown("""
            <div class='section-header'>
                <h2 class='section-heading'>4. Sebaran Dapil Potensial</h2> 
    			<span class='badge'>SP & RAB per Kursi</span>
            </div>
        """, unsafe_allow_html=True)

    df_display = df_terpilih[[
        "DAPIL", "ALOKASI_KURSI", "SUARA_2024", "KURSI_2024",
        "TARGET_TAMBAHAN_KURSI", "TOTAL_TARGET_SUARA_2029", "TOTAL_RAB"
    ]].copy()

    df_display.columns = [
        "DAPIL", "Alokasi Kursi", "Suara 2024", "Kursi 2024",
        "Target Kursi 2029", "Target Suara 2029", "Total RAB"
    ]

    for kolom in ["Suara 2024", "Target Suara 2029", "Total RAB"]:
        df_display[kolom] = df_display[kolom].apply(format_ribuan)

    st.markdown(f"""
        <div class="scrollable-table">
            {df_display.to_html(index=False, classes="centered-table", escape=False)}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)
    st.caption(f"Menampilkan {len(df_display)} DAPIL dari hasil seleksi seluruh kriteria.")