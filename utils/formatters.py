import re

def format_ribuan(x):
    """
    Format angka menjadi ribuan dengan titik sebagai pemisah.
    Contoh: 10000 → '10.000'
    """
    try:
        return f"{int(x):,}".replace(",", ".")
    except:
        return x

def format_persen(x):
    """
    Format angka menjadi persen 2 digit desimal.
    Contoh: 13.456 → '13.46 %'
    """
    try:
        return f"{float(x):.2f} %"
    except:
        return x

def roman_to_int(roman):
    """
    Konversi angka romawi ke integer.
    """
    roman_dict = {
        "I": 1, "II": 2, "III": 3, "IV": 4, "V": 5,
        "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10,
        "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15,
        "XVI": 16, "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20
    }
    return roman_dict.get(roman.strip().upper(), 0)

def extract_roman_order(dapil_name):
    """
    Ambil angka romawi di akhir nama DAPIL dan konversi ke integer.
    Contoh: 'Jawa Barat II' → 2
    """
    match = re.search(
        r"(I{1,3}|IV|V|VI{0,3}|IX|X|XI{0,3}|XIV|XV|XVI|XVII|XVIII|XIX|XX)$",
        dapil_name.strip(), re.IGNORECASE
    )
    return roman_to_int(match.group()) if match else 0