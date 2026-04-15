import os, requests
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

# --- BİLGİLERİN ---
K = 'AIzaSyDD_eoF59ajl9pHuik-bxxQSdw8V-zPnEs' 
T = '8665581548:AAGnU06mVY6BK0TVXWPbszsgnmNqyywkBc' 
U = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={K}"

app = Flask('')
@app.route('/')
def home(): return "Zynx Bot Online"

async def handle(update, context):
    q = ' '.join(context.args)
    if not q: 
        await update.message.reply_text("Bir şeyler yaz knk. Örnek: /sor selam")
        return
    try:
        r = requests.post(U, json={"contents": [{"parts": [{"text": q}]}]})
        data = r.json()
        if "candidates" in data:
            cevap = data["candidates"][0]["content"]["parts"][0]["text"]
            await update.message.reply_text(cevap)
        else:
            hata = data.get("error", {}).get("message", "Google henüz anahtarı onaylamadı.")
            await update.message.reply_text(f"Sistem: {hata}")
    except Exception as e:
        await update.message.reply_text(f"Hata: {str(e)}")

def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

app_tg = ApplicationBuilder().token(T).build()
app_tg.add_handler(CommandHandler("sor", handle))
app_tg.run_polling()
