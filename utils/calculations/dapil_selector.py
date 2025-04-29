import pandas as pd

def filter_dapil_terpilih(df_all_kriteria: pd.DataFrame, target_kursi: int) -> pd.DataFrame:
    """
    Seleksi dapil dari hasil gabungan kriteria berdasarkan target kursi nasional.
    Mengambil dapil dari urutan terendah TARGET_SUARA_2029 secara bertahap
    hingga jumlah kursi terpenuhi.

    Args:
        df_all_kriteria (pd.DataFrame): DataFrame gabungan dari semua kriteria
        target_kursi (int): Total kursi tambahan yang ingin dicapai

    Returns:
        pd.DataFrame: df_terpilih yang berisi baris terpilih sesuai target kursi
    """
    # Pastikan kolom TARGET_SUARA_2029 tersedia
    if "TARGET_SUARA_2029" not in df_all_kriteria.columns:
        raise ValueError("Kolom 'TARGET_SUARA_2029' belum dihitung. Jalankan proses SP terlebih dahulu.")

    df_sorted = df_all_kriteria.sort_values(by="TARGET_SUARA_2029", ascending=True).copy()
    selected_rows = []
    total_kursi = 0

    for _, row in df_sorted.iterrows():
        if total_kursi >= target_kursi:
            break
        selected_rows.append(row.to_dict())
        total_kursi += row["TARGET_TAMBAHAN_KURSI"]

    return pd.DataFrame(selected_rows).reset_index(drop=True)