import streamlit as st
import pandas as pd
import datetime

DEBUG_MODE = True  # Ganti False untuk menonaktifkan log saat production


def log_debug(message):
    """
    Menampilkan pesan debug jika DEBUG_MODE aktif.
    """
    if DEBUG_MODE:
        st.write(f"🛠️ [DEBUG] {message}")


def log_error(e):
    """
    Menampilkan error dengan gaya khusus.
    """
    st.error(f"🚨 Terjadi kesalahan: {str(e)}")


def log_shape(df: pd.DataFrame, label: str = "DataFrame"):
    """
    Menampilkan jumlah baris dan kolom sebuah DataFrame.
    """
    if DEBUG_MODE:
        st.caption(f"📐 {label} shape: {df.shape[0]} baris × {df.shape[1]} kolom")


def log_time(msg: str):
    """
    Menampilkan waktu sekarang untuk benchmark sederhana.
    """
    if DEBUG_MODE:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        st.caption(f"⏱️ {msg} — {now}")
