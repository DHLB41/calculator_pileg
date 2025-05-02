import streamlit as st
import pandas as pd
from utils.formatters import format_ribuan
from utils.calculations.rab_calculator import proses_perhitungan_rab

def safe_get(dapil_obj, key):
    """Mengakses key baik dari dict maupun Series. Fallback ke 0 jika tidak ada."""
    if isinstance(dapil_obj, dict):
        return dapil_obj.get(key, 0)
    elif hasattr(dapil_obj, '__getitem__') and key in dapil_obj:
        return dapil_obj[key]
    return 0

def tampilkan_detail_dapil_terpilih(dapil, df_terpilih, angka_psikologis, biaya_manajemen, biaya_pendampingan):
    idx = st.session_state.dapil_page

    if "angka_psikologis_dapil" not in st.session_state:
        st.session_state.angka_psikologis_dapil = {}

    dapil_nama = safe_get(dapil, "DAPIL")
    st.markdown(f"### <span class='section-heading'>Detail Dapil:</span> <span class='badge'>{dapil_nama}</span>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # === INFO UTAMA ===
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text_input("Alokasi Kursi", value=format_ribuan(safe_get(dapil, 'ALOKASI_KURSI')), disabled=True)
        with col2:
            st.text_input("Suara 2024", value=format_ribuan(safe_get(dapil, 'SUARA_2024')), disabled=True)
        with col3:
            st.text_input("Kursi 2024", value=format_ribuan(safe_get(dapil, 'KURSI_2024')), disabled=True)

        col4, col5, col6 = st.columns(3)
        with col4:
            st.text_input("Target Kursi 2029", value=format_ribuan(safe_get(dapil, 'TARGET_TAMBAHAN_KURSI')), disabled=True)
        with col5:
            st.text_input("Target Suara 2029", value=format_ribuan(safe_get(dapil, 'TARGET_SUARA_2029')), disabled=True)
        with col6:
            st.text_input("Partai Terendah Ke-2", value=f"{safe_get(dapil, 'PARTAI_K2_TERENDAH')} ({format_ribuan(safe_get(dapil, 'SUARA_K2'))} suara)", disabled=True)

    # === INPUT ANGKA PSIKOLOGIS PER DAPIL ===
    if angka_psikologis >= 1000:
        default_angka = st.session_state.angka_psikologis_dapil.get(dapil_nama, angka_psikologis)

        with st.form(f"form_angka_psiko_{dapil_nama}"):
            input_angka = st.number_input(
                label="Angka Psikologis Khusus Dapil",
                min_value=1000,
                max_value=1000000000,
                step=10000,
                value=default_angka,
                key=f"angka_psiko_input_{dapil_nama}"
            )
            submitted = st.form_submit_button("🔁 Update Perhitungan")

            if submitted:
                st.session_state.angka_psikologis_dapil[dapil_nama] = input_angka
                st.rerun()
    else:
        st.warning("⚠️ Silakan isi terlebih dahulu Angka Psikologis secara umum (≥ 1000) sebelum mengatur per Dapil.")

    # === TABEL SP PER KURSI ===
    st.markdown("#### SP per Kursi")
    df_sp = pd.DataFrame([{
        "TOTAL SP": safe_get(dapil, "SP"),
        "SP Kursi 1": safe_get(dapil, "SP_KURSI_1"),
        "SP Kursi 2": safe_get(dapil, "SP_KURSI_2"),
        "SP Kursi 3": safe_get(dapil, "SP_KURSI_3"),
        "SP Kursi 4": safe_get(dapil, "SP_KURSI_4"),
    }])
    df_sp = df_sp.applymap(lambda x: format_ribuan(x) if x > 0 else "0")

    st.markdown(f"""
        <div class="scrollable-table">
            {df_sp.to_html(index=False, classes="centered-table", escape=False)}
        </div>
    """, unsafe_allow_html=True)

    # === PERHITUNGAN RAB ===
    df_dapil_ini = pd.DataFrame([dapil])
    df_rab = proses_perhitungan_rab(
        df=df_dapil_ini,
        angka_psikologis=angka_psikologis,
        biaya_pendampingan=biaya_pendampingan,
        angka_psikologis_dapil=st.session_state.angka_psikologis_dapil
    )

    rab_sp = df_rab.iloc[0]["RAB_SP"]
    total_rab_all = df_rab.iloc[0]["TOTAL_RAB"]
    angka_psiko_dapil_ini = st.session_state.angka_psikologis_dapil.get(dapil_nama, angka_psikologis)

    # === RAB PER KURSI (SP x Angka Psikologis)
    st.markdown("#### RAB SP per Kursi")
    rab_sp_kursi = [int(safe_get(dapil, f"SP_KURSI_{i}") * angka_psiko_dapil_ini) for i in range(1, 5)]
    df_rab = pd.DataFrame([rab_sp_kursi], columns=[f"RAB Kursi {i}" for i in range(1, 5)])
    df_rab = df_rab.applymap(format_ribuan)

    st.markdown(f"""
        <div class="scrollable-table">
            {df_rab.to_html(index=False, classes="centered-table", escape=False)}
        </div>
    """, unsafe_allow_html=True)

    # === TOTAL RAB ===
    st.markdown("#### Total RAB")
    df_total = pd.DataFrame([[
        format_ribuan(rab_sp),
        format_ribuan(biaya_pendampingan),
        format_ribuan(total_rab_all)
    ]], columns=["RAB SP", "Biaya Pendampingan", "TOTAL RAB"])

    st.markdown(f"""
        <div class="scrollable-table">
            {df_total.to_html(index=False, classes="centered-table", escape=False)}
        </div>
    """, unsafe_allow_html=True)

    df_terpilih.at[idx, "TOTAL_RAB"] = total_rab_all

    # === TOMBOL ELIMINASI ===
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    if st.button("Eliminasi Dapil Ini", key=f"eliminasi_{idx}"):
        st.session_state.show_popup = True
        st.session_state.elim_target = dapil_nama

    if st.session_state.get("show_popup") and st.session_state.get("elim_target") == dapil_nama:
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