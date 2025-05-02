import pandas as pd

def hitung_rab_sp(row, angka_psikologis: int) -> int:
    return int(row["SP"] * angka_psikologis)

def hitung_biaya_kampanye(rab_sp: int) -> int:
    return int(rab_sp * 3 / 2)

def hitung_biaya_manajemen(biaya_kampanye: int) -> int:
    return int(biaya_kampanye / 3)

def hitung_total_rab(rab_sp: int, biaya_manajemen: int, biaya_pendampingan: int) -> int:
    return int(rab_sp + biaya_manajemen + biaya_pendampingan)

def proses_perhitungan_rab(
    df: pd.DataFrame,
    angka_psikologis: int,
    biaya_pendampingan: int,
    angka_psikologis_dapil: dict[str, int] = None
) -> pd.DataFrame:
    """
    Pipeline menghitung RAB dengan kemungkinan override Angka Psikologis per dapil.
    """

    df = df.copy()

    def get_angka_psikologis(dapil: str) -> int:
        if angka_psikologis_dapil and dapil in angka_psikologis_dapil:
            return angka_psikologis_dapil[dapil]
        return angka_psikologis

    df["ANGKA_PSIKOLOGIS"] = df["DAPIL"].apply(get_angka_psikologis)
    df["RAB_SP"] = df.apply(lambda row: hitung_rab_sp(row, row["ANGKA_PSIKOLOGIS"]), axis=1)
    df["BIAYA_KAMPANYE"] = df["RAB_SP"].apply(hitung_biaya_kampanye)
    df["BIAYA_MANAJEMEN"] = df["BIAYA_KAMPANYE"].apply(hitung_biaya_manajemen)

    df["TOTAL_RAB"] = df.apply(
        lambda row: hitung_total_rab(row["RAB_SP"], row["BIAYA_MANAJEMEN"], biaya_pendampingan)
        if row["SP"] > 0 else 0,
        axis=1
    )

    return df