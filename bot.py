import asyncio
import requests
from datetime import datetime, timedelta

TOKEN = "8671377519:AAHRU5jHYCcPJUdIG4QbfyVC7lSzBRi4uiI"
CHAT_ID = "-1004451794051"

# Hafıza
mac_bitis_zamani = None
# Analizi de içeren güncel ve detaylı kupon metni
aktif_kupon = (
    "🏀 **GÜNCEL BASKETBOL KUPONU**\n\n"
    "🆚 **Cyber Ukrayna vs Gürcistan**\n"
    "📊 **Tahmin:** 164 ALT\n"
    "💰 **Oran:** 1.70\n\n"
    "💡 **Analiz:** İade avantajlı, sert savunma bekliyoruz. "
    "Maç başladı, herkese bol şans!"
)

def mesaj_gonder_menu(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "reply_markup": {
            "inline_keyboard": [
                [{"text": "🏀 Basketbol Kuponu", "callback_data": "basket"}],
                [{"text": "⚽ Futbol Tahmini", "callback_data": "futbol"}]
            ]
        }
    }
    requests.post(url, json=payload)

def mesaj_gonder_duz(text):
    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                  data={"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"})

async def main():
    global mac_bitis_zamani
    print("Bot hazır, tam analizli sistem aktif...")
    son_update_id = 0
    
    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={son_update_id + 1}"
        try:
            cevap = requests.get(url).json()
            if cevap["result"]:
                for update in cevap["result"]:
                    son_update_id = update["update_id"]
                    
                    if "message" in update and "/start" in update["message"].get("text", ""):
                        mesaj_gonder_menu("🤖 **Premium Kupon Botu Aktif!**\nLütfen bir branş seçin:")
                    
                    elif "callback_query" in update:
                        data = update["callback_query"]["data"]
                        
                        if data == "basket":
                            if mac_bitis_zamani and datetime.now() > mac_bitis_zamani:
                                mesaj_gonder_duz("ℹ️ Şu an aktif bir maç kuponu bulunmamaktadır. Yeni analizler için takipte kal!")
                            else:
                                if not mac_bitis_zamani:
                                    sure = 60 if "Cyber" in aktif_kupon else 80
                                    mac_bitis_zamani = datetime.now() + timedelta(minutes=sure)
                                mesaj_gonder_duz(aktif_kupon)
                        
                        elif data == "futbol":
                            mesaj_gonder_duz("⚽ Şu an aktif bir futbol tahmini bulunmamaktadır.")
        except: pass
        await asyncio.sleep(2)

if __name__ == '__main__':
    asyncio.run(main())
