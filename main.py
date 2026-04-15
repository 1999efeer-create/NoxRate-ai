import os, requests
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

# --- AYARLAR ---
K = 'AIzaSyDD_eoF59ajl9pHuik-bxxQSdw8V-zPnEs' 
T = '8665581548:AAGnU06mVY6BK0TVXWPbszsgnmNqyywkBc' 

app = Flask('')
@app.route('/')
def home(): return "Zynx Bot Aktif"

async def handle(update, context):
    q = ' '.join(context.args)
    if not q: return
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={K}"
    payload = {"contents": [{"parts": [{"text": q}]}]}
    
    try:
        r = requests.post(url, json=payload)
        data = r.json()
        if "candidates" in data:
            msg = data["candidates"][0]["content"]["parts"][0]["text"]
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("Google şu an cevap vermiyor, 5 dk sonra tekrar dene knk.")
    except:
        await update.message.reply_text("Sistemde bir hata oldu.")

def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

app_tg = ApplicationBuilder().token(T).build()
app_tg.add_handler(CommandHandler("sor", handle))
app_tg.run_polling()
