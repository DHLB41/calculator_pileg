# utils/calculations/sp_calculator.py

import pandas as pd


def hitung_target_kebutuhan(row):
    """
    Hitung Target Kebutuhan Suara berdasarkan Kursi 2024 dan Target Kursi 2029.
    Mengikuti rumus yang mempertimbangkan kursi existing.
    """
    kursi_2024 = row["KURSI_2024"]
    target_kursi = row["TARGET_TAMBAHAN_KURSI"]
    suara_k2 = row["SUARA_K2"]

    if kursi_2024 == target_kursi:
        return int(suara_k2 * 1.1)

    if kursi_2024 == 0 and target_kursi == 1:
        return int(suara_k2 * 1.1)
    elif kursi_2024 == 1 and target_kursi == 2:
        return int(suara_k2 * 1.1 * 3)
    elif kursi_2024 == 2 and target_kursi == 3:
        return int(suara_k2 * 1.1 * 5)
    elif kursi_2024 == 3 and target_kursi == 4:
        return int(suara_k2 * 1.1 * 7)
    else:
        # fallback umum untuk kasus lain
        return int(suara_k2 * 1.1 * (2 * target_kursi - 1))

def hitung_suara_tambahan(row):
    """
    Hitung Suara Tambahan: Jika Target Kebutuhan > Suara 2024, baru dihitung.
    """
    if row["TARGET_KEBUTUHAN"] <= row["SUARA_2024"]:
        return 0
    return row["TARGET_KEBUTUHAN"] - row["SUARA_2024"]

def hitung_potensi_kehilangan_suara(row, kehilangan_2024):
    """
    Hitung Potensi Kehilangan Suara berdasarkan % kehilangan suara 2024.
    """
    return int(row["SUARA_2024"] * kehilangan_2024 / 100)

def hitung_total_suara_tambahan(row):
    """
    Hitung Total Suara Tambahan = Suara Tambahan + Potensi Kehilangan Suara.
    """
    if row["SUARA_TAMBAHAN"] == 0:
        return row["POTENSI_KEHILANGAN_SUARA"]
    return row["SUARA_TAMBAHAN"] + row["POTENSI_KEHILANGAN_SUARA"]

def hitung_potensi_kehilangan_sp(row, kehilangan_sp):
    """
    Hitung Potensi Kehilangan SP berdasarkan total suara tambahan.
    """
    return int(row["TOTAL_SUARA_TAMBAHAN"] * kehilangan_sp / 100)

def hitung_sp(row):
    """
    Hitung SP: jika Total Suara Tambahan = 0 maka SP = 0,
    jika tidak, SP = Total Suara Tambahan + Potensi Kehilangan SP.
    """
    if row["TOTAL_SUARA_TAMBAHAN"] == 0:
        return 0
    return row["TOTAL_SUARA_TAMBAHAN"] + row["POTENSI_KEHILANGAN_SP"]

def hitung_sp_per_kursi(row, kursi_input):
    """
    Hitung distribusi SP untuk kursi 1-4 berdasarkan proporsi input user.
    """
    hasil = {}
    target_kursi = int(row["TARGET_TAMBAHAN_KURSI"])
    sp_total = row["SP"]

    if sp_total == 0 or target_kursi == 0:
        hasil["SP_KURSI_1"] = 0
        hasil["SP_KURSI_2"] = 0
        hasil["SP_KURSI_3"] = 0
        hasil["SP_KURSI_4"] = 0
        return pd.Series(hasil)

    for i in range(1, 5):
        if i > target_kursi:
            hasil[f"SP_KURSI_{i}"] = 0
            continue

        key = f"proporsi_{target_kursi}_{i}"
        proporsi = kursi_input.get(key, 0) / 100
        hasil[f"SP_KURSI_{i}"] = int(sp_total * proporsi)

    return pd.Series(hasil)

def hitung_target_suara_2029(row, target_suara_2029_persen):
    """
    Hitung Target Suara 2029 = (Suara 2024 + SP) x Proporsi Target Suara 2029.
    """
    return int((row["SUARA_2024"] + row["SP"]) * target_suara_2029_persen / 100)

def proses_perhitungan_sp(df: pd.DataFrame, kehilangan_2024: float, kehilangan_sp: float, kursi_input: dict, target_suara_2029_persen: float) -> pd.DataFrame:
    """
    Pipeline untuk memproses seluruh kolom:
    TARGET_KEBUTUHAN, SUARA_TAMBAHAN, POTENSI_KEHILANGAN_SUARA, TOTAL_SUARA_TAMBAHAN,
    POTENSI_KEHILANGAN_SP, SP, SP_KURSI_X, TARGET_SUARA_2029.
    """
    df = df.copy()

    df["TARGET_KEBUTUHAN"] = df.apply(hitung_target_kebutuhan, axis=1)
    df["SUARA_TAMBAHAN"] = df.apply(hitung_suara_tambahan, axis=1)
    df["POTENSI_KEHILANGAN_SUARA"] = df.apply(lambda row: hitung_potensi_kehilangan_suara(row, kehilangan_2024), axis=1)
    df["TOTAL_SUARA_TAMBAHAN"] = df.apply(hitung_total_suara_tambahan, axis=1)
    df["POTENSI_KEHILANGAN_SP"] = df.apply(lambda row: hitung_potensi_kehilangan_sp(row, kehilangan_sp), axis=1)
    df["SP"] = df.apply(hitung_sp, axis=1)

    sp_per_kursi = df.apply(lambda row: hitung_sp_per_kursi(row, kursi_input), axis=1)
    df[["SP_KURSI_1", "SP_KURSI_2", "SP_KURSI_3", "SP_KURSI_4"]] = sp_per_kursi

    df["TARGET_SUARA_2029"] = df.apply(lambda row: hitung_target_suara_2029(row, target_suara_2029_persen), axis=1)

    return df