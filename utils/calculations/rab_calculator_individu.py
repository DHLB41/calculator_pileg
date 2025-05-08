import pandas as pd

def hitung_rab_sp(sp_kursi_tertentu: int, angka_psikologis: int) -> int:
    """Hitung RAB SP berdasarkan SP kursi tertentu dan angka psikologis."""
    return int(sp_kursi_tertentu * angka_psikologis)

def hitung_biaya_kampanye(rab_sp: int) -> int:
    """Hitung biaya kampanye sebagai 1.5x dari RAB SP."""
    return int(rab_sp * 3 / 2)

def hitung_biaya_manajemen(biaya_kampanye: int) -> int:
    """Hitung biaya manajemen sebagai sepertiga dari biaya kampanye."""
    return int(biaya_kampanye / 3)

def hitung_total_rab(rab_sp: int, biaya_manajemen: int, biaya_pendampingan: int) -> int:
    """Total RAB adalah penjumlahan dari RAB SP, biaya manajemen, dan biaya pendampingan."""
    return int(rab_sp + biaya_manajemen + biaya_pendampingan)

def proses_perhitungan_rab_individu(
    df: pd.DataFrame,
    angka_psikologis: int,
    biaya_pendampingan: int
) -> pd.DataFrame:
    """
    Pipeline menghitung RAB hanya untuk kursi yang ditargetkan oleh individu.
    RAB dihitung hanya berdasarkan SP kursi yang dituju.
    """
    df = df.copy()

    # Ambil hanya SP untuk kursi target user (misal SP_KURSI_2 jika target = 2)
    def ambil_sp_target(row):
        target_kursi = row["TARGET_TAMBAHAN_KURSI"]
        return row.get(f"SP_KURSI_{target_kursi}", 0)

    df["SP_TARGET"] = df.apply(ambil_sp_target, axis=1)

    df["ANGKA_PSIKOLOGIS"] = angka_psikologis
    df["RAB_SP"] = df.apply(lambda row: hitung_rab_sp(row["SP_TARGET"], angka_psikologis), axis=1)
    df["BIAYA_KAMPANYE"] = df["RAB_SP"].apply(hitung_biaya_kampanye)
    df["BIAYA_MANAJEMEN"] = df["BIAYA_KAMPANYE"].apply(hitung_biaya_manajemen)
    df["BIAYA_PENDAMPINGAN"] = biaya_pendampingan

    df["TOTAL_RAB"] = df.apply(
        lambda row: hitung_total_rab(row["RAB_SP"], row["BIAYA_MANAJEMEN"], row["BIAYA_PENDAMPINGAN"]), axis=1
    )

    # Untuk keseragaman di UI dan sortir
    df["TOTAL_RAB_FINAL"] = df["TOTAL_RAB"]

    return df