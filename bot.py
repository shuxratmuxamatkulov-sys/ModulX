import os
import requests
import telebot
from telebot import types

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8930078083:AAGSrwdiMeXOgPNi5B_DGHwkc66UOYY6yD0')
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://modulx.onrender.com/api/')

bot = telebot.TeleBot(BOT_TOKEN)

# Ma'lumotlarni vaqtincha saqlash uchun lug'at (user_id -> data)
user_data = {}


def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    btn_yarns = types.InlineKeyboardButton("🧶 Ip ombori", callback_data="get_yarns")
    btn_fabrics = types.InlineKeyboardButton("🏭 Mato ombori", callback_data="get_fabrics")
    btn_add_yarn = types.InlineKeyboardButton("➕ Yangi ip kirim qilish", callback_data="add_yarn")
    btn_add_fabric = types.InlineKeyboardButton("➕ Yangi mato kirim qilish", callback_data="add_fabric")
    btn_orders = types.InlineKeyboardButton("📋 Buyurtmalar", callback_data="get_orders")
    btn_status = types.InlineKeyboardButton("🟢 API Status", callback_data="get_status")

    keyboard.add(btn_yarns, btn_fabrics)
    keyboard.add(btn_add_yarn, btn_add_fabric)
    keyboard.add(btn_orders, btn_status)
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **ModulX ERP Boshqaruv Botiga xush kelibsiz!**\n\n"
        "Quyidagi menyu orqali ombor qoldiqlarini ko'rishingiz yoki yangi kirim qilishingiz mumkin:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(), parse_mode='Markdown')


# --- INLINE TUGMALAR ISHLOVCHISI ---
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    if call.data == "get_yarns":
        fetch_yarns(call.message)
    elif call.data == "get_fabrics":
        fetch_fabrics(call.message)
    elif call.data == "get_orders":
        fetch_orders(call.message)
    elif call.data == "get_status":
        check_api_status(call.message)
    elif call.data == "add_yarn":
        msg = bot.send_message(call.message.chat.id, "🧶 **Yangi ip nomini kiriting:**\n\n*(Masalan: 30/1 KCD)*")
        bot.register_next_step_handler(msg, process_yarn_name)
    elif call.data == "add_fabric":
        msg = bot.send_message(call.message.chat.id,
                               "🏭 **Yangi mato nomini kiriting:**\n\n*(Masalan: Suprem 100% Xlopok)*")
        bot.register_next_step_handler(msg, process_fabric_name)


# --- IP OMBORI KO'RISH VA KIRIM QILISH ---
def fetch_yarns(message):
    try:
        response = requests.get(f"{API_BASE_URL}yarns/", timeout=5)
        if response.status_code == 200:
            yarns = response.json()
            if not yarns:
                bot.send_message(message.chat.id, "📦 Ip omborida hozircha hech narsa yo'q.",
                                 reply_markup=get_main_keyboard())
                return

            text = "🧶 **Ip omboridagi qoldiqlar:**\n\n"
            for item in yarns:
                name = item.get('title') or item.get('name') or item.get('yarn_type') or item.get('code') or 'Ip'
                qty = (
                        item.get('quantity_kg') or
                        item.get('amount_kg') or
                        item.get('quantity') or
                        item.get('amount') or
                        item.get('weight') or 0
                )
                text += f"• **{name}**: {qty} kg\n"

            bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"❌ API xatosi (Status code: {response.status_code})",
                             reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


def process_yarn_name(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'title': message.text}
    msg = bot.send_message(chat_id, f"⚖️ **'{message.text}'** uchun miqdorni kiriting (kg):")
    bot.register_next_step_handler(msg, process_yarn_quantity)


def process_yarn_quantity(message):
    chat_id = message.chat.id
    try:
        quantity = float(message.text.replace(',', '.'))
        yarn_title = user_data[chat_id]['title']

        # REST API ga POST so'rov yuboramiz
        payload = {
            'title': yarn_title,
            'quantity_kg': quantity
        }

        response = requests.post(f"{API_BASE_URL}yarns/", json=payload, timeout=5)
        if response.status_code in [200, 201]:
            bot.send_message(
                chat_id,
                f"✅ **Muvaffaqiyatli saqlandi!**\n\n🧶 Ip: **{yarn_title}**\n⚖️ Miqdor: **{quantity} kg**",
                reply_markup=get_main_keyboard(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id,
                             f"❌ Saqlashda xatolik yuz berdi (API status: {response.status_code}):\n{response.text}",
                             reply_markup=get_main_keyboard())
    except ValueError:
        msg = bot.send_message(chat_id, "⚠️ Iltimos, miqdorni faqat sonlarda kiriting (Masalan: 250.5):")
        bot.register_next_step_handler(msg, process_yarn_quantity)
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Server bilan ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


# --- MATO OMBORI KO'RISH VA KIRIM QILISH ---
def fetch_fabrics(message):
    try:
        response = requests.get(f"{API_BASE_URL}fabrics/", timeout=5)
        if response.status_code == 200:
            fabrics = response.json()
            if not fabrics:
                bot.send_message(message.chat.id, "📦 Mato omborida hozircha hech narsa yo'q.",
                                 reply_markup=get_main_keyboard())
                return

            text = "🏭 **Tayyor mato qoldiqlari:**\n\n"
            for item in fabrics:
                name = item.get('title') or item.get('name') or item.get('fabric_type') or item.get('code') or 'Mato'
                qty = (
                        item.get('quantity_kg') or
                        item.get('amount_kg') or
                        item.get('quantity') or
                        item.get('amount') or
                        item.get('weight') or 0
                )
                text += f"• **{name}**: {qty} kg/rulon\n"

            bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"❌ API xatosi (Status code: {response.status_code})",
                             reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


def process_fabric_name(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'title': message.text}
    msg = bot.send_message(chat_id, f"⚖️ **'{message.text}'** matosi uchun miqdorni kiriting (kg):")
    bot.register_next_step_handler(msg, process_fabric_quantity)


def process_fabric_quantity(message):
    chat_id = message.chat.id
    try:
        quantity = float(message.text.replace(',', '.'))
        fabric_title = user_data[chat_id]['title']

        payload = {
            'title': fabric_title,
            'quantity_kg': quantity
        }

        response = requests.post(f"{API_BASE_URL}fabrics/", json=payload, timeout=5)
        if response.status_code in [200, 201]:
            bot.send_message(
                chat_id,
                f"✅ **Muvaffaqiyatli saqlandi!**\n\n🏭 Mato: **{fabric_title}**\n⚖️ Miqdor: **{quantity} kg**",
                reply_markup=get_main_keyboard(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id,
                             f"❌ Saqlashda xatolik yuz berdi (API status: {response.status_code}):\n{response.text}",
                             reply_markup=get_main_keyboard())
    except ValueError:
        msg = bot.send_message(chat_id, "⚠️ Iltimos, miqdorni faqat sonlarda kiriting (Masalan: 120):")
        bot.register_next_step_handler(msg, process_fabric_quantity)
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Server bilan ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


# --- QO'SHIMCHA FUNKSIYALAR ---
def fetch_orders(message):
    try:
        response = requests.get(f"{API_BASE_URL}orders/", timeout=5)
        if response.status_code == 200:
            orders = response.json()
            if not orders:
                bot.send_message(message.chat.id, "📋 Ishlab chiqarish buyurtmalari hozircha yo'q.",
                                 reply_markup=get_main_keyboard())
                return

            text = "📋 **Ishlab chiqarish buyurtmalari:**\n\n"
            for item in orders:
                order_id = item.get('id', '')
                status = item.get('status', 'Noma\'lum')
                quantity = item.get('quantity') or item.get('amount') or 0
                text += f"• **Buyurtma #{order_id}**: {quantity} kg/rulon | Status: {status}\n"

            bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"❌ API xatosi (Status code: {response.status_code})",
                             reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


def check_api_status(message):
    try:
        response = requests.get(API_BASE_URL.replace('/api/', '/'), timeout=5)
        if response.status_code == 200:
            bot.send_message(message.chat.id, "🟢 **ModulX API tizimi barqaror ishlamoqda!**",
                             reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"⚠️ API javob statusi: {response.status_code}",
                             reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"🔴 API ga ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


if __name__ == '__main__':
    print("ModulX Telegram boti ishga tushdi...")
    bot.infinity_polling()