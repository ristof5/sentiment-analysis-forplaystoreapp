# Sentiment Analysis for Play Store App

Web aplikasi berbasis Flask untuk menganalisis sentimen pengguna terhadap aplikasi Play Store berdasarkan ulasan dan rating yang diberikan.

## 📌 Fitur

- Upload file CSV yang berisi data ulasan aplikasi
- Menampilkan hasil analisis dalam tabel (preview 25 data pertama)
- Visualisasi sentimen dengan:
  - Pie chart distribusi sentimen
  - Word cloud untuk masing-masing kategori sentimen
- Download hasil analisis dalam format CSV

## 🗂️ Struktur File CSV yang Didukung

Pastikan file CSV memiliki kolom berikut agar kompatibel dengan aplikasi:

- `Komentar`
- `Nama Pengguna`
- `Rating`
- `Tanggal`
- `Nama Aplikasi`

Contoh struktur CSV:

| Komentar | Nama Pengguna | Rating | Tanggal | Nama Aplikasi |
|----------|----------------|--------|---------|----------------|
| Aplikasinya bagus | user123 | 5 | 2024-03-01 | InfoBMKG |

## 🎈 Demo

Ini merupakan ini link demonya https://riffani.pythonanywhere.com/
