def hitung_rab_per_kursi(sp: float, angka_psikologis: int) -> int:
    """
    Hitung RAB per kursi berdasarkan SP dan angka psikologis (biaya per suara).
    """
    return int(sp * angka_psikologis)


def hitung_total_rab_per_dapil(sp_list: list, biaya_manajemen: int, biaya_pendampingan: int) -> list:
    """
    Hitung total RAB per kursi dan keseluruhan untuk satu dapil.

    Args:
        sp_list (list): List of SP_KURSI_1..4 dalam urutan
        biaya_manajemen (int): biaya manajemen tetap per dapil
        biaya_pendampingan (int): biaya pendampingan tetap per dapil

    Returns:
        list: Total RAB per kursi [RAB_1, RAB_2, RAB_3, RAB_4] dan total
    """
    rab_kursi = []
    for sp in sp_list:
        if sp > 0:
            rab = int(sp * angka_psikologis) + biaya_manajemen + biaya_pendampingan
        else:
            rab = 0
        rab_kursi.append(rab)
    total = sum(rab_kursi)
    return rab_kursi + [total]


def hitung_total_rab_all(row, angka_psikologis: int, biaya_manajemen: int, biaya_pendampingan: int) -> int:
    """
    Hitung total keseluruhan RAB untuk satu baris (dapil).
    Digunakan untuk apply per row.
    """
    total = 0
    for i in range(1, 5):
        sp = row.get(f"SP_KURSI_{i}", 0)
        if sp > 0:
            rab = sp * angka_psikologis + biaya_manajemen + biaya_pendampingan
            total += rab
    return int(total)