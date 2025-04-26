<p align="center">
  <img src="assets/logo_prodata.png" alt="Prodata Logo" width="160"/>
</p>

<h1 align="center">📊 Kalkulator Kebutuhan Suara Pemilu 2029</h1>
<p align="center"><em>Simulasi strategis berbasis Sainte-Laguë untuk proyeksi kebutuhan kursi legislatif</em></p>

<p align="center">
  <a href="https://streamlit.io/">
    <img src="https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/License-Private-important?style=for-the-badge&logo=read-the-docs&logoColor=white" alt="License">
  </a>
</p>

---

# Simulasi Kalkulasi Kebutuhan Suara Pemilu 2029

Selamat datang di **Simulasi Kalkulasi Pemilu 2029**! 🚀
Aplikasi ini membantu Anda menghitung kebutuhan suara, kursi, dan biaya kampanye untuk target pemenangan Pemilu Legislatif 2029, berdasarkan simulasi strategis per dapil.

---

## Fitur Utama

- **Input Strategis:**
  - Pemilihan Partai.
  - Input Target Kursi 2029.
  - Penyesuaian Proporsi Kenaikan Suara per Kursi.

- **Seleksi Dapil Potensial:**
  - Filtering otomatis berdasarkan kriteria strategis.
  - Eliminasi dapil manual dengan sistem pengganti otomatis.

- **Simulasi Sainte-Laguë:**
  - Pembagian kursi berdasarkan suara aktual.

- **Daftar Caleg Terpilih:**
  - Caleg-caleg yang mendapatkan kursi di tiap dapil.

- **Download Ringkasan:**
  - Ekspor ke file HTML siap cetak.
  - Struktur pengelompokan berdasarkan Gugusan ➔ Provinsi.
  - Tambahan kolom **Total SP** di tabel ringkasan.

---

## Alur Penggunaan

1. **Pilih Partai** yang akan dianalisis.
2. **Masukkan Target Kursi** yang ingin dicapai di Pemilu 2029.
3. **Atur Proporsi Kenaikan Suara** per tambahan kursi.
4. **Isi Estimasi Biaya Kampanye** (per suara, manajemen, pendampingan).
5. **Review Dapil Potensial** yang disarankan oleh sistem.
6. **Eliminasi dapil** (opsional) jika perlu, sistem otomatis mencari pengganti.
7. **Lihat Simulasi Sainte-Laguë** untuk pembagian kursi.
8. **Download Ringkasan** hasil kalkulasi dalam format HTML.
9. **(Opsional)** Cetak hasil ke PDF dengan Ctrl + P (Windows) / ⌘ + P (Mac).

---

## Struktur Folder

```plaintext
├── app.py                  # Main Streamlit App
├── components/             # Komponen modular UI
├── utils/                  # Utility functions (formatter, calculation, export)
├── assets/
│   └── styles.css           # Styling custom untuk Streamlit
├── data_calculated.xlsx    # Source Data (Suara, Kursi, Dapil, Detail SL)
├── README.md               # Ini file yang sedang Anda baca
```

---

## Tech Stack

- **Python 3.9+**
- **Streamlit** - Frontend Framework
- **Pandas** - Data Processing
- **Custom HTML/CSS** - Output Formatting

---

## Future Enhancement

- [ ] Export langsung ke PDF.
- [ ] Auto-filter Dapil berdasarkan Provinsi/Wilayah di UI.
- [ ] Support Multi-Partai Analisis.
- [ ] Highlight otomatis untuk dapil prioritas tinggi.

---

## Kontak

Untuk pertanyaan atau kontribusi, silakan hubungi:

- 📧 Email: risad.tristan@gmail.com
- 📱 WhatsApp: +62 812 9585 7514

---

> "Data yang tepat adalah kunci kemenangan di medan politik."

---

Terima kasih telah menggunakan **Simulasi Kalkulasi Pemilu 2029**! 🎉🇮🇩


> © 2025 Prodata Indonesia — All Rights Reserved
