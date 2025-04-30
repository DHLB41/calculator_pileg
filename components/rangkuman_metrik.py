import streamlit as st
from utils import format_ribuan

def tampilkan_rangkuman_metrik(df_terpilih):
    """
    Menampilkan metrik akhir: total suara, kursi, dan RAB dari hasil seleksi.
    """

    if df_terpilih.empty:
        return

    # Hitung total
    total_suara = int(df_terpilih['TARGET_SUARA_2029'].sum())
    total_kursi = int(df_terpilih['TARGET_TAMBAHAN_KURSI'].sum())
    total_rab = int(df_terpilih['TOTAL_RAB'].sum())

    # Header
    st.markdown("""
        <div class='section-header'>
            <h2 class='section-heading'>5. Rangkuman Simulasi</h2> 
            <span class='badge'>Summary Akhir</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

    # Tampilkan metrik
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Total Target Suara 2029", value=format_ribuan(total_suara))
        with col2:
            st.metric(label="Target Tambahan Kursi", value=total_kursi)
        with col3:
            st.metric(label="Total RAB (Rp)", value=format_ribuan(total_rab))

    # Caption
    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    st.caption("Rangkuman ini mencakup total agregat dari semua Dapil terpilih dalam simulasi.")

    # Divider
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)