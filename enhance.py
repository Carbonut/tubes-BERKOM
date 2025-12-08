import os
import requests
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage
from bs4 import BeautifulSoup

# ======================
# LOAD ENV
# ======================
load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    raise RuntimeError("ENV tidak terbaca! Pastikan file .env benar.")

# ======================
# INIT LINE API
# ======================
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask(__name__)

# ======================
# ARRAY + MAPPING URL AQICN
# ======================
KOTA_AQI = {
    "jakarta": "https://aqicn.org/city/jakarta/",
    "bandung": "https://aqicn.org/city/bandung/",
    "surabaya": "https://aqicn.org/city/surabaya/",
    "medan": "https://aqicn.org/city/medan/",
    "semarang": "https://aqicn.org/city/semarang/",
    "yogyakarta": "https://aqicn.org/city/yogyakarta/",
    "malang": "https://aqicn.org/city/malang/",
    "depok": "https://aqicn.org/city/depok/",
    "bekasi": "https://aqicn.org/city/bekasi/"
}

# ======================
# SUBPROGRAM SCRAPING AQICN
# ======================
def get_aqi_scraping(kota):
    kota = kota.lower()

    # PERCABANGAN
    if kota not in KOTA_AQI:
        return None

    url = KOTA_AQI[kota]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=15)

    if r.status_code != 200:
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # Selector AQI yang STABIL di AQICN
    aqi_tag = soup.find("div", id="aqiwgtvalue")

    if not aqi_tag:
        return None

    aqi = int(aqi_tag.text.strip())
    return aqi

# ======================
# SUBPROGRAM REKOMENDASI
# ======================
def rekomendasi_masker(aqi):
    if aqi <= 50:
        return "Udara bagus, aman tanpa masker ✅"
    elif aqi <= 100:
        return "Sedang, masker disarankan 😷"
    elif aqi <= 150:
        return "Tidak sehat untuk kelompok sensitif ⚠️"
    else:
        return "Tidak sehat! Wajib masker N95 🚨"

# ======================
# SUBPROGRAM MENU (ARRAY + LOOP)
# ======================
def menu_bantuan():
    menu = [
        "=== MENU BOT AQI ===",
        "1. Ketik: menu",
        "2. Ketik: cek <nama kota>",
        "3. Contoh: cek jakarta",
        "",
        "Daftar kota tersedia:"
    ]

    hasil = ""
    for m in menu:   # LOOPING
        hasil += m + "\n"

    for kota in KOTA_AQI:  # LOOPING ARRAY
        hasil += f"- {kota}\n"

    return hasil

# ======================
# CALLBACK
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
# HANDLER PESAN
# ======================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    pesan = event.message.text.lower()

    if pesan == "menu":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=menu_bantuan())
        )
        return

    if pesan.startswith("cek "):
        kota = pesan.replace("cek ", "").strip()

        aqi = get_aqi_scraping(kota)

        if not aqi:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="Kota tidak tersedia.\nKetik: menu")
            )
            return

        rekomendasi = rekomendasi_masker(aqi)

        hasil = (
            f"📍 Kota: {kota.title()}\n"
            f"📊 AQI: {aqi}\n\n"
            f"✅ Rekomendasi:\n{rekomendasi}"
        )

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=hasil)
        )
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Perintah tidak dikenali.\nKetik: menu")
    )

# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    app.run(port=5000)
