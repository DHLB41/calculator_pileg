import pandas as pd
from utils.sainte_lague import simulasi_sainte_lague

PARTAI_TERPILIH = ["PKB", "GERINDRA", "PDIP", "GOLKAR", "NASDEM", "PKS", "PAN", "DEMOKRAT"]

def generate_kriteria_1(df_suara, df_kursi, df_dapil, selected_party):
    dapil_result = []

    for dapil in df_suara["DAPIL"].tolist():
        alokasi_row = df_dapil[df_dapil["DAPIL"] == dapil]
        if alokasi_row.empty:
            continue

        alokasi = int(alokasi_row["ALOKASI KURSI"].values[0])
        kursi_partai = df_kursi[df_kursi["DAPIL"] == dapil]
        suara_partai = df_suara[df_suara["DAPIL"] == dapil]

        if suara_partai.empty:
            continue

        kursi = 0
        if not kursi_partai.empty and selected_party in kursi_partai.columns:
            kursi = int(kursi_partai[selected_party].values[0])

        suara = int(suara_partai[selected_party].values[0])

        if kursi != 0:
            continue

        partai_lolos = PARTAI_TERPILIH.copy()
        if selected_party not in partai_lolos:
            partai_lolos.append(selected_party)

        urutan_kursi, _ = simulasi_sainte_lague(dapil, alokasi, df_suara, partai_lolos)
        if len(urutan_kursi) < 2:
            continue

        partai_k2 = urutan_kursi[-2]
        suara_k2 = int(suara_partai[partai_k2].values[0])
        total_target_suara = int(suara_k2 * 1.1)

        dapil_result.append({
            "DAPIL": dapil,
            "PARTAI": selected_party,
            "ALOKASI_KURSI": alokasi,
            "SUARA_2024": suara,
            "KURSI_2024": kursi,
            "TARGET_TAMBAHAN_KURSI": 1,
            "PARTAI_K2_TERENDAH": partai_k2,
            "SUARA_K2": suara_k2,
            "TOTAL_TARGET_SUARA_2029": total_target_suara
        })

    return pd.DataFrame(dapil_result)


def generate_kriteria_2(df_suara, df_kursi, df_dapil, selected_party):
    dapil_result = []

    for dapil in df_suara["DAPIL"].tolist():
        alokasi_row = df_dapil[df_dapil["DAPIL"] == dapil]
        if alokasi_row.empty:
            continue

        alokasi = int(alokasi_row["ALOKASI KURSI"].values[0])
        kursi_partai = df_kursi[df_kursi["DAPIL"] == dapil]
        suara_partai = df_suara[df_suara["DAPIL"] == dapil]

        if suara_partai.empty:
            continue

        kursi = 0
        if not kursi_partai.empty and selected_party in kursi_partai.columns:
            kursi = int(kursi_partai[selected_party].values[0])

        suara = int(suara_partai[selected_party].values[0])

        if kursi != 1:
            continue

        urutan_kursi, _ = simulasi_sainte_lague(dapil, alokasi, df_suara, PARTAI_TERPILIH)
        if len(urutan_kursi) < 2:
            continue

        partai_k2 = urutan_kursi[-2]
        if partai_k2 not in ["PAN", "DEMOKRAT"]:
            continue

        suara_k2 = int(suara_partai[partai_k2].values[0])
        total_target_suara = int(suara_k2 * 3 * 1.1)
        target_kursi = 1 if alokasi <= 4 else 1 + kursi

        dapil_result.append({
            "DAPIL": dapil,
            "PARTAI": selected_party,
            "ALOKASI_KURSI": alokasi,
            "SUARA_2024": suara,
            "KURSI_2024": kursi,
            "TARGET_TAMBAHAN_KURSI": target_kursi,
            "PARTAI_K2_TERENDAH": partai_k2,
            "SUARA_K2": suara_k2,
            "TOTAL_TARGET_SUARA_2029": total_target_suara
        })

    return pd.DataFrame(dapil_result)


def generate_kriteria_3(df_suara, df_kursi, df_dapil, selected_party):
    dapil_result = []

    for dapil in df_suara["DAPIL"].tolist():
        alokasi_row = df_dapil[df_dapil["DAPIL"] == dapil]
        if alokasi_row.empty:
            continue

        alokasi = int(alokasi_row["ALOKASI KURSI"].values[0])
        kursi_partai = df_kursi[df_kursi["DAPIL"] == dapil]
        suara_partai = df_suara[df_suara["DAPIL"] == dapil]

        if suara_partai.empty:
            continue

        kursi = 0
        if not kursi_partai.empty and selected_party in kursi_partai.columns:
            kursi = int(kursi_partai[selected_party].values[0])

        suara = int(suara_partai[selected_party].values[0])

        if kursi != 1:
            continue

        urutan_kursi, _ = simulasi_sainte_lague(dapil, alokasi, df_suara, PARTAI_TERPILIH)
        if len(urutan_kursi) < 2:
            continue

        partai_k2 = urutan_kursi[-2]
        suara_k2 = int(suara_partai[partai_k2].values[0])
        total_target_suara = int(suara_k2 * 3 * 1.1)
        target_kursi = 1 if alokasi <= 4 else 1 + kursi

        dapil_result.append({
            "DAPIL": dapil,
            "PARTAI": selected_party,
            "ALOKASI_KURSI": alokasi,
            "SUARA_2024": suara,
            "KURSI_2024": kursi,
            "TARGET_TAMBAHAN_KURSI": target_kursi,
            "PARTAI_K2_TERENDAH": partai_k2,
            "SUARA_K2": suara_k2,
            "TOTAL_TARGET_SUARA_2029": total_target_suara
        })

    return pd.DataFrame(dapil_result)


def generate_kriteria_4(df_suara, df_kursi, df_dapil, selected_party):
    dapil_result = []

    for dapil in df_suara["DAPIL"].tolist():
        alokasi_row = df_dapil[df_dapil["DAPIL"] == dapil]
        if alokasi_row.empty:
            continue

        alokasi = int(alokasi_row["ALOKASI KURSI"].values[0])
        kursi_partai = df_kursi[df_kursi["DAPIL"] == dapil]
        suara_partai = df_suara[df_suara["DAPIL"] == dapil]

        if suara_partai.empty:
            continue

        kursi = 0
        if not kursi_partai.empty and selected_party in kursi_partai.columns:
            kursi = int(kursi_partai[selected_party].values[0])

        suara = int(suara_partai[selected_party].values[0])

        if kursi <= 1:
            continue

        urutan_kursi, _ = simulasi_sainte_lague(dapil, alokasi, df_suara, PARTAI_TERPILIH)
        if len(urutan_kursi) < 2:
            continue

        partai_k2 = urutan_kursi[-2]
        suara_k2 = int(suara_partai[partai_k2].values[0])
        total_target_suara = int(suara_k2 * 3 * 1.1)

        dapil_result.append({
            "DAPIL": dapil,
            "PARTAI": selected_party,
            "ALOKASI_KURSI": alokasi,
            "SUARA_2024": suara,
            "KURSI_2024": kursi,
            "TARGET_TAMBAHAN_KURSI": kursi,
            "PARTAI_K2_TERENDAH": partai_k2,
            "SUARA_K2": suara_k2,
            "TOTAL_TARGET_SUARA_2029": total_target_suara
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
        if not df.empty and "TOTAL_TARGET_SUARA_2029" in df.columns:
            df = df.copy()
            df["KRITERIA"] = i
            dataframes.append(df)

    if not dataframes:
        return pd.DataFrame()

    df_all = pd.concat(dataframes, ignore_index=True)
    df_all = df_all.sort_values(by="TOTAL_TARGET_SUARA_2029", ascending=True)
    df_all = df_all.drop_duplicates(subset=["DAPIL"], keep="first")

    return df_all