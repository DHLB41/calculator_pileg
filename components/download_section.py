import streamlit as st
from utils import export_to_html

def tampilkan_download_section(df_terpilih, df_dapil, selected_party, votes_2024, seats_2024):
    """
    Komponen untuk mengunduh ringkasan hasil kalkulasi dalam format HTML.
    """

    # === HEADER ===
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='section-header'>
            <h2 class='section-heading'>6. Unduh Ringkasan Hasil Kalkulasi</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

    # === EXPORT KE HTML ===
    html_export = export_to_html(df_terpilih, df_dapil, selected_party, votes_2024, seats_2024)
    html_bytes = html_export.encode("utf-8")

    # === TOMBOL DOWNLOAD ===
    st.download_button(
        label="⬇️ Download Ringkasan (HTML)",
        data=html_bytes,
        file_name="rangkuman_kalkulasi_2029.html",
        mime="text/html",
        help="Klik untuk mengunduh ringkasan dalam format HTML."
    )

    # === PETUNJUK LANJUTAN ===
    st.markdown("""
        <div class='alert-info'>
            💡 Setelah mengunduh file, buka di browser dan tekan <strong>Ctrl + P</strong> (Windows) atau <strong>⌘ + P</strong> (Mac) untuk menyimpan sebagai PDF.
        </div>
    """, unsafe_allow_html=True)