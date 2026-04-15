import os, requests
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

# --- BİLGİLER ---
K = 'AIzaSyDD_eoF59ajl9pHuik-bxxQSdw8V-zPnEs' 
T = '8665581548:AAGnU06mVY6BK0TVXWPbszsgnmNqyywkBc' 

app = Flask('')
@app.route('/')
def home(): return "Zynx Bot Aktif"

async def handle(update, context):
    q = ' '.join(context.args)
    if not q: return
    
    # En stabil Google linki
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={K}"
    
    try:
        r = requests.post(url, json={"contents": [{"parts": [{"text": q}]}]})
        data = r.json()
        
        if "candidates" in data:
            cevap = data["candidates"][0]["content"]["parts"][0]["text"]
            await update.message.reply_text(cevap)
        else:
            await update.message.reply_text("Google anahtarı henüz tam aktif değil, biraz bekle knk.")
    except Exception as e:
        await update.message.reply_text("Bir hata oluştu, tekrar dene.")

def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

app_tg = ApplicationBuilder().token(T).build()
app_tg.add_handler(CommandHandler("sor", handle))
app_tg.run_polling()
