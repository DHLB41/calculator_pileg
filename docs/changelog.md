# CHANGELOG: Simulasi Kalkulasi Pemilu 2029

---

## [1.0.0] - 26 April 2025
### Initial Stable Release

#### Fitur Utama
- Input Partai, Target Kursi, Proporsi Kenaikan Suara.
- Simulasi Seleksi Dapil berdasarkan Kriteria.
- Estimasi SP dan RAB per Dapil.
- Simulasi Sainte-Laguë untuk Pembagian Kursi.
- Menampilkan Daftar Caleg Terpilih.
- Download Ringkasan Hasil Kalkulasi (HTML Output).

#### Visual & UX
- Styling Streamlit dengan `assets/styles.css`.
- Scrollable Table dengan `centered-table` format.
- Metric Cards styled untuk Total Target Suara, Kursi, dan RAB.
- Divider dan Badge terintegrasi untuk konsistensi tampilan.

#### Export & Struktur Data
- Output HTML terstruktur:
  - Grouping: Gugusan ➔ Provinsi ➔ Dapil.
  - Kolom: Dapil, Alokasi Kursi, Kursi 2024, Target Kursi 2029, Suara 2024, Target Suara 2029, Total SP, Total RAB.
- Penambahan kolom "Total SP" dalam tabel output.

#### Dokumentasi
- README.md untuk overview aplikasi.
- Setup.sh untuk environment otomatis.
- Usage Guide, Structure Overview, dan FAQ di dalam folder `docs/`.

#### Bug Fixes
- Konsistensi Heading/Subheading dengan `section-heading` class.
- Validasi struktur file Excel.
- Handling data kosong di simulasi Sainte-Laguë dan Caleg Terpilih.

---

## Planned for Next Versions

### [1.1.0] (Planned)
- Export Ringkasan langsung ke PDF via WeasyPrint.
- Filtering Dapil berdasarkan Provinsi di UI.
- Highlight otomatis Dapil prioritas.
- Multi-Partai Simulasi (Analisis serentak lebih dari satu partai).
- Penyempurnaan style untuk output cetak profesional.

---

> "Perubahan kecil hari ini adalah fondasi kemenangan besar esok hari."

---

**End of CHANGELOG**
