import pandas as pd

def filter_dapil_terpilih(df_all_kriteria: pd.DataFrame, target_kursi: int) -> pd.DataFrame:
    """
    Seleksi dapil dari hasil gabungan kriteria berdasarkan target kursi nasional.
    Mengambil dapil dari urutan terendah TOTAL_TARGET_SUARA_2029 secara bertahap
    hingga jumlah kursi terpenuhi.

    Args:
        df_all_kriteria (pd.DataFrame): DataFrame gabungan dari semua kriteria
        target_kursi (int): Total kursi tambahan yang ingin dicapai

    Returns:
        pd.DataFrame: df_terpilih yang berisi baris terpilih sesuai target kursi
    """
    selected_rows = []
    total_kursi = 0

    for _, row in df_all_kriteria.iterrows():
        if total_kursi >= target_kursi:
            break
        selected_rows.append(row.to_dict())
        total_kursi += row["TARGET_TAMBAHAN_KURSI"]

    df_terpilih = pd.DataFrame(selected_rows).reset_index(drop=True)
    return df_terpilih