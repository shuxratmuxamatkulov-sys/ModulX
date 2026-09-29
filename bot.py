import os
import requests
import telebot
from telebot import types

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8930078083:AAGSrwdiMeXOgPNi5B_DGHwkc66UOYY6yD0')
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://modulx.onrender.com/api/')

# Render.com cold-start (60 sekund)
REQUEST_TIMEOUT = 60

bot = telebot.TeleBot(BOT_TOKEN)

# Vaqtinchalik ma'lumotlarni saqlash (user_id -> data)
user_data = {}


def get_main_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    # 1. YUQORI QISM - BARCHA HARAKATLAR (AMALLAR)
    btn_add_order = types.InlineKeyboardButton("➕ Yangi buyurtma", callback_data="add_order")
    btn_add_yarn = types.InlineKeyboardButton("📥 Ip kirim qilish", callback_data="add_yarn")
    btn_issue_yarn = types.InlineKeyboardButton("📤 Sexga ip chiqim", callback_data="issue_yarn")
    btn_add_fabric = types.InlineKeyboardButton("📥 Sexdan mato kirim", callback_data="add_fabric")
    btn_issue_fabric = types.InlineKeyboardButton("🚚 Mijozga mato chiqim", callback_data="issue_fabric")

    # 2. PASTKI QISM - OMBOR VA HISOBOTLAR
    btn_yarns = types.InlineKeyboardButton("🧶 Ip ombori", callback_data="get_yarns")
    btn_fabrics = types.InlineKeyboardButton("🏭 Mato ombori", callback_data="get_fabrics")
    btn_orders = types.InlineKeyboardButton("📋 Buyurtmalar", callback_data="get_orders")
    btn_report = types.InlineKeyboardButton("📊 Kunlik hisobot", callback_data="get_report")
    btn_status = types.InlineKeyboardButton("🟢 API Status", callback_data="get_status")

    keyboard.add(btn_add_order)
    keyboard.add(btn_add_yarn, btn_issue_yarn)
    keyboard.add(btn_add_fabric, btn_issue_fabric)
    keyboard.add(btn_yarns, btn_fabrics)
    keyboard.add(btn_orders, btn_report)
    keyboard.add(btn_status)
    return keyboard


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 **ModulX ERP - To'quv Korxonasi Boshqaruv Boti**\n\n"
        "Barcha ishlab chiqarish va ombor operatsiyalarini quyidagi menyu orqali boshqarishingiz mumkin:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_keyboard(), parse_mode='Markdown')


# --- INLINE TUGMALAR ISHLOVCHISI ---
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    chat_id = call.message.chat.id

    if call.data == "get_yarns":
        fetch_yarns(call.message)
    elif call.data == "get_fabrics":
        fetch_fabrics(call.message)
    elif call.data == "get_orders":
        fetch_orders(call.message)
    elif call.data == "get_report":
        fetch_daily_report(call.message)
    elif call.data == "get_status":
        check_api_status(call.message)

    elif call.data == "add_order":
        msg = bot.send_message(chat_id, "📋 **Buyurtmachi (mijoz) nomini kiriting:**\n\n*(Masalan: 'XAN TEXTILE' MCHJ)*")
        bot.register_next_step_handler(msg, process_order_client)

    elif call.data == "add_yarn":
        msg = bot.send_message(chat_id, "👤 **Ip kimning nomi/buyurtmasi uchun keldi? (Mijoz nomi):**")
        bot.register_next_step_handler(msg, process_yarn_owner)

    elif call.data == "issue_yarn":
        msg = bot.send_message(chat_id, "🏭 **To'quv sexiga berilayotgan ip nomini kiriting:**\n*(Masalan: 30/1 KCD)*")
        bot.register_next_step_handler(msg, process_issue_yarn_name)

    elif call.data == "add_fabric":
        msg = bot.send_message(chat_id, "🏭 **To'quv sexidan tushgan mato nomini kiriting:**\n*(Masalan: Suprem 180g)*")
        bot.register_next_step_handler(msg, process_fabric_name)

    elif call.data == "issue_fabric":
        msg = bot.send_message(chat_id, "🚚 **Mijozga topshiriladigan mato nomini kiriting:**")
        bot.register_next_step_handler(msg, process_issue_fabric_name)


# ==========================================
# 1. BUYURTMA YARATISH (ORDER)
# ==========================================
def process_order_client(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'client': message.text.strip()}
    msg = bot.send_message(chat_id, "🏭 **Buyurtma qaysi mato uchun? Mato nomini kiriting:**")
    bot.register_next_step_handler(msg, process_order_fabric)


def process_order_fabric(message):
    chat_id = message.chat.id
    user_data[chat_id]['fabric'] = message.text.strip()
    msg = bot.send_message(chat_id, f"⚖️ **'{user_data[chat_id]['client']}'** uchun rejadagi miqdorni kiriting (kg):")
    bot.register_next_step_handler(msg, process_order_quantity)


def process_order_quantity(message):
    chat_id = message.chat.id
    try:
        quantity = float(message.text.replace(',', '.').strip())
        client_name = user_data[chat_id]['client']
        fabric_name = user_data[chat_id]['fabric']

        bot.send_message(chat_id, "⏳ Serverga ulanmoqda, iltimos kuting...")

        # Backend talabiga ko'ra 'fabric' maydoni string yoki mos formatda yuboriladi
        payload = {
            'client_name': client_name,
            'fabric': fabric_name,
            'target_kg': quantity,
            'status': 'pending'
        }

        response = requests.post(f"{API_BASE_URL}orders/", json=payload, timeout=REQUEST_TIMEOUT)
        if response.status_code in [200, 201]:
            bot.send_message(
                chat_id,
                f"✅ **Buyurtma muvaffaqiyatli saqlandi!**\n\n📋 Mijoz: **{client_name}**\n🏭 Mato: **{fabric_name}**\n⚖️ Reja: **{quantity} kg**",
                reply_markup=get_main_keyboard(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id, f"❌ Saqlashda xatolik: {response.text}", reply_markup=get_main_keyboard())
    except ValueError:
        bot.send_message(chat_id, "⚠️ Iltimos, miqdorni faqat raqamlarda kiriting!", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Xatolik: {e}", reply_markup=get_main_keyboard())


# ==========================================
# 2. IP KIRIM VA CHIQIM (YARN MOVEMENT)
# ==========================================
def process_yarn_owner(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'owner': message.text.strip()}
    msg = bot.send_message(chat_id, "🧶 **Kelgan ipning markasi/nomini kiriting:**\n*(Masalan: 30/1 KCD)*")
    bot.register_next_step_handler(msg, process_yarn_name)


def process_yarn_name(message):
    chat_id = message.chat.id
    user_data[chat_id]['title'] = message.text.strip()
    msg = bot.send_message(chat_id, f"⚖️ **{user_data[chat_id]['owner']}** uchun kelgan **'{message.text}'** ipi miqdorini kiriting (kg):")
    bot.register_next_step_handler(msg, process_yarn_quantity)


def process_yarn_quantity(message):
    chat_id = message.chat.id
    try:
        quantity = float(message.text.replace(',', '.').strip())
        owner = user_data[chat_id]['owner']
        yarn_title = user_data[chat_id]['title']

        bot.send_message(chat_id, "⏳ Serverga yozilmoqda...")

        # 1. Ombor umumiy balansini yangilash
        payload_yarn = {'name': f"{yarn_title} ({owner})", 'quantity': quantity}
        requests.post(f"{API_BASE_URL}yarns/", json=payload_yarn, timeout=REQUEST_TIMEOUT)

        # 2. Ip Kirim jurnaliga yozish
        payload_income = {
            'client_name': owner,
            'yarn_name': yarn_title,
            'quantity_kg': quantity
        }
        response = requests.post(f"{API_BASE_URL}yarn-incomes/", json=payload_income, timeout=REQUEST_TIMEOUT)

        if response.status_code in [200, 201]:
            bot.send_message(
                chat_id,
                f"✅ **Ip omboriga kirim qilindi!**\n\n👤 Mijoz: **{owner}**\n🧶 Ip: **{yarn_title}**\n⚖️ Miqdor: **{quantity} kg**",
                reply_markup=get_main_keyboard(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id, f"❌ Xatolik: {response.text}", reply_markup=get_main_keyboard())
    except ValueError:
        bot.send_message(chat_id, "⚠️ Iltimos, miqdorni raqamlarda kiriting!", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Xatolik: {e}", reply_markup=get_main_keyboard())


def process_issue_yarn_name(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'yarn_issue_name': message.text.strip()}
    msg = bot.send_message(chat_id, f"⚖️ **'{message.text}'** ipidan to'quv sexiga qancha berilmoqda (kg)?")
    bot.register_next_step_handler(msg, process_issue_yarn_qty)


def process_issue_yarn_qty(message):
    chat_id = message.chat.id
    try:
        quantity = float(message.text.replace(',', '.').strip())
        yarn_name = user_data[chat_id]['yarn_issue_name']

        bot.send_message(chat_id, "⏳ Chiqim rasmiylashtirilmoqda...")

        payload = {
            'yarn_name': yarn_name,
            'quantity_kg': quantity
        }
        response = requests.post(f"{API_BASE_URL}yarn-issues/", json=payload, timeout=REQUEST_TIMEOUT)

        if response.status_code in [200, 201]:
            bot.send_message(
                chat_id,
                f"📤 **To'quv sexiga ip chiqim qilindi!**\n\n🧶 Ip: **{yarn_name}**\n⚖️ Chiqim: **{quantity} kg**",
                reply_markup=get_main_keyboard(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id, f"❌ Xatolik: {response.text}", reply_markup=get_main_keyboard())
    except ValueError:
        bot.send_message(chat_id, "⚠️ Iltimos, miqdorni raqamlarda kiriting!", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Xatolik: {e}", reply_markup=get_main_keyboard())


# ==========================================
# 3. MATO KIRIM VA CHIQIM (FABRIC MOVEMENT)
# ==========================================
def process_fabric_name(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'title': message.text.strip()}
    msg = bot.send_message(chat_id, f"⚖️ To'quv sexida to'qilgan **'{message.text}'** matosi miqdorini kiriting (kg):")
    bot.register_next_step_handler(msg, process_fabric_quantity)


def process_fabric_quantity(message):
    chat_id = message.chat.id
    try:
        quantity = float(message.text.replace(',', '.').strip())
        fabric_title = user_data[chat_id]['title']

        bot.send_message(chat_id, "⏳ Omborga mato kirim qilinmoqda...")

        # 1. Ombor balansini yangilash
        payload_fabric = {'name': fabric_title, 'quantity': quantity}
        requests.post(f"{API_BASE_URL}fabrics/", json=payload_fabric, timeout=REQUEST_TIMEOUT)

        # 2. Mato Kirim jurnaliga yozish
        payload_income = {
            'fabric_name': fabric_title,
            'quantity_kg': quantity
        }
        response = requests.post(f"{API_BASE_URL}fabric-incomes/", json=payload_income, timeout=REQUEST_TIMEOUT)

        if response.status_code in [200, 201]:
            bot.send_message(
                chat_id,
                f"✅ **Mato omboriga tushdi!**\n\n🏭 Mato: **{fabric_title}**\n⚖️ Miqdor: **{quantity} kg**",
                reply_markup=get_main_keyboard(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id, f"❌ Xatolik: {response.text}", reply_markup=get_main_keyboard())
    except ValueError:
        bot.send_message(chat_id, "⚠️ Iltimos, miqdorni raqamlarda kiriting!", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Xatolik: {e}", reply_markup=get_main_keyboard())


def process_issue_fabric_name(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'fabric_issue_name': message.text.strip()}
    msg = bot.send_message(chat_id, f"⚖️ **'{message.text}'** matosidan mijozga qancha topshirilmoqda (kg)?")
    bot.register_next_step_handler(msg, process_issue_fabric_qty)


def process_issue_fabric_qty(message):
    chat_id = message.chat.id
    try:
        quantity = float(message.text.replace(',', '.').strip())
        fabric_name = user_data[chat_id]['fabric_issue_name']

        bot.send_message(chat_id, "⏳ Mijozga mato topshirilmoqda...")

        payload = {
            'fabric_name': fabric_name,
            'quantity_kg': quantity
        }
        response = requests.post(f"{API_BASE_URL}fabric-dispatches/", json=payload, timeout=REQUEST_TIMEOUT)

        if response.status_code in [200, 201]:
            bot.send_message(
                chat_id,
                f"🚚 **Mijozga mato topshirildi (Chiqim)!**\n\n🏭 Mato: **{fabric_name}**\n⚖️ Chiqim: **{quantity} kg**",
                reply_markup=get_main_keyboard(),
                parse_mode='Markdown'
            )
        else:
            bot.send_message(chat_id, f"❌ Xatolik: {response.text}", reply_markup=get_main_keyboard())
    except ValueError:
        bot.send_message(chat_id, "⚠️ Iltimos, miqdorni raqamlarda kiriting!", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(chat_id, f"⚠️ Xatolik: {e}", reply_markup=get_main_keyboard())


# ==========================================
# 4. OMBOR VA HISOBOTLARNI KO'RISH
# ==========================================
def fetch_yarns(message):
    try:
        response = requests.get(f"{API_BASE_URL}yarns/", timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            yarns = response.json()
            if not yarns:
                bot.send_message(message.chat.id, "📦 Ip omborida hozircha qoldiq yo'q.", reply_markup=get_main_keyboard())
                return
            text = "🧶 **Ip omboridagi qoldiqlar:**\n\n"
            for item in yarns:
                name = item.get('name') or item.get('title') or 'Ip'
                qty = item.get('quantity') or item.get('quantity_kg') or 0
                text += f"• **{name}**: {qty} kg\n"
            bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "❌ API xatosi", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


def fetch_fabrics(message):
    try:
        response = requests.get(f"{API_BASE_URL}fabrics/", timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            fabrics = response.json()
            if not fabrics:
                bot.send_message(message.chat.id, "📦 Mato omborida hozircha qoldiq yo'q.", reply_markup=get_main_keyboard())
                return
            text = "🏭 **Mato omboridagi tayyor qoldiqlar:**\n\n"
            for item in fabrics:
                name = item.get('name') or item.get('title') or 'Mato'
                qty = item.get('quantity') or item.get('quantity_kg') or 0
                text += f"• **{name}**: {qty} kg\n"
            bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "❌ API xatosi", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


def fetch_orders(message):
    try:
        response = requests.get(f"{API_BASE_URL}orders/", timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            orders = response.json()
            if not orders:
                bot.send_message(message.chat.id, "📋 Buyurtmalar mavjud emas.", reply_markup=get_main_keyboard())
                return
            text = "📋 **Aktiv buyurtmalar ro'yxati:**\n\n"
            for item in orders:
                client = item.get('client_name') or "Mijoz"
                fabric = item.get('fabric_name') or item.get('fabric') or "Mato"
                status = item.get('status', 'pending')
                qty = item.get('target_kg') or item.get('quantity') or 0
                text += f"• **{client}** ({fabric}): {qty} kg | Status: `{status}`\n"
            bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "❌ API xatosi", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Ulanishda xatolik: {e}", reply_markup=get_main_keyboard())


def fetch_daily_report(message):
    try:
        y_res = requests.get(f"{API_BASE_URL}yarns/", timeout=REQUEST_TIMEOUT)
        f_res = requests.get(f"{API_BASE_URL}fabrics/", timeout=REQUEST_TIMEOUT)
        o_res = requests.get(f"{API_BASE_URL}orders/", timeout=REQUEST_TIMEOUT)

        total_yarn = sum([float(i.get('quantity') or i.get('quantity_kg') or 0) for i in y_res.json()]) if y_res.status_code == 200 else 0
        total_fabric = sum([float(i.get('quantity') or i.get('quantity_kg') or 0) for i in f_res.json()]) if f_res.status_code == 200 else 0
        total_orders = len(o_res.json()) if o_res.status_code == 200 else 0

        text = (
            "📊 **KORXONA KUNLIK UMUMIY HISOBOTI**\n\n"
            f"🧶 **Umumiy Ip qoldig'i:** {total_yarn} kg\n"
            f"🏭 **Umumiy Mato qoldig'i:** {total_fabric} kg\n"
            f"📋 **Aktiv Buyurtmalar soni:** {total_orders} ta\n"
        )
        bot.send_message(message.chat.id, text, reply_markup=get_main_keyboard(), parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Hisobot tayyorlashda xatolik: {e}", reply_markup=get_main_keyboard())


def check_api_status(message):
    try:
        response = requests.get(API_BASE_URL.replace('/api/', '/'), timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            bot.send_message(message.chat.id, "🟢 **ModulX API tizimi barqaror ishlamoqda!**", reply_markup=get_main_keyboard(), parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, f"⚠️ API status: {response.status_code}", reply_markup=get_main_keyboard())
    except Exception as e:
        bot.send_message(message.chat.id, f"🔴 API xatosi: {e}", reply_markup=get_main_keyboard())


if __name__ == '__main__':
    print("ModulX Yangilangan Telegram Boti ishga tushdi...")
    bot.infinity_polling()