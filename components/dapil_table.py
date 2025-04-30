import streamlit as st
from utils import format_ribuan, format_persen

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
def tampilkan_tabel_dapil(df_dapil, df_suara, df_kursi, selected_party):
    st.markdown("""
            <div class='section-header'>
                <h2 class='section-heading'>2. Sebaran Perolehan Suara & Kursi</h2> 
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<p class='stCaption'>Data ditampilkan berdasarkan hasil Pemilu 2024 untuk tiap DAPIL</p>", unsafe_allow_html=True)

    if selected_party not in df_suara.columns:
        st.warning(f"Data suara untuk partai '{selected_party}' tidak tersedia.")
        return

    if selected_party in df_kursi.columns:
        kursi_dapil = df_kursi.set_index("DAPIL")[selected_party].to_dict()
    else:
        kursi_dapil = {dapil: 0 for dapil in df_kursi["DAPIL"]}
        st.markdown("<div class='alert-warning'>Partai ini tidak memperoleh kursi di Pemilu 2024.</div>", unsafe_allow_html=True)

    suara_dapil = df_suara.set_index("DAPIL")[selected_party].to_dict()

    tabel = df_dapil.copy()
    tabel["Perolehan Suara"] = tabel["DAPIL"].map(suara_dapil).fillna(0).astype(int)
    tabel["Perolehan Kursi"] = tabel["DAPIL"].map(kursi_dapil).fillna(0).astype(int)
    tabel["Persentase Perolehan Suara"] = (
        (tabel["Perolehan Suara"] / tabel["TOTAL DPT"]) * 100
    ).round(2).astype(str) + " %"

    # Format angka
    tabel["TOTAL DPT"] = tabel["TOTAL DPT"].apply(format_ribuan)
    tabel["Perolehan Suara"] = tabel["Perolehan Suara"].apply(format_ribuan)
    tabel["No"] = range(1, len(tabel) + 1)

    # Badge untuk kursi
    def badge_kursi(val):
        val_int = int(val)
        if val_int == 0:
            return "<span class='badge danger'>0</span>"
        return f"<span class='badge success'>{val_int}</span>"

    tabel["Perolehan Kursi"] = tabel["Perolehan Kursi"].apply(badge_kursi)

    # Tooltip untuk persentase suara
    tabel["Persentase Perolehan Suara"] = tabel["Persentase Perolehan Suara"].apply(
        lambda x: f"<span class='tooltip' data-tooltip='Dihitung dari total DPT'>{x}</span>"
    )

    tabel = tabel[[
        "No", "DAPIL", "ALOKASI KURSI", "TOTAL DPT",
        "Perolehan Suara", "Perolehan Kursi", "Persentase Perolehan Suara"
    ]]

    # Pagination
    per_page = 10
    if "current_page" not in st.session_state:
        st.session_state.current_page = 1

    start_idx = (st.session_state.current_page - 1) * per_page
    end_idx = start_idx + per_page
    tabel_page = tabel.iloc[start_idx:end_idx]

    # Tampilkan tabel
    st.markdown(
        f"""
        <div class="scrollable-table">
            {tabel_page.to_html(index=False, classes="centered-table", escape=False)}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Spasi vertikal untuk kenyamanan navigasi
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # Navigasi halaman
    col_prev, _, col_next = st.columns([1, 6, 1])
    total_pages = (len(tabel) - 1) // per_page + 1

    with col_prev:
        if st.session_state.current_page > 1:
            if st.button("← Sebelumnya", key="prev_page"):
                st.session_state.current_page -= 1

    with col_next:
        if st.session_state.current_page < total_pages:
            if st.button("Berikutnya →", key="next_page"):
                st.session_state.current_page += 1

    # Footer info
    st.caption(f"Menampilkan halaman ke-{st.session_state.current_page} dari {total_pages} | Total DAPIL: {len(tabel)}")
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)