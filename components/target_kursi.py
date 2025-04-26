import streamlit as st

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def tampilkan_input_target_kursi():
    """
    UI bagian 3: Input target kursi & proporsi kenaikan suara.
    Returns:
        tuple: (target_kursi, kursi_input_dict, kehilangan_2024, kehilangan_sp, target_suara_2029)
    """
    st.markdown("""
            <div class='section-header'>
                <h2 class='section-heading'>3. Target Kursi & Proporsi Pembagian SP</h2> 
    			<span class='badge'>Input Strategis</span>
            </div>
        """, unsafe_allow_html=True)
    target_kursi = st.number_input(" Target Perolehan Kursi Pemilu 2029", min_value=0, step=1, value=0)

    st.markdown("<div class='sub-section-heading'> Proporsi Target SP</div>", unsafe_allow_html=True)
    st.caption("Atur persentase target SP per kursi untuk tiap dapil. Persentase dihitung berdasarkan target penambahan kursi dan total target SP.")

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    kursi_input = {}
    kursi_labels = ["Kursi Ke-1", "Kursi Ke-2", "Kursi Ke-3", "Kursi Ke-4"]

    for i in range(1, 5):
        st.markdown("<div style='margin-top:0.5rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"**Penambahan {i} Kursi**")
        cols = st.columns(4)
        for j, col in enumerate(cols):
            with col:
                key = f"proporsi_{i}_{j+1}"
                kursi_input[key] = st.number_input(
                    label=kursi_labels[j],
                    key=key,
                    min_value=0.0,
                    max_value=200.0,
                    step=10.0,
                    format="%.2f"
                )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    with st.expander("Pengaturan Tambahan: Faktor Pengurang & Target Suara", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            kehilangan_2024 = st.number_input("Potensi Kehilangan Suara 2029 (%)", min_value=0.0, max_value=200.0, step=1.0, format="%.2f")
        with col2:
            kehilangan_sp = st.number_input("Potensi Kehilangan SP (%)", min_value=0.0, max_value=200.0, step=1.0, format="%.2f")
        with col3:
            target_suara_2029 = st.number_input("Proporsi Target Suara 2029 (%)", min_value=0.0, max_value=200.0, step=1.0, format="%.2f")

    return target_kursi, kursi_input, kehilangan_2024, kehilangan_sp, target_suara_2029