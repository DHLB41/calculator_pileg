import streamlit as st
from utils.exporters import (
    export_to_html, export_to_csv, export_to_excel, export_to_pdf
)

def tampilkan_download_section(df_terpilih, df_dapil, selected_party, votes_2024, seats_2024):
    """
    Komponen untuk mengunduh ringkasan hasil kalkulasi dalam berbagai format.
    """

    # === HEADER ===
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='section-header'>
            <h2 class='section-heading'>6. Unduh Ringkasan Hasil Kalkulasi</h2>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

    # === PILIH FORMAT ===
    format_opsi = st.selectbox("Pilih format ekspor:", ["HTML", "XLSX", "CSV", "PDF"])

    # === HANDLE EKSPOR SESUAI PILIHAN ===
    if format_opsi == "HTML":
        html_export = export_to_html(df_terpilih, df_dapil, selected_party, votes_2024, seats_2024)
        html_bytes = html_export.encode("utf-8")
        st.download_button(
            label="Download HTML",
            data=html_bytes,
            file_name="rangkuman_kalkulasi_2029.html",
            mime="text/html"
        )

    elif format_opsi == "XLSX":
        xlsx_data = export_to_excel(df_terpilih, df_dapil)
        st.download_button(
            label="Download Excel",
            data=xlsx_data,
            file_name="rangkuman_kalkulasi_2029.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    elif format_opsi == "CSV":
        csv_data = export_to_csv(df_terpilih, df_dapil)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="rangkuman_kalkulasi_2029.csv",
            mime="text/csv"
        )

    elif format_opsi == "PDF":
        pdf_data = export_to_pdf(df_terpilih, df_dapil)
        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name="rangkuman_kalkulasi_2029.pdf",
            mime="application/pdf"
        )

    # === PETUNJUK LANJUTAN ===
    st.markdown("""
        <div class='alert-info'>
            Setelah mengunduh file, buka di browser dan tekan <strong>Ctrl + P</strong> (Windows) atau <strong>⌘ + P</strong> (Mac) untuk menyimpan sebagai PDF.
        </div>
    """, unsafe_allow_html=True)