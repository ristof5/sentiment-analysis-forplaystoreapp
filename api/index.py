from flask import Flask, render_template, request, send_file
import pandas as pd
import os
import matplotlib.pyplot as plt
from wordcloud import WordCloud

app = Flask(__name__)

# Pastikan folder static ada
UPLOAD_FOLDER = "static"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Fungsi Label Sentimen
def label_sentiment(rating):
    if rating <= 2:
        return "Negatif"
    elif rating == 3:
        return "Netral"
    else:
        return "Positif"

@app.route("/", methods=["GET", "POST"])
def index():
    data_preview = None  
    pie_chart_path = None
    wordcloud_paths = {}
    total_rows = 0  # Untuk menghitung total komentar

    if request.method == "POST":
        if "file" not in request.files:
            return "Tidak ada file yang diunggah"

        file = request.files["file"]
        if file.filename == "":
            return "Pilih file terlebih dahulu"

        if file and file.filename.endswith(".csv"):
            df = pd.read_csv(file)
            required_columns = {"Komentar", "Nama Pengguna", "Rating", "Tanggal", "Nama Aplikasi"}

            if not required_columns.issubset(df.columns):
                return f"File CSV harus memiliki kolom: {', '.join(required_columns)}"

            # Pastikan rating dalam bentuk angka
            df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

            # Hapus baris dengan rating NaN
            df = df.dropna(subset=["Rating"])

            # Terapkan analisis sentimen berdasarkan rating
            df["Sentimen"] = df["Rating"].apply(label_sentiment)

            # Hitung total komentar
            total_rows = len(df)

            # Simpan hasil analisis
            output_file = os.path.join(UPLOAD_FOLDER, "hasil.csv")
            df.to_csv(output_file, index=False)

            # Ambil hanya 25 data pertama untuk ditampilkan
            data_preview = df.head(5).to_dict(orient="records")

            # Hitung jumlah sentimen untuk pie chart
            sentiment_counts = df["Sentimen"].value_counts()

            # Buat Pie Chart
            plt.figure(figsize=(6, 6))
            plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct="%1.1f%%", startangle=90)
            plt.title("Distribusi Sentimen")
            plt.axis("equal")
            pie_chart_path = os.path.join(UPLOAD_FOLDER, "pie_chart.png")
            plt.savefig(pie_chart_path)
            plt.close()

            # Generate WordClouds untuk tiap sentimen
            for sentiment, color in [("Positif", "Greens"), ("Negatif", "Reds"), ("Netral", "Wistia")]:
                text = " ".join(df[df["Sentimen"] == sentiment]["Komentar"].astype(str))
                wordcloud = WordCloud(width=800, height=400, colormap=color, background_color="black").generate(text)

                wc_path = os.path.join(UPLOAD_FOLDER, f"wordcloud_{sentiment.lower()}.png")
                wordcloud.to_file(wc_path)
                wordcloud_paths[sentiment] = wc_path

    return render_template(
        "index.html",
        data_preview=data_preview,
        total_rows=total_rows,  # Menampilkan jumlah total komentar
        pie_chart=pie_chart_path,
        wordclouds=wordcloud_paths,
        file_download="static/hasil.csv"
    )

@app.route("/download")
def download_file():
    return send_file("static/hasil.csv", as_attachment=True)

def handler(environ, start_response):
    return app(environ, start_response)
