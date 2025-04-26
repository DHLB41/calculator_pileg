# Usage Guide: Simulasi Kalkulasi Pemilu 2029

---

## Persiapan Awal

1. **Clone atau Download** repository aplikasi ini.
2. **Buka terminal** di direktori project.
3. **Jalankan Setup:**

```bash
bash setup.sh
```

4. **Aktifkan Virtual Environment (jika belum aktif):**

```bash
source venv/bin/activate
```

5. **Jalankan Aplikasi:**

```bash
streamlit run app.py
```

---

## Input Data

- Pastikan file `data_calculated.xlsx` tersedia di folder project.
- File ini berisi:
  - **Sheet suara:** Data suara partai per dapil.
  - **Sheet kursi:** Data perolehan kursi 2024.
  - **Sheet dapil:** Informasi dapil termasuk kolom GUGUSAN dan PROPINSI.
  - **Sheet detail_sl:** Data detail untuk simulasi Sainte-Laguë.

---

## Alur Penggunaan Aplikasi

1. **Pilih Partai** yang akan dianalisis.
2. **Input Target Kursi 2029** dan **Proporsi Kenaikan Suara**.
3. **Isi Biaya Kampanye** (per suara, manajemen, pendampingan).
4. **Review Dapil Potensial** yang dipilih otomatis.
5. **Eliminasi dapil** jika perlu ➔ sistem akan mencari pengganti.
6. **Lihat Simulasi Sainte-Laguë** untuk dapil aktif.
7. **Cek Daftar Caleg Terpilih** (jika data tersedia).
8. **Unduh Ringkasan** dalam format HTML.
9. **(Opsional)** Simpan ke PDF melalui browser: `Ctrl + P` / `⌘ + P`.

---

## Struktur Output HTML

| Kolom | Keterangan |
|:---|:---|
| Dapil | Nama Daerah Pemilihan |
| Alokasi Kursi | Jumlah alokasi kursi dapil |
| Kursi 2024 | Kursi yang dimenangkan 2024 |
| Target Kursi 2029 | Target tambahan kursi |
| Suara 2024 | Perolehan suara 2024 |
| Target Suara 2029 | Estimasi suara yang harus dicapai |
| Total SP | Total SP kebutuhan suara tambahan |
| Total RAB | Estimasi biaya kampanye |

- Data dikelompokkan berdasarkan **Wilayah ➔ Provinsi** (hanya Provinsi ditampilkan).

---

## Catatan Tambahan

- Untuk fitur ekspor PDF otomatis, dapat diaktifkan menggunakan WeasyPrint (sudah disiapkan dalam `requirements.txt`).
- Untuk pengembangan lanjutan (multi-partai, auto-highlight dapil strategis), roadmap sudah tersedia di `README.md`.

---

## 📞 Bantuan Teknis

Hubungi:
- 📧 Email: risad.tristan@gmail.com
- 📱 WhatsApp: +62 812 9585 7514

---

> "Merancang strategi, mengoptimalkan suara."

---

**Selamat menggunakan Simulasi Kalkulasi Pemilu 2029! 🇮🇩🎯**
