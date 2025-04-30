import pandas as pd

def hitung_rab_sp(row, angka_psikologis: int) -> int:
    """
    Hitung RAB SP berdasarkan SP x angka psikologis.
    """
    return int(row["SP"] * angka_psikologis)

def hitung_biaya_kampanye(rab_sp: int) -> int:
    """
    Hitung estimasi Biaya Kampanye (RAB_SP adalah 2/3 dari biaya kampanye).
    """
    return int(rab_sp * 3 / 2)

def hitung_biaya_manajemen(biaya_kampanye: int) -> int:
    """
    Hitung Biaya Manajemen sebagai 1/3 dari Biaya Kampanye.
    """
    return int(biaya_kampanye / 3)

def hitung_total_rab(rab_sp: int, biaya_manajemen: int, biaya_pendampingan: int) -> int:
    """
    Hitung Total RAB = RAB_SP + Biaya Manajemen + Biaya Pendampingan.
    """
    return int(rab_sp + biaya_manajemen + biaya_pendampingan)

def proses_perhitungan_rab(df: pd.DataFrame, angka_psikologis: int, biaya_pendampingan: int) -> pd.DataFrame:
    """
    Pipeline menghitung RAB: RAB_SP, Biaya Kampanye, Biaya Manajemen, Total RAB.
    """
    df = df.copy()

    df["RAB_SP"] = df["SP"].apply(lambda sp: int(sp * angka_psikologis))
    df["BIAYA_KAMPANYE"] = df["RAB_SP"].apply(hitung_biaya_kampanye)
    df["BIAYA_MANAJEMEN"] = df["BIAYA_KAMPANYE"].apply(hitung_biaya_manajemen)

    df["TOTAL_RAB"] = df.apply(
        lambda row: hitung_total_rab(row["RAB_SP"], row["BIAYA_MANAJEMEN"], biaya_pendampingan)
        if row["SP"] > 0 else 0,
        axis=1
    )

    return df