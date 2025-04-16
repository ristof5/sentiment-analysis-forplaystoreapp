from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64

app = Flask(__name__)

def label_sentiment(rating):
    if rating <= 2:
        return "Negatif"
    elif rating == 3:
        return "Netral"
    else:
        return "Positif"

def create_pie_chart(df):
    sentiments = df['Sentimen'].value_counts()
    plt.figure(figsize=(6, 6))
    plt.pie(sentiments, labels=sentiments.index, autopct='%1.1f%%', startangle=90)
    plt.title("Distribusi Sentimen")
    plt.axis('equal')

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", transparent=True)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    plt.close()
    return img_base64

def generate_wordcloud(df, colormap):
    text = ' '.join(df['Komentar'].astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color='black', colormap=colormap).generate(text)
    
    buf = io.BytesIO()
    plt.figure(figsize=(8, 4))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(buf, format="png", transparent=True)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    plt.close()
    return img_base64

@app.route("/", methods=["GET", "POST"])
def index():
    data_preview = None
    pie_chart_base64 = None
    wordcloud_positif = None
    wordcloud_netral = None
    wordcloud_negatif = None
    total_rows = 0

    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            required_cols = {"Komentar", "Nama Pengguna", "Rating", "Tanggal", "Nama Aplikasi"}
            if not required_cols.issubset(df.columns):
                return "Kolom tidak sesuai. Harus ada: Komentar, Nama Pengguna, Rating, Tanggal, Nama Aplikasi"

            df["Sentimen"] = df["Rating"].apply(label_sentiment)
            total_rows = len(df)
            data_preview = df.head(25).to_dict(orient="records")
            pie_chart_base64 = create_pie_chart(df)

            positif_df = df[df["Sentimen"] == "Positif"]
            netral_df = df[df["Sentimen"] == "Netral"]
            negatif_df = df[df["Sentimen"] == "Negatif"]

            wordcloud_positif = generate_wordcloud(positif_df, "Greens")
            wordcloud_netral = generate_wordcloud(netral_df, "Wistia")
            wordcloud_negatif = generate_wordcloud(negatif_df, "Reds")

    return render_template("index.html", data_preview=data_preview,
                           pie_chart_base64=pie_chart_base64,
                           wordcloud_positif=wordcloud_positif,
                           wordcloud_netral=wordcloud_netral,
                           wordcloud_negatif=wordcloud_negatif,
                           total_rows=total_rows)
