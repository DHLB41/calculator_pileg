import pandas as pd
from typing import Optional, List

from utils.calculations.sp_calculator import proses_perhitungan_sp
from utils.calculations.rab_calculator_individu import proses_perhitungan_rab_individu
from utils.sainte_lague import partai_kursi_ke_2_terbawah

DEFAULT_PROPORSI_SUARA_2029 = 80
DEFAULT_KEHILANGAN_2024 = 30
DEFAULT_KEHILANGAN_SP = 20

def jalankan_simulasi_pencalonan(
    df_dapil: pd.DataFrame,
    df_suara: pd.DataFrame,
    df_kursi: pd.DataFrame,
    partai_terpilih: Optional[List[str]] = None,
    dana_maksimal: Optional[int] = None,
    angka_psikologis: int = 50000,
    biaya_pendampingan: int = 1_000_000_000,
    kehilangan_2024: float = DEFAULT_KEHILANGAN_2024,
    kehilangan_sp: float = DEFAULT_KEHILANGAN_SP,
    target_suara_2029: float = DEFAULT_PROPORSI_SUARA_2029,
    kursi_input: Optional[dict] = None
) -> pd.DataFrame:

    if kursi_input is None:
        kursi_input = {
            "proporsi_1_1": 100,
            "proporsi_2_1": 60,
            "proporsi_2_2": 40,
            "proporsi_3_1": 50,
            "proporsi_3_2": 30,
            "proporsi_3_3": 20,
            "proporsi_4_1": 40,
            "proporsi_4_2": 30,
            "proporsi_4_3": 20,
            "proporsi_4_4": 10,
        }

    semua_partai = [col for col in df_suara.columns if col != "DAPIL"]
    if not partai_terpilih:
        partai_terpilih = semua_partai

    hasil = []

    for dapil in df_dapil["DAPIL"].unique():
        alokasi_kursi = df_dapil.loc[df_dapil["DAPIL"] == dapil, "ALOKASI KURSI"].values[0]

        for partai in partai_terpilih:
            kursi_2024 = int(df_kursi.loc[df_kursi["DAPIL"] == dapil, partai].fillna(0).values[0]) if partai in df_kursi.columns else 0
            suara_2024 = int(df_suara.loc[df_suara["DAPIL"] == dapil, partai].fillna(0).values[0]) if partai in df_suara.columns else 0
            partai_k2 = partai_kursi_ke_2_terbawah(dapil, alokasi_kursi, df_suara, semua_partai)

            if not partai_k2:
                continue

            suara_k2 = df_suara.loc[df_suara["DAPIL"] == dapil, partai_k2].values[0]
            target_kursi = kursi_2024 + 1

            hasil.append({
                "DAPIL": dapil,
                "PARTAI": partai,
                "ALOKASI KURSI": alokasi_kursi,
                "KURSI_2024": kursi_2024,
                "SUARA_2024": suara_2024,
                "TARGET_TAMBAHAN_KURSI": target_kursi,
                "SUARA_K2": int(suara_k2),
                "PARTAI_K2_TERENDAH": partai_k2
            })

    df_simulasi = pd.DataFrame(hasil)

    if df_simulasi.empty:
        return df_simulasi

    # Gunakan fungsi SP resmi dari sp_calculator (sudah mengandung logika kebutuhan target)
    df_simulasi = proses_perhitungan_sp(
        df_simulasi, kehilangan_2024, kehilangan_sp, kursi_input, target_suara_2029
    )

    # Hitung RAB hanya berdasarkan SP kursi yang dituju user
    df_simulasi = proses_perhitungan_rab_individu(
        df_simulasi, angka_psikologis, biaya_pendampingan
    )

    if dana_maksimal:
        df_simulasi = df_simulasi[df_simulasi["TOTAL_RAB"] <= dana_maksimal]

    df_simulasi = df_simulasi.sort_values(
        by=["TARGET_TAMBAHAN_KURSI", "TOTAL_RAB"], ascending=[True, True]
    ).reset_index(drop=True)

    return df_simulasi