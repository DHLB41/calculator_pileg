import pandas as pd

def hitung_suara_tambahan(row):
    """
    Hitung suara tambahan yang dibutuhkan berdasarkan selisih kebutuhan dengan suara 2024.
    """
    if row["TARGET_TAMBAHAN_KURSI"] == 0:
        return 0
    elif row["TARGET_KEBUTUHAN"] < row["SUARA_2024"]:
        return 0
    return row["TARGET_KEBUTUHAN"] - row["SUARA_2024"]


def hitung_total_suara_tambahan(row, kehilangan_2024):
    """
    Tambahkan potensi kehilangan suara 2024 ke suara tambahan.
    """
    if row["SUARA_TAMBAHAN"] == 0:
        return 0
    return row["SUARA_TAMBAHAN"] + (row["SUARA_2024"] * (kehilangan_2024 / 100))


def hitung_sp(row, kehilangan_sp):
    """
    Hitung suara penguat (SP) berdasarkan total suara tambahan dan faktor kehilangan SP.
    """
    if row["TOTAL_SUARA_TAMBAHAN"] == 0:
        return 0
    return row["TOTAL_SUARA_TAMBAHAN"] * (1 + kehilangan_sp / 100)


def hitung_sp_per_kursi(row, kursi_input):
    """
    Hitung distribusi SP per kursi berdasarkan proporsi input.
    """
    jumlah_kursi = int(row["TARGET_TAMBAHAN_KURSI"])
    total_sp = row["SP"]
    hasil = [0.0, 0.0, 0.0, 0.0]

    if jumlah_kursi == 1:
        hasil[0] = total_sp
    elif jumlah_kursi in [2, 3, 4]:
        for i in range(jumlah_kursi):
            proporsi_key = f"proporsi_{jumlah_kursi}_{i+1}"
            proporsi = kursi_input.get(proporsi_key, 0)
            hasil[i] = (total_sp / jumlah_kursi) * (proporsi / 100)

    return pd.Series(hasil)