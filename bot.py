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
    btn_add_order = types.InlineKeyboardButton("➕ Yangi buyurtma", callback_data="add_order")
    btn_status = types.InlineKeyboardButton("🟢 API Status", callback_data="get_status")

    keyboard.add(btn_yarns, btn_fabrics)
    keyboard.add(btn_add_yarn, btn_add_fabric)
    keyboard.add(btn_orders, btn_add_order)
    keyboard.add(btn_status)
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
    elif call.data == "add_order":
        msg = bot.send_message(call.message.chat.id,
                               "📋 **Buyurtmachi (mijoz) nomini kiriting:**\n\n*(Masalan: 'FEN TEXTILE' MCHJ)*")
        bot.register_next_step_handler(msg, process_order_client)


# --- IP OMBORI KO'RISH VA KIRIM QILISH ---
def fetch_yarns(message):
    try:
        response = requests.get(f"{API_BASE_URL}yarns/", timeout=15)
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
    except requests.exceptions.Timeout:
        bot.send_message(message.chat.id, "⏳ Server javob berishda kechikmoqda, iltimos qaytadan urinib ko'ring.", reply_markup=get_main_keyboard())
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

        payload = {
            'name': yarn_title,
            'title': yarn_title,
            'quantity': quantity,
            'quantity_kg': quantity,
            'amount': quantity,
            'amount_kg': quantity
        }

        response = requests.post(f"{API_BASE_URL}yarns/", json=payload, timeout=15)
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
    except requests.exceptions.Timeout:
        bot.send_message(chat_id, "⏳ Server javob berishda kechikmoqda. Iltimos qaytadan urinib ko'ring.", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Server bilan ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


# --- MATO OMBORI KO'RISH VA KIRIM QILISH ---
def fetch_fabrics(message):
    try:
        response = requests.get(f"{API_BASE_URL}fabrics/", timeout=15)
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
    except requests.exceptions.Timeout:
        bot.send_message(message.chat.id, "⏳ Server javob berishda kechikmoqda, iltimos qaytadan urinib ko'ring.", reply_markup=get_main_keyboard())
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
            'name': fabric_title,
            'title': fabric_title,
            'quantity': quantity,
            'quantity_kg': quantity,
            'amount': quantity,
            'amount_kg': quantity
        }

        response = requests.post(f"{API_BASE_URL}fabrics/", json=payload, timeout=15)
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
    except requests.exceptions.Timeout:
        bot.send_message(chat_id, "⏳ Server javob berishda kechikmoqda. Iltimos qaytadan urinib ko'ring.", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Server bilan ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


# --- BUYURTMALAR KO'RISH VA QO'SHISH ---
def fetch_orders(message):
    try:
        response = requests.get(f"{API_BASE_URL}orders/", timeout=15)
        if response.status_code == 200:
            orders = response.json()
            if not orders:
                bot.send_message(message.chat.id, "📋 Ishlab chiqarish buyurtmalari hozircha yo'q.",
                                 reply_markup=get_main_keyboard())
                return

            text = "📋 **Ishlab chiqarish buyurtmalari:**\n\n"
            for item in orders:
                order_id = item.get('id', '')
                title = item.get('title') or item.get('name') or item.get('client_name') or f"Buyurtma #{order_id}"
                status = item.get('status', 'Noma\'lum')
                quantity = item.get('target_kg') or item.get('quantity') or item.get('amount') or 0
                text += f"• **{title}**: {quantity} kg | Status: {status}\n"

            bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"❌ API xatosi (Status code: {response.status_code})",
                             reply_markup=get_main_keyboard())
    except requests.exceptions.Timeout:
        bot.send_message(message.chat.id, "⏳ Server javob berishda kechikmoqda, iltimos qaytadan urinib ko'ring.", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


def process_order_client(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'client': message.text}
    msg = bot.send_message(chat_id, "🏭 **Buyurtma qaysi mato uchun? Mato nomini kiriting:**\n\n*(Masalan: Suprem 100% Xlopok)*")
    bot.register_next_step_handler(msg, process_order_fabric)


def process_order_fabric(message):
    chat_id = message.chat.id
    user_data[chat_id]['fabric'] = message.text
    msg = bot.send_message(chat_id, f"⚖️ **'{user_data[chat_id]['client']}'** uchun rejadagi miqdorni kiriting (kg):")
    bot.register_next_step_handler(msg, process_order_quantity)


def process_order_quantity(message):
    chat_id = message.chat.id
    try:
        quantity = float(message.text.replace(',', '.'))
        client_name = user_data[chat_id]['client']
        fabric_name = user_data[chat_id]['fabric']

        # 1. Matolar ro'yxatidan nomiga mos mato ID sini izlash
        fabric_id = None
        fab_res = requests.get(f"{API_BASE_URL}fabrics/", timeout=15)
        if fab_res.status_code == 200:
            fabrics = fab_res.json()
            for f in fabrics:
                f_title = f.get('title') or f.get('name') or ''
                if f_title.lower().strip() == fabric_name.lower().strip():
                    fabric_id = f.get('id')
                    break

        # 2. Agar mato bazada hali bo'lmasa, uni avval yangi mato sifatida yaratamiz
        if not fabric_id:
            create_fab = requests.post(
                f"{API_BASE_URL}fabrics/",
                json={'title': fabric_name, 'name': fabric_name, 'quantity': 0},
                timeout=15
            )
            if create_fab.status_code in [200, 201]:
                fabric_id = create_fab.json().get('id')

        # 3. Buyurtma payload'ini tayyorlash
        payload = {
            'client_name': client_name,
            'client': client_name,
            'title': f"{client_name} - {fabric_name}",
            'fabric_name': fabric_name,
            'target_kg': quantity,
            'quantity': quantity,
            'quantity_kg': quantity,
            'status': 'pending'
        }

        # Django ForeignKey kutilayotgan ID ni yuboramiz
        if fabric_id:
            payload['fabric'] = fabric_id

        response = requests.post(f"{API_BASE_URL}orders/", json=payload, timeout=15)
        if response.status_code in [200, 201]:
            bot.send_message(
                chat_id,
                f"✅ **Buyurtma muvaffaqiyatli saqlandi!**\n\n📋 Mijoz: **{client_name}**\n🏭 Mato: **{fabric_name}**\n⚖️ Reja: **{quantity} kg**",
                reply_markup=get_main_keyboard(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(
                chat_id,
                f"❌ Saqlashda xatolik yuz berdi (API status: {response.status_code}):\n{response.text}",
                reply_markup=get_main_keyboard()
            )
    except ValueError:
        msg = bot.send_message(chat_id, "⚠️ Iltimos, miqdorni faqat sonlarda kiriting (Masalan: 5000):")
        bot.register_next_step_handler(msg, process_order_quantity)
    except requests.exceptions.Timeout:
        bot.send_message(
            chat_id,
            "⏳ Server javob berishda kechikmoqda, qaytadan urinib ko'ring.",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Server bilan ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


# --- QO'SHIMCHA FUNKSIYALAR ---
def check_api_status(message):
    try:
        response = requests.get(API_BASE_URL.replace('/api/', '/'), timeout=15)
        if response.status_code == 200:
            bot.send_message(message.chat.id, "🟢 **ModulX API tizimi barqaror ishlamoqda!**",
                             reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"⚠️ API javob statusi: {response.status_code}",
                             reply_markup=get_main_keyboard())
    except requests.exceptions.Timeout:
        bot.send_message(message.chat.id, "⏳ API ulanish taym-auti (server uyquda bo'lishi mumkin).", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"🔴 API ga ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


if __name__ == '__main__':
    print("ModulX Telegram boti ishga tushdi...")
    bot.infinity_polling()