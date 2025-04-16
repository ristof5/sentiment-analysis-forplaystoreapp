# Sentiment Analysis for Play Store App

Web aplikasi berbasis Flask untuk menganalisis sentimen pengguna terhadap aplikasi Play Store berdasarkan ulasan dan rating yang diberikan.

## 📌 Fitur

- Upload file CSV yang berisi data ulasan aplikasi
- Analisis sentimen berdasarkan rating:
  - Rating 1–2 → Negatif
  - Rating 3 → Netral
  - Rating 4–5 → Positif
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

## 🚀 Cara Menjalankan Secara Lokal

### 1. Clone Repo

```bash
git clone https://github.com/username/sentiment-analysis-forplaystoreapp.git
cd sentiment-analysis-forplaystoreapp
