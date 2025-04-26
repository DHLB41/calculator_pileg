# FAQ (Frequently Asked Questions)

---

##  Umum

**Q: Apa itu Simulasi Kalkulasi Pemilu 2029?**
> A: Ini adalah aplikasi berbasis Streamlit untuk menghitung kebutuhan suara, target kursi, dan estimasi biaya kampanye berdasarkan analisis dapil Pemilu 2029.

**Q: Platform apa yang digunakan untuk menjalankan aplikasi ini?**
> A: Aplikasi berbasis Python dan Streamlit. Anda bisa menjalankan di laptop/PC lokal atau deploy ke server cloud.

**Q: Data apa yang digunakan?**
> A: Data berasal dari file `data_calculated.xlsx` yang berisi informasi suara 2024, alokasi kursi, dapil, dan detail simulasi Sainte-Laguë.

---

## Teknis

**Q: Bagaimana cara menjalankan aplikasi ini?**
> A: Cukup jalankan perintah `bash setup.sh`, lalu `streamlit run app.py` dari terminal.

**Q: Saya mendapat error "Missing columns" saat upload data?**
> A: Pastikan file `data_calculated.xlsx` memuat semua sheet yang diperlukan: `suara`, `kursi`, `dapil`, dan `detail_sl`, dengan struktur kolom yang sesuai.

**Q: Apakah aplikasi ini bisa export ke PDF?**
> A: Saat ini export default ke HTML. Untuk export PDF, Anda bisa menggunakan fitur print ke PDF dari browser (`Ctrl+P` atau `⌘+P`). Roadmap ke depan akan mendukung export PDF otomatis.

**Q: Apakah hasil Sainte-Laguë bisa diubah manual?**
> A: Tidak. Kalkulasi Sainte-Laguë berdasarkan algoritma tetap untuk memastikan akurasi simulasi distribusi kursi.

---

## Data & Output

**Q: Kenapa hanya provinsi yang tampil, bukan gugusan?**
> A: Untuk menjaga kesederhanaan visual. Gugusan tetap dipakai di backend sebagai dasar grouping, tapi output fokus menampilkan provinsi saja.

**Q: Kolom "Total SP" itu apa?**
> A: Total SP adalah total suara tambahan yang diperlukan untuk mempertahankan/memperbesar peluang kursi tambahan di masing-masing dapil.

**Q: Bisa memilih lebih dari satu partai?**
> A: Saat ini aplikasi hanya mendukung simulasi satu partai per sesi. Roadmap pengembangan ke depan akan mendukung multi-partai.

---

## Bantuan

**Q: Jika saya menemukan bug atau error, kemana harus melapor?**
> A: Silakan hubungi kami melalui:
> - 📧 Email: risad.tristan@gmail.com
> - 📱 WhatsApp: +62 812 9585 7514

**Q: Apakah saya bisa berkontribusi?**
> A: Tentu! Kami terbuka untuk kontribusi pengembangan. Silakan hubungi kontak yang tersedia.

---

> "Pertanyaan kecil menghasilkan pengembangan besar."

---

**End of FAQ**
