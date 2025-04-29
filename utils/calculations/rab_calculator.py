import pandas as pd

def hitung_rab_sp(row, angka_psikologis: int) -> int:
    return int(row["SP"] * angka_psikologis)

def hitung_biaya_manajemen(rab_sp: int) -> int:
    return int(rab_sp / 3)

def hitung_total_rab(rab_sp: int, biaya_manajemen: int, biaya_pendampingan: int) -> int:
    return int(rab_sp + biaya_manajemen + biaya_pendampingan)

def proses_perhitungan_rab(df: pd.DataFrame, angka_psikologis: int, biaya_manajemen: int, biaya_pendampingan: int) -> pd.DataFrame:
    df = df.copy()

    # Hitung RAB_SP
    df["RAB_SP"] = df["SP"].apply(lambda sp: sp * angka_psikologis)

    # Hitung Biaya Manajemen
    df["BIAYA_MANAJEMEN"] = df["RAB_SP"].apply(lambda rab_sp: rab_sp // 3)

    # Hitung Total RAB
    df["TOTAL_RAB"] = df.apply(
        lambda row: row["RAB_SP"] + row["BIAYA_MANAJEMEN"] + biaya_pendampingan
        if row["SP"] > 0 else 0,
        axis=1
    )

    return df