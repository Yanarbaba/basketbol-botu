import telebot
from flask import Flask
from threading import Thread
from telebot import types

# Token ve Chat ID bilgilerin güncellendi
TOKEN = "8671377519:AAHRU5jHYCcPJUdiG4Qbf"
CHAT_ID = "-1004451794051"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Render'ın uyutmaması için web rotası
@app.route('/')
def home():
    return "Bot aktif ve çalışıyor!"

def run_web():
    app.run(host='0.0.0.0', port=10000)

# Butonlu menü yapısı
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('🏀 Basketbol Kuponu', '⚽ Futbol Tahmini')
    bot.send_message(message.chat.id, "🤖 **Premium Kupon Botu Aktif!**\nLütfen bir branş seçin:", parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == '🏀 Basketbol Kuponu':
        bot.reply_to(message, "🏀 GÜNCEL BASKETBOL KUPONU\n\nVS Cyber Ukrayna vs Gürcistan\n📊 Tahmin: 164 ALT\n💰 Oran: 1.70\n\n💡 Analiz: İade avantajlı, sert savunma bekliyoruz. Maç başladı, herkese bol şans!")
    elif message.text == '⚽ Futbol Tahmini':
        bot.reply_to(message, "⚽ Henüz aktif futbol tahmini bulunmuyor.")

# Flask web sunucusunu ayarla
app = Flask('')

@app.route('/')
def home():
    return "Bot aktif!"

def run():
    app.run(host='0.0.0.0', port=10000)

# Web sunucusunu arka planda çalıştır
t = Thread(target=run)
t.start()

# Botu çalıştır
bot.infinity_polling()
