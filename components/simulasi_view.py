import streamlit as st
import pandas as pd
from utils.formatters import format_ribuan
from utils.exporters import export_dapil_simulasi_to_html
from utils.simulasi import jalankan_simulasi_pencalonan

def tampilkan_simulasi_view(df_suara, df_kursi, df_dapil, biaya_pendampingan_default=1_000_000_000, angka_psikologis_default=50000):
    """
    Tampilan utama halaman simulasi pencalonan legislatif.
    """
    st.markdown("""
        <div class='section-header'>
            <h2 class='section-heading'>Input Data Umum</h2> 
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

    # === FORMULIR SIMULASI ===
    with st.form("form_simulasi"):
        nama = st.text_input("Nama (Opsional)")
        dana_maksimal = st.number_input("RAB Maksimal (Opsional)", min_value=0, step=1000000, format="%d")
        partai_opsional = st.multiselect("Pilih Partai (Opsional)", options=list(df_suara.columns[1:]))

        st.markdown("""
            <div class='section-header'>
                <h2 class='section-heading'>Pengaturan Simulasi</h2> 
            </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            biaya_pendampingan = st.number_input("Biaya Pendampingan per Kursi", min_value=0, step=1000000, value=biaya_pendampingan_default)
        with col2:
            angka_psikologis = st.number_input("Angka Psikologis", min_value=1000, step=1000, value=angka_psikologis_default)

        submit = st.form_submit_button("Simulasikan")

        if submit:
            st.session_state.simulasi_hasil = jalankan_simulasi_pencalonan(
                df_suara=df_suara,
                df_kursi=df_kursi,
                df_dapil=df_dapil,
                angka_psikologis=angka_psikologis,
                biaya_pendampingan=biaya_pendampingan,
                dana_maksimal=dana_maksimal if dana_maksimal > 0 else None,
                partai_terpilih=partai_opsional if partai_opsional else None,
            )

    # === TAMPILKAN HASIL JIKA SUDAH ADA DI SESSION ===
    if "simulasi_hasil" in st.session_state and not st.session_state.simulasi_hasil.empty:
        df_hasil = st.session_state.simulasi_hasil

        st.markdown(f"<h2 class='sub-section-heading'>Hasil Simulasi Pencalonan</h2>", unsafe_allow_html=True)

        # === FILTER ===
        st.markdown("<div class='sub-section-heading'>Filter Hasil Simulasi</div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            filter_dapil = st.text_input("Cari Dapil", placeholder="Contoh: Jawa Timur")
        with col2:
            filter_kursi = st.selectbox("Filter Target Kursi", options=["Semua"] + sorted(df_hasil["TARGET_TAMBAHAN_KURSI"].unique()))
        with col3:
            filter_partai = st.selectbox("Filter Partai", options=["Semua"] + sorted(df_hasil["PARTAI"].unique()))

        df_filtered = df_hasil.copy()
        if filter_dapil:
            df_filtered = df_filtered[df_filtered["DAPIL"].str.contains(filter_dapil, case=False, na=False)]
        if filter_kursi != "Semua":
            df_filtered = df_filtered[df_filtered["TARGET_TAMBAHAN_KURSI"] == filter_kursi]
        if filter_partai != "Semua":
            df_filtered = df_filtered[df_filtered["PARTAI"] == filter_partai]

        st.caption(f"Menampilkan {len(df_filtered)} dari {len(df_hasil)} hasil simulasi")

        st.markdown("<div class='sub-section-heading'>Detail Hasil Simulasi</div>", unsafe_allow_html=True)
        st.markdown("<div style='margin-top:0.8rem;'></div>", unsafe_allow_html=True)

        for i, row in df_filtered.iterrows():
            with st.container():
                st.markdown(f"""
                <div class='simulasi-card'>
                    <h4>{row['DAPIL']}</h4>
                    <p><span class='badge'>Partai: {row['PARTAI']}</span> <span class='badge'>Target Kursi ke-{row['TARGET_TAMBAHAN_KURSI']}</span> <span class='badge success'>RAB: Rp {format_ribuan(row['TOTAL_RAB'])}</span></p>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("Lihat Detail"):
                    st.markdown("#### Informasi Dapil")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.text_input("Alokasi Kursi", value=str(row["ALOKASI KURSI"]), disabled=True, key=f"alokasi{i}")
                        st.text_input("Kursi 2024", value=str(row["KURSI_2024"]), disabled=True, key=f"kursi{i}")
                    with col2:
                        st.text_input("Suara 2024", value=format_ribuan(row["SUARA_2024"]), disabled=True, key=f"s2024{i}")
                        st.text_input("Target Kursi 2029", value=str(row["TARGET_TAMBAHAN_KURSI"]), disabled=True, key=f"tk{i}")
                    with col3:
                        st.text_input("Target Suara 2029", value=format_ribuan(row["TARGET_SUARA_2029"]), disabled=True, key=f"ts2029{i}")
                        partai_k2_label = f"{row['PARTAI_K2_TERENDAH']} ({format_ribuan(row['SUARA_K2'])})"
                        st.text_input("Partai K2 Terendah", value=partai_k2_label, disabled=True, key=f"pk2{i}")

                    st.markdown("#### Informasi Biaya")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.text_input("SP", value=format_ribuan(row["SP"]), disabled=True, key=f"sp{i}")
                    with col2:
                        st.text_input("RAB SP + Manajemen", value=format_ribuan(row["BIAYA_KAMPANYE"]), disabled=True, key=f"kampanye{i}")
                    with col3:
                        st.text_input("Biaya Pendampingan", value=format_ribuan(row["BIAYA_PENDAMPINGAN"]), disabled=True, key=f"bp{i}")
                    with col4:
                        st.text_input("Total RAB", value=format_ribuan(row["TOTAL_RAB"]), disabled=True, key=f"totrab{i}")

            # Tambahkan tombol ekspor HTML di bawah detail tiap dapil
            with st.container():
                nama_file = f"rangkuman_simulasi_{row['DAPIL'].lower().replace(' ', '_')}.html"
                html_content = export_dapil_simulasi_to_html(row, nama_file=nama_file)

                st.download_button(
                    label="Download",
                    data=html_content,
                    file_name=nama_file,
                    mime="text/html",
                    key=f"download_{i}"
                )