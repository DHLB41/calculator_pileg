# Project Structure Overview: Simulasi Kalkulasi Pemilu 2029

---

## Struktur Utama

```plaintext
├── app.py                  # Main app Streamlit, menggabungkan semua komponen
├── components/             # Modul tampilan UI modular
│   ├── partai_info.py       # Input form partai dan suara awal
│   ├── tabel_dapil.py       # Tabel persebaran suara dan kursi per dapil
│   ├── input_target.py      # Form input target kursi dan proporsi suara
│   ├── detail_dapil.py      # Rincian simulasi satu dapil, eliminasi dapil
│   ├── ringkasan_dapil.py   # Tabel ringkasan dapil terpilih
│   ├── sainte_lague.py      # Simulasi pembagian kursi metode Sainte-Laguë
│   ├── caleg_terpilih.py    # Daftar caleg per dapil
│   ├── rangkuman_metrik.py  # Metrik total suara, kursi, RAB
│   └── download_section.py  # Tombol dan ekspor ringkasan kalkulasi
├── utils/                  # Utility functions
│   ├── formatters.py        # Fungsi format angka, roman order extractor
│   ├── calculations.py      # Fungsi kalkulasi suara tambahan, SP, RAB
│   ├── sainte_lague.py      # Algoritma simulasi pembagian kursi
│   ├── validators.py        # Validasi input form pengguna
│   └── exporter.py          # Fungsi ekspor hasil kalkulasi ke HTML
├── assets/
│   └── styles.css           # Styling kustom untuk tampilan Streamlit
├── data_calculated.xlsx    # File sumber data: suara, kursi, dapil, detail Sainte-Laguë
├── requirements.txt        # Daftar dependencies project
├── setup.sh                # Script setup environment otomatis
├── README.md               # Ringkasan dan dokumentasi project
└── docs/                   # Dokumentasi tambahan
    ├── usage_guide.md       # Panduan penggunaan aplikasi
    └── structure_overview.md # Penjelasan struktur project
```

---

## Penjelasan Komponen Kunci

| Folder | Fungsi |
|:---|:---|
| **components/** | Menyimpan seluruh bagian tampilan Streamlit, dipanggil modular dari `app.py` |
| **utils/** | Menyimpan fungsi pendukung non-visual: kalkulasi, format, ekspor |
| **assets/** | Menyimpan styling CSS untuk mempercantik tampilan aplikasi |
| **data_calculated.xlsx** | Menjadi basis data untuk simulasi perhitungan |
| **docs/** | Dokumentasi internal, memudahkan kolaborasi dan pengembangan |

---

## Alur Program Singkat

1. **User membuka aplikasi Streamlit** ➔ `app.py`
2. **Formulir dipilih** ➔ dari `components/partai_info.py`
3. **Data dapil ditampilkan** ➔ `components/tabel_dapil.py`
4. **Input target kursi dan proporsi** ➔ `components/input_target.py`
5. **Simulasi dapil diproses** ➔ `utils/calculations.py`
6. **Hasil Sainte-Laguë** ➔ `components/sainte_lague.py`
7. **Output HTML ringkasan** ➔ `utils/exporter.py`

---

## Tujuan Struktur Modular Ini

- **Mudah dikembangkan** (tambah fitur baru tanpa mengganggu core).
- **Mudah dirawat** (perubahan kecil tidak berdampak ke seluruh app).
- **Profesional** (struktur sesuai standar industri pengembangan aplikasi).

---

> "Struktur yang rapi adalah fondasi aplikasi yang sukses." 🚀

---

**End of Structure Overview**
