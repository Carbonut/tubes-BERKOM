import os
import requests
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage

# ======================
# LOAD ENV (VARIABEL LINGKUNGAN)
# ======================
load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
OWM_API_KEY = os.getenv("OWM_API_KEY")

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET or not OWM_API_KEY:
    raise RuntimeError("ENV tidak terbaca! Pastikan file .env sudah diisi.")

# ======================
# INISIALISASI LINE BOT
# ======================
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask(__name__)

# ======================
# SUBPROGRAM 1: AMBIL KOORDINAT KOTA
# ======================
def get_geo(city):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": OWM_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code != 200 or not response.json():
        return None

    data = response.json()[0]
    return data["lat"], data["lon"], data["name"]

# ======================
# SUBPROGRAM 2: AMBIL DATA AQI
# ======================
def get_aqi(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": OWM_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None

    components = response.json()["list"][0]["components"]
    pm25 = components["pm2_5"]

    # ======================
    # PERCABANGAN (IF ELSE)
    # ======================
    if pm25 <= 12:
        aqi = int((pm25 / 12) * 50)
    else:
        aqi = int(50 + (pm25 - 12) * 2)

    return pm25, aqi

# ======================
# SUBPROGRAM 3: REKOMENDASI MASKER
# ======================
def rekomendasi_masker(aqi):
    if aqi <= 50:
        return "Udara bagus, aman tanpa masker 👍"
    elif aqi <= 100:
        return "Masih cukup aman, tetap waspada."
    elif aqi <= 150:
        return "Disarankan memakai masker (N95)."
    else:
        return "SANGAT disarankan memakai masker N95 dan kurangi aktivitas luar!"

# ======================
# SUBPROGRAM 4: MENU BANTUAN (ARRAY + LOOPING)
# ======================
def menu_bantuan():
    menu = [
        "Ketik: cek <nama kota>",
        "Contoh: cek jakarta",
        "Bot ini menampilkan:",
        "- PM2.5",
        "- AQI",
        "- Rekomendasi masker"
    ]

    hasil = "=== MENU BOT AQI ===\n"
    for item in menu:   # <-- LOOPING
        hasil += item + "\n"

    return hasil

# ======================
# WEBHOOK CALLBACK
# ======================
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

# ======================
# HANDLER PESAN (PERCABANGAN UTAMA)
# ======================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    pesan = event.message.text.lower()

    # ======================
    # JIKA USER KETIK "menu"
    # ======================
    if pesan == "menu":
        reply = menu_bantuan()
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        return

    # ======================
    # JIKA USER KETIK "cek kota"
    # ======================
    if pesan.startswith("cek "):
        kota = pesan.replace("cek ", "").strip()

        data_geo = get_geo(kota)
        if not data_geo:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Kota tidak ditemukan!")
            )
            return

        lat, lon, nama_kota = data_geo
        data_aqi = get_aqi(lat, lon)

        if not data_aqi:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Gagal mengambil data AQI.")
            )
            return

        pm25, aqi = data_aqi
        rekomendasi = rekomendasi_masker(aqi)

        hasil = (
            f"📍 Kota: {nama_kota}\n"
            f"🌫 PM2.5 : {pm25}\n"
            f"📊 AQI : {aqi}\n\n"
            f"✅ Rekomendasi:\n{rekomendasi}"
        )

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=hasil))
        return

    # ======================
    # JIKA FORMAT SALAH
    # ======================
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Perintah tidak dikenali.\nKetik: menu")
    )

# ======================
# JALANKAN SERVER
# ======================
if __name__ == "__main__":
    app.run(port=5000)
