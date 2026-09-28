import os
import requests
import telebot

# Konfiguratsiya o'zgaruvchilari
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8930078083:AAGSrwdiMeXOgPNi5B_DGHwkc66UOYY6yD0')
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://modulx.onrender.com/api/')

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **ModulX ERP Botiga xush kelibsiz!**\n\n"
        "Ushbu bot ombor va ishlab chiqarish jarayonlarini tezkor boshqarish uchun mo'ljallangan.\n\n"
        "Mavjud buyruqlar:\n"
        "/yarns — Ip ombori qoldiqlari\n"
        "/fabrics — Mato/Gazlama ombori qoldiqlari\n"
        "/orders — Ishlab chiqarish buyurtmalari\n"
        "/status — API bilan aloqani tekshirish"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')


@bot.message_handler(commands=['status'])
def check_status(message):
    try:
        response = requests.get(API_BASE_URL.replace('/api/', '/'), timeout=5)
        if response.status_code == 200:
            bot.reply_to(message, "🟢 **ModulX API tizimi barqaror ishlamoqda!**", parse_mode='Markdown')
        else:
            bot.reply_to(message, f"⚠️ API javob statusi: {response.status_code}")
    except Exception as e:
        bot.reply_to(message, f"🔴 API ga ulanishda xatolik: {e}")


@bot.message_handler(commands=['yarns'])
def get_yarns(message):
    try:
        response = requests.get(f"{API_BASE_URL}yarns/", timeout=5)
        if response.status_code == 200:
            yarns = response.json()
            if not yarns:
                bot.reply_to(message, "📦 Ip ombori hozircha bo'sh.")
                return

            text = "🧶 **Ip omboridagi qoldiqlar:**\n\n"
            for item in yarns:
                # Modeldagi maydon nomlariga mos ravishda chiqaramiz
                name = item.get('name') or item.get('title') or item.get('yarn_type') or 'Nomsiz ip'
                qty = item.get('quantity') or item.get('amount') or 0
                text += f"• **{name}**: {qty} kg\n"

            bot.reply_to(message, text, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ Ip ombori ma'lumotlarini olib bo'lmadi.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ulanishda xatolik: {e}")


@bot.message_handler(commands=['fabrics'])
def get_fabrics(message):
    try:
        response = requests.get(f"{API_BASE_URL}fabrics/", timeout=5)
        if response.status_code == 200:
            fabrics = response.json()
            if not fabrics:
                bot.reply_to(message, "📦 Mato ombori hozircha bo'sh.")
                return

            text = "🏭 **Tayyor mato/gazlama qoldiqlari:**\n\n"
            for item in fabrics:
                name = item.get('name') or item.get('title') or item.get('fabric_type') or 'Nomsiz mato'
                qty = item.get('quantity') or item.get('amount') or 0
                text += f"• **{name}**: {qty} kg/rulon\n"

            bot.reply_to(message, text, parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ Mato ombori ma'lumotlarini olib bo'lmadi.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Ulanishda xatolik: {e}")


if __name__ == '__main__':
    print("ModulX Telegram boti ishga tushdi...")
    bot.infinity_polling()