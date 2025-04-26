import pandas as pd
from pathlib import Path

def load_excel_data(filepath: str):
    """
    Load data Excel berisi:
    - Sheet 'perolehan_suara'
    - Sheet 'hasil_sl'
    - Sheet 'dapil'
    - (Opsional) Sheet 'detail_sl' untuk data caleg pemenang

    Returns:
        df_suara: DataFrame perolehan suara
        df_kursi: DataFrame hasil Sainte-Laguë
        df_dapil: DataFrame info dapil
        df_detail_sl: DataFrame detail caleg pemenang per kursi (jika ada, jika tidak dikembalikan None)
    """
    file_path = Path(filepath)

    if not file_path.exists():
        raise FileNotFoundError(f"File '{filepath}' tidak ditemukan.")

    df_suara = pd.read_excel(file_path, sheet_name="perolehan_suara")
    df_kursi = pd.read_excel(file_path, sheet_name="hasil_sl")
    df_dapil = pd.read_excel(file_path, sheet_name="dapil")
    df_detail_sl = pd.read_excel(file_path, sheet_name="detail_sl")

    return df_suara, df_kursi, df_dapil, df_detail_sl


def get_total_suara(df, partai):
    """
    Mengembalikan total suara nasional untuk partai tertentu.
    """
    return df[partai].sum() if partai in df.columns else 0


def get_total_kursi(df, partai):
    """
    Mengembalikan total kursi nasional untuk partai tertentu.
    """
    return df[partai].sum() if partai in df.columns else 0