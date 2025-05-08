# components/sidebar.py

import streamlit as st

def tampilkan_sidebar_header():
    with st.sidebar:
        st.markdown("""
            <div class='sidebar-header'>
                <h2>Kalkulator Pemilu 2029</h2>
                <p>Simulasi kebutuhan suara dan biaya pencalonan legislatif.</p>
            </div>
        """, unsafe_allow_html=True)