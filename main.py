import os, requests
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler

# --- BİLGİLERİN ---
K = 'AIzaSyDD_eoF59ajl9pHuik-bxxQSdw8V-zPnEs'
T = '8665581548:AAGnU06mVY6BK0TVXWPwbszsgnhNqyywkBc'
U = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={K}"

app = Flask('')
@app.route('/')
def home(): return "Zynx Bot Online"

async def handle(update, context):
    q = ' '.join(context.args)
    if not q: return
    try:
        # Doğrudan istek gönderiyoruz, kütüphane kalabalığı yok
        r = requests.post(U, json={"contents": [{"parts": [{"text": q}]}]}).json()
        ans = r['candidates'][0]['content']['parts'][0]['text']
        await update.message.reply_text(ans)
    except:
        await update.message.reply_text("...")

if __name__ == '__main__':
    Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    bot = ApplicationBuilder().token(T).build()
    bot.add_handler(CommandHandler('sor', handle))
    bot.run_polling()
