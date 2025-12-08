import os
import requests
from flask import Flask, request, abort
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage, MessageEvent, TextMessage

# ======================
# LOAD ENV
# ======================
load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")
OWM_API_KEY = os.getenv("OWM_API_KEY")

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    raise RuntimeError("ENV tidak terbaca! Pastikan .env 1 folder dengan app.py")

# ======================
# INIT LINE API
# ======================
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

app = Flask(__name__)

# ======================
# AQI HELPERS
# ======================
def get_geo(city):
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": OWM_API_KEY}
    r = requests.get(url, params=params)
    if r.status_code != 200 or not r.json():
        return None
    d = r.json()[0]
    return d["lat"], d["lon"], d["name"]

def get_aqi(lat, lon):
    url = "http://api.openweathermap.org/data/2.5/air_pollution"
    params = {"lat": lat, "lon": lon, "appid": OWM_API_KEY}
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return None
    comp = r.json()["list"][0]["components"]
    pm25 = comp["pm2_5"]
    # konversi pm2.5 → AQI
    aqi = int((pm25 / 12) * 50) if pm25 <= 12 else int(50 + (pm25 - 12) * 2)
    return pm25, aqi

def mask_reco(aqi):
    if aqi <= 50: return "Udara bagus, aman 👍"
    if aqi <= 100: return "Masih aman, tapi tetap waspada."
    if aqi <= 150: return "Disarankan memakai masker (N95)."
    return "SANGAT disarankan memakai masker N95!"

# ======================
# LINE CALLBACK
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
# MESSAGE HANDLER
# ======================
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    txt = event.message.text.lower()

    if txt.startswith("cek "):
        city = txt.replace("cek ", "").strip()
        geo = get_geo(city)
        if not geo:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Kota tidak ditemukan"))
            return

        lat, lon, name = geo
        data = get_aqi(lat, lon)

        if not data:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text="Gagal mengambil AQI"))
            return

        pm25, aqi = data
        rec = mask_reco(aqi)

        msg = (
            f"Kualitas Udara {name}\n"
            f"• PM2.5 : {pm25}\n"
            f"• AQI Perkiraan : {aqi}\n\n"
            f"Rekomendasi: {rec}"
        )

        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
        return

    line_bot_api.reply_message(event.reply_token, TextSendMessage(
        text="Ketik: cek <nama kota>\nContoh: cek Jakarta"
    ))

# ======================
# RUN SERVER
# ======================
if __name__ == "__main__":
    app.run(port=5000)
