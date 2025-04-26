import pandas as pd

def simulasi_sainte_lague(dapil_nama, alokasi_kursi, df_suara, partai_lolos):
    """
    Melakukan simulasi Sainte-Laguë untuk satu Dapil.
    Mengembalikan daftar urutan partai pemenang kursi dan distribusi kursi per partai.
    """
    alokasi_kursi = int(alokasi_kursi)
    baris = df_suara[df_suara["DAPIL"] == dapil_nama]
    if baris.empty:
        return [], {}

    hasil_bagi = []
    for partai in partai_lolos:
        try:
            suara = int(baris[partai].values[0])
        except (KeyError, ValueError, TypeError):
            continue
        for pembagi in range(1, alokasi_kursi * 2, 2):
            hasil_bagi.append((partai, suara / pembagi))

    hasil_bagi.sort(key=lambda x: x[1], reverse=True)
    alokasi = hasil_bagi[:alokasi_kursi]

    hasil_akhir = {}
    for partai, _ in alokasi:
        hasil_akhir[partai] = hasil_akhir.get(partai, 0) + 1

    urutan_kursi = [p[0] for p in alokasi]
    return urutan_kursi, hasil_akhir


def partai_kursi_ke_2_terbawah(dapil_nama, alokasi_kursi, df_suara, partai_lolos):
    """
    Mengembalikan nama partai yang mendapatkan kursi ke-2 terbawah di Dapil.
    """
    urutan_kursi, _ = simulasi_sainte_lague(dapil_nama, alokasi_kursi, df_suara, partai_lolos)
    return urutan_kursi[-2] if len(urutan_kursi) >= 2 else None


def hitung_detail_kursi(dapil_nama, alokasi_kursi, df_suara, partai_lolos, df_detail_sl=None):
    """
    Menghasilkan tabel detail hasil Sainte-Laguë (full semua baris pembagi),
    dengan kolom URUTAN KURSI hanya diisi untuk pemenang.
    Output: DAPIL, URUTAN KURSI, PARTAI, PEMBAGI, PEROLEHAN SUARA, NILAI BAGI
    """
    alokasi_kursi = int(alokasi_kursi)
    baris = df_suara[df_suara["DAPIL"] == dapil_nama]
    if baris.empty:
        return pd.DataFrame()

    hasil_bagi = []

    # Hitung seluruh pembagian suara
    for partai in partai_lolos:
        try:
            suara = int(baris[partai].values[0])
        except (KeyError, ValueError, TypeError):
            continue

        for pembagi in range(1, alokasi_kursi * 2, 2):
            hasil_bagi.append({
                "DAPIL": dapil_nama,
                "PARTAI": partai,
                "PEMBAGI": pembagi,
                "PEROLEHAN SUARA": suara,
                "NILAI BAGI": suara / pembagi
            })

    # Urutkan berdasarkan nilai bagi
    hasil_sorted = sorted(hasil_bagi, key=lambda x: x["NILAI BAGI"], reverse=True)

    # Tandai pemenang kursi
    for i in range(min(alokasi_kursi, len(hasil_sorted))):
        hasil_sorted[i]["URUTAN KURSI"] = i + 1

    # Buat dataframe akhir
    df_final = pd.DataFrame(hasil_sorted)
    df_final = df_final[
        ["DAPIL", "URUTAN KURSI", "PARTAI", "PEMBAGI", "PEROLEHAN SUARA", "NILAI BAGI"]
    ].sort_values(by="NILAI BAGI", ascending=False).reset_index(drop=True)

    return df_final