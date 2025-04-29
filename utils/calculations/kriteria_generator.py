import pandas as pd
from utils.sainte_lague import simulasi_sainte_lague

PARTAI_TERPILIH = ["PKB", "GERINDRA", "PDIP", "GOLKAR", "NASDEM", "PKS", "PAN", "DEMOKRAT"]

def generate_kriteria_1(df_suara, df_kursi, df_dapil, selected_party):
    """
    Kriteria 1: Dapil tanpa kursi (kursi 0).
    """
    dapil_result = []

    for dapil in df_suara["DAPIL"]:
        alokasi_row = df_dapil[df_dapil["DAPIL"] == dapil]
        if alokasi_row.empty:
            continue

        alokasi = int(alokasi_row["ALOKASI KURSI"].values[0])
        kursi = int(df_kursi.loc[df_kursi["DAPIL"] == dapil, selected_party].fillna(0))
        suara = int(df_suara.loc[df_suara["DAPIL"] == dapil, selected_party].fillna(0))

        if kursi != 0:
            continue

        urutan_kursi, _ = simulasi_sainte_lague(dapil, alokasi, df_suara, PARTAI_TERPILIH + [selected_party])
        if len(urutan_kursi) < 2:
            continue

        partai_k2 = urutan_kursi[-2]
        suara_k2 = int(df_suara.loc[df_suara["DAPIL"] == dapil, partai_k2].fillna(0))

        dapil_result.append({
            "DAPIL": dapil,
            "PARTAI": selected_party,
            "ALOKASI_KURSI": alokasi,
            "SUARA_2024": suara,
            "KURSI_2024": kursi,
            "TARGET_TAMBAHAN_KURSI": 1,
            "PARTAI_K2_TERENDAH": partai_k2,
            "SUARA_K2": suara_k2
        })

    return pd.DataFrame(dapil_result)

def generate_kriteria_2(df_suara, df_kursi, df_dapil, selected_party):
    """
    Kriteria 2: Kursi 1 + partai K2 adalah PAN atau DEMOKRAT.
    """
    dapil_result = []

    for dapil in df_suara["DAPIL"]:
        alokasi_row = df_dapil[df_dapil["DAPIL"] == dapil]
        if alokasi_row.empty:
            continue

        alokasi = int(alokasi_row["ALOKASI KURSI"].values[0])
        kursi = int(df_kursi.loc[df_kursi["DAPIL"] == dapil, selected_party].fillna(0))
        suara = int(df_suara.loc[df_suara["DAPIL"] == dapil, selected_party].fillna(0))

        if kursi != 1:
            continue

        urutan_kursi, _ = simulasi_sainte_lague(dapil, alokasi, df_suara, PARTAI_TERPILIH)
        if len(urutan_kursi) < 2:
            continue

        partai_k2 = urutan_kursi[-2]
        if partai_k2 not in ["PAN", "DEMOKRAT"]:
            continue

        suara_k2 = int(df_suara.loc[df_suara["DAPIL"] == dapil, partai_k2].fillna(0))
        target_kursi = 1 if alokasi <= 4 else kursi + 1

        dapil_result.append({
            "DAPIL": dapil,
            "PARTAI": selected_party,
            "ALOKASI_KURSI": alokasi,
            "SUARA_2024": suara,
            "KURSI_2024": kursi,
            "TARGET_TAMBAHAN_KURSI": target_kursi,
            "PARTAI_K2_TERENDAH": partai_k2,
            "SUARA_K2": suara_k2
        })

    return pd.DataFrame(dapil_result)

def generate_kriteria_3(df_suara, df_kursi, df_dapil, selected_party):
    """
    Kriteria 3: Kursi 1 umum, tanpa syarat partai K2.
    """
    dapil_result = []

    for dapil in df_suara["DAPIL"]:
        alokasi_row = df_dapil[df_dapil["DAPIL"] == dapil]
        if alokasi_row.empty:
            continue

        alokasi = int(alokasi_row["ALOKASI KURSI"].values[0])
        kursi = int(df_kursi.loc[df_kursi["DAPIL"] == dapil, selected_party].fillna(0))
        suara = int(df_suara.loc[df_suara["DAPIL"] == dapil, selected_party].fillna(0))

        if kursi != 1:
            continue

        urutan_kursi, _ = simulasi_sainte_lague(dapil, alokasi, df_suara, PARTAI_TERPILIH)
        if len(urutan_kursi) < 2:
            continue

        partai_k2 = urutan_kursi[-2]
        suara_k2 = int(df_suara.loc[df_suara["DAPIL"] == dapil, partai_k2].fillna(0))
        target_kursi = 1 if alokasi <= 4 else kursi + 1

        dapil_result.append({
            "DAPIL": dapil,
            "PARTAI": selected_party,
            "ALOKASI_KURSI": alokasi,
            "SUARA_2024": suara,
            "KURSI_2024": kursi,
            "TARGET_TAMBAHAN_KURSI": target_kursi,
            "PARTAI_K2_TERENDAH": partai_k2,
            "SUARA_K2": suara_k2
        })

    return pd.DataFrame(dapil_result)

def generate_kriteria_4(df_suara, df_kursi, df_dapil, selected_party):
    """
    Kriteria 4: Kursi lebih dari 1, target suara bertingkat.
    """
    dapil_result = []

    for dapil in df_suara["DAPIL"]:
        alokasi_row = df_dapil[df_dapil["DAPIL"] == dapil]
        if alokasi_row.empty:
            continue

        alokasi = int(alokasi_row["ALOKASI KURSI"].values[0])
        kursi = int(df_kursi.loc[df_kursi["DAPIL"] == dapil, selected_party].fillna(0))
        suara = int(df_suara.loc[df_suara["DAPIL"] == dapil, selected_party].fillna(0))

        if kursi <= 1:
            continue

        urutan_kursi, _ = simulasi_sainte_lague(dapil, alokasi, df_suara, PARTAI_TERPILIH)
        if len(urutan_kursi) < 2:
            continue

        partai_k2 = urutan_kursi[-2]
        suara_k2 = int(df_suara.loc[df_suara["DAPIL"] == dapil, partai_k2].fillna(0))

        dapil_result.append({
            "DAPIL": dapil,
            "PARTAI": selected_party,
            "ALOKASI_KURSI": alokasi,
            "SUARA_2024": suara,
            "KURSI_2024": kursi,
            "TARGET_TAMBAHAN_KURSI": kursi,
            "PARTAI_K2_TERENDAH": partai_k2,
            "SUARA_K2": suara_k2
        })

    return pd.DataFrame(dapil_result)

def get_all_kriteria_combined(df_suara, df_kursi, df_dapil, selected_party):
    raw_kriteria = [
        generate_kriteria_1(df_suara, df_kursi, df_dapil, selected_party),
        generate_kriteria_2(df_suara, df_kursi, df_dapil, selected_party),
        generate_kriteria_3(df_suara, df_kursi, df_dapil, selected_party),
        generate_kriteria_4(df_suara, df_kursi, df_dapil, selected_party),
    ]

    dataframes = []
    for i, df in enumerate(raw_kriteria, start=1):
        if not df.empty:
            df = df.copy()
            df["KRITERIA"] = i
            dataframes.append(df)

    if not dataframes:
        return pd.DataFrame()

    df_all = pd.concat(dataframes, ignore_index=True)
    df_all = df_all.drop_duplicates(subset=["DAPIL"], keep="first")
    df_all = df_all.sort_values(by="DAPIL")

    return df_all