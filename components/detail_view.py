import streamlit as st
import pandas as pd
from utils.formatters import format_ribuan

def tampilkan_detail_dapil_terpilih(dapil, df_terpilih, angka_psikologis, biaya_manajemen, biaya_pendampingan):
    idx = st.session_state.dapil_page

    st.markdown(f"### <span class='section-heading'>Detail Dapil:</span> <span class='badge'>{dapil['DAPIL']}</span>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # === INFO UTAMA ===
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Alokasi Kursi", value=format_ribuan(dapil['ALOKASI_KURSI']), disabled=True)
        with col2:
            st.text_input("Suara 2024", value=format_ribuan(dapil['SUARA_2024']), disabled=True)
        with col3:
            st.text_input("Kursi 2024", value=format_ribuan(dapil['KURSI_2024']), disabled=True)

        col4, col5, col6 = st.columns(3)
        with col4:
            st.text_input("Target Kursi 2029", value=format_ribuan(dapil['TARGET_TAMBAHAN_KURSI']), disabled=True)
        with col5:
            st.text_input("Target Suara 2029", value=format_ribuan(dapil['TARGET_SUARA_2029']), disabled=True)
        with col6:
            st.text_input("Partai Terendah Ke-2", value=f"{dapil['PARTAI_K2_TERENDAH']} ({format_ribuan(dapil['SUARA_K2'])} suara)", disabled=True)

    # === TABEL SP PER KURSI ===
    st.markdown("#### SP per Kursi")
    sp_kolom = ["SP", "SP_KURSI_1", "SP_KURSI_2", "SP_KURSI_3", "SP_KURSI_4"]
    df_sp = dapil[sp_kolom].to_frame().T.copy()
    df_sp.columns = ["TOTAL SP", "SP Kursi 1", "SP Kursi 2", "SP Kursi 3", "SP Kursi 4"]
    for col in df_sp.columns:
        df_sp[col] = df_sp[col].apply(lambda x: format_ribuan(x) if x > 0 else "0")

    st.markdown(f"""
        <div class="scrollable-table">
            {df_sp.to_html(index=False, classes="centered-table", escape=False)}
        </div>
    """, unsafe_allow_html=True)

    # === RAB ===
    st.markdown("#### RAB per Kursi (SP x Angka Psikologis)")
    rab_sp_kursi = [int(dapil.get(f"SP_KURSI_{i}", 0) * angka_psikologis) for i in range(1, 5)]
    df_rab = pd.DataFrame([rab_sp_kursi], columns=[f"RAB Kursi {i}" for i in range(1, 5)])
    df_rab = df_rab.applymap(format_ribuan)

    st.markdown(f"""
        <div class="scrollable-table">
            {df_rab.to_html(index=False, classes="centered-table", escape=False)}
        </div>
    """, unsafe_allow_html=True)

    # === TOTAL RAB + Manajemen + Pendampingan ===
    total_rab_kursi = [rab + biaya_manajemen + biaya_pendampingan if rab > 0 else 0 for rab in rab_sp_kursi]
    total_rab_all = sum(total_rab_kursi)
    df_total = pd.DataFrame([total_rab_kursi + [total_rab_all]], columns=[f"Total RAB Kursi {i}" for i in range(1, 5)] + ["TOTAL RAB"])
    df_total = df_total.applymap(format_ribuan)

    st.markdown("#### Total RAB (SP + Manajemen + Pendampingan)")
    st.markdown(f"""
        <div class="scrollable-table">
            {df_total.to_html(index=False, classes="centered-table", escape=False)}
        </div>
    """, unsafe_allow_html=True)

    # Update Total RAB ke df_terpilih real-time
    df_terpilih.at[idx, "TOTAL_RAB"] = total_rab_all

    # === TOMBOL ELIMINASI ===
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    if st.button("Eliminasi Dapil Ini", key=f"eliminasi_{idx}"):
        st.session_state.show_popup = True
        st.session_state.elim_target = dapil["DAPIL"]

    if st.session_state.get("show_popup") and st.session_state.get("elim_target") == dapil["DAPIL"]:
        with st.form("form_eliminasi"):
            alasan = st.text_area("Tuliskan alasan eliminasi dapil ini:", key="alasan_input", height=100)
            col_a, col_b = st.columns(2)
            with col_a:
                cancel = st.form_submit_button("Batal")
            with col_b:
                submit = st.form_submit_button("Konfirmasi Eliminasi")

            if cancel:
                st.session_state.show_popup = False
                st.rerun()
            elif submit:
                if alasan.strip() == "":
                    st.warning("Alasan eliminasi wajib diisi.")
                else:
                    dapil_nama = dapil["DAPIL"]
                    st.session_state.eliminated_dapil.add(dapil_nama)
                    st.session_state.alasan_eliminasi[dapil_nama] = alasan.strip()
                    st.session_state.show_popup = False
                    st.rerun()

    # === NAVIGASI DAPIL ===
    col_prev, _, col_next = st.columns([1, 6, 1])
    with col_prev:
        if st.session_state.dapil_page > 0:
            if st.button("← Sebelumnya", key="prev_dapil"):
                st.session_state.dapil_page -= 1
                st.rerun()
    with col_next:
        if st.session_state.dapil_page < len(df_terpilih) - 1:
            if st.button("Berikutnya →", key="next_dapil"):
                st.session_state.dapil_page += 1
                st.rerun()



def tampilkan_dapil_dieliminasi(df_all_kriteria):
    with st.expander("Lihat Dapil yang Telah Dieliminasi", expanded=False):
        if "eliminated_dapil" not in st.session_state or not st.session_state.eliminated_dapil:
            st.markdown("<div class='empty-state'>Belum ada dapil yang dieliminasi.</div>", unsafe_allow_html=True)
            return

        df_elim = df_all_kriteria[df_all_kriteria["DAPIL"].isin(st.session_state.eliminated_dapil)]

        for _, row in df_elim.iterrows():
            alasan = st.session_state.alasan_eliminasi.get(row["DAPIL"], "-")
            with st.container():
                st.markdown(f"<h4><span class='badge danger'>{row['DAPIL']}</span></h4>", unsafe_allow_html=True)
                st.markdown(f"**Alasan Eliminasi:** {alasan}", unsafe_allow_html=True)
                st.markdown(
                    f"Target Kursi: **{row['TARGET_TAMBAHAN_KURSI']}** | Target Suara: **{format_ribuan(row['TARGET_SUARA_2029'])}**",
                    unsafe_allow_html=True)

                st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
                if st.button("Restore", key=f"restore_{row['DAPIL']}"):
                    st.session_state.eliminated_dapil.remove(row["DAPIL"])
                    st.session_state.alasan_eliminasi.pop(row["DAPIL"], None)
                    st.success(f"{row['DAPIL']} berhasil dikembalikan.")
                    st.rerun()

                st.markdown("<div class='divider'></div>", unsafe_allow_html=True)