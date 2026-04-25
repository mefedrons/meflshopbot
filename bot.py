import telebot
from telebot import types
import sqlite3
import random
import time

TOKEN = "8763154419:AAFaaCS4i0hNXGwAOgGK82WVjmBFWRtaeAw"
ADMIN = "@MEFEDRONYT"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ---------------- БАЗА ----------------
db = sqlite3.connect("shop.db", check_same_thread=False)
sql = db.cursor()

sql.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
balance INTEGER DEFAULT 0
)
""")

sql.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
product TEXT,
brand TEXT,
delivery TEXT,
track TEXT,
date TEXT
)
""")
db.commit()

# ---------------- ТОВАРЫ ----------------
catalog = {
    "Stone Island": [
        ("Hoodie Black", 6990),
        ("Jacket Soft Shell", 12990),
        ("Cargo Pants", 8990)
    ],
    "CP Company": [
        ("Zip Hoodie", 7490),
        ("Shell Jacket", 11990)
    ],
    "D&G": [
        ("Tee Black", 5490),
        ("Sweatshirt", 8990)
    ],
    "Nike": [
        ("Tech Fleece", 7990),
        ("TN Plus", 9990)
    ]
}

temp_orders = {}

# ---------------- ВСПОМОГАТЕЛЬНОЕ ----------------
def reg_user(uid):
    sql.execute("INSERT OR IGNORE INTO users(user_id) VALUES(?)", (uid,))
    db.commit()

def main_menu():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("👤 Личный кабинет")
    kb.row("🛍 Каталог", "⭐ Отзывы")
    kb.row("📞 Контакты / FAQ")
    return kb

def track_gen():
    return "MFS" + str(random.randint(100000, 999999))

# ---------------- START ----------------
@bot.message_handler(commands=["start"])
def start(msg):
    reg_user(msg.from_user.id)

    bot.send_message(
        msg.chat.id,
        "🔥 <b>Приветствую в магазин одежды mefedron•shop.</b>\n\n"
        "Здесь можете выбрать и приобрести любую вещь из каталога разных брендов с автоматической оплатой.\n\n"
        "Если возникли вопросы:\n"
        f"{ADMIN}",
        reply_markup=main_menu()
    )

# ---------------- ЛК ----------------
@bot.message_handler(func=lambda m: m.text == "👤 Личный кабинет")
def cabinet(msg):
    reg_user(msg.from_user.id)

    sql.execute("SELECT balance FROM users WHERE user_id=?", (msg.from_user.id,))
    bal = sql.fetchone()[0]

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📜 История покупок", callback_data="history"))

    bot.send_message(
        msg.chat.id,
        f"👤 <b>Личный кабинет</b>\n\n"
        f"ID: <code>{msg.from_user.id}</code>\n"
        f"Баланс: <b>{bal}₽</b>",
        reply_markup=kb
    )

# ---------------- КАТАЛОГ ----------------
@bot.message_handler(func=lambda m: m.text == "🛍 Каталог")
def open_catalog(msg):
    kb = types.InlineKeyboardMarkup()

    for brand in catalog:
        kb.add(types.InlineKeyboardButton(brand, callback_data=f"brand_{brand}"))

    bot.send_message(msg.chat.id, "🛍 <b>Выбери желаемый товар:</b>", reply_markup=kb)

# ---------------- ОТЗЫВЫ ----------------
@bot.message_handler(func=lambda m: m.text == "⭐ Отзывы")
def reviews(msg):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Отзывы покупателей", url="https://t.me/MEFEDRONOTZ"))

    bot.send_message(
        msg.chat.id,
        "☑️ <b>Только оригинальный товар</b>",
        reply_markup=kb
    )

# ---------------- КОНТАКТЫ ----------------
@bot.message_handler(func=lambda m: m.text == "📞 Контакты / FAQ")
def faq(msg):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        "Пользовательское соглашение",
        callback_data="policy"
    ))

    bot.send_message(
        msg.chat.id,
        "📞 <b>Мессенджер для связи:</b>\n\n"
        "Telegram - @MEFEDRONYT\n\n"
        "Ответы на общие вопросы - @HEMEFEDRON\n\n"
        "В нашем магазине в продажу поступает только оригинальная продукция и вещи, которые редко можно встретить в РФ.\n\n"
        "Любые легит проверки наш товар пройдет.\n\n"
        "Совершая оплату, вы соглашаетесь с политикой конфиденциальности и пользовательским соглашением.",
        reply_markup=kb
    )

# ---------------- CALLBACK ----------------
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    uid = call.from_user.id

    # История покупок
    if call.data == "history":
        sql.execute("SELECT product, delivery, track FROM orders WHERE user_id=?", (uid,))
        rows = sql.fetchall()

        if not rows:
            bot.answer_callback_query(call.id, "Покупок пока нет")
            return

        text = "📜 <b>История покупок:</b>\n\n"
        for x in rows:
            text += f"{x[0]}\n🚚 {x[1]}\n📦 {x[2]}\n\n"

        bot.send_message(call.message.chat.id, text)

    # Политика
    elif call.data == "policy":
        bot.send_message(
            call.message.chat.id,
            "📄 <b>Пользовательское соглашение</b>\n\n"
            "1. После оплаты заказ считается оформленным.\n"
            "2. Возврат возможен только при браке.\n"
            "3. Сроки доставки зависят от службы доставки.\n"
            "4. Оформляя заказ, клиент соглашается с условиями магазина.\n"
            "5. Личные данные не передаются третьим лицам."
        )

    # Выбор бренда
    elif call.data.startswith("brand_"):
        brand = call.data.replace("brand_", "")

        kb = types.InlineKeyboardMarkup()

        for item in catalog[brand]:
            name = item[0]
            price = item[1]
            kb.add(types.InlineKeyboardButton(
                f"{name} — {price}₽",
                callback_data=f"item_{brand}|{name}|{price}"
            ))

        bot.edit_message_text(
            f"🛍 <b>{brand}</b>\nВыберите товар:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=kb
        )

    # Выбор товара
    elif call.data.startswith("item_"):
        data = call.data.replace("item_", "")
        brand, name, price = data.split("|")

        temp_orders[uid] = {
            "brand": brand,
            "product": f"{name} — {price}₽"
        }

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Яндекс", callback_data="delivery_Яндекс"))
        kb.add(types.InlineKeyboardButton("СДЭК", callback_data="delivery_СДЭК"))
        kb.add(types.InlineKeyboardButton("Авито", callback_data="delivery_Авито"))

        bot.send_message(call.message.chat.id, "🚚 Выберите доставку:", reply_markup=kb)

    # Выбор доставки
    elif call.data.startswith("delivery_"):
        delivery = call.data.replace("delivery_", "")
        temp_orders[uid]["delivery"] = delivery

        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("💳 Оплатить по СПБ", callback_data="pay"))

        bot.send_message(
            call.message.chat.id,
            "💳 <b>Оплатите заказ по СПБ</b>\n\n"
            "Номер: 79870920666\n"
            "Банк: Т-банк\n"
            "Получатель: Айдар Г.",
            reply_markup=kb
        )

    # Оплата
    elif call.data == "pay":
        order = temp_orders[uid]
        track = track_gen()

        sql.execute("""
        INSERT INTO orders(user_id, product, brand, delivery, track, date)
        VALUES(?,?,?,?,?,?)
        """, (
            uid,
            order["product"],
            order["brand"],
            order["delivery"],
            track,
            time.strftime("%d.%m.%Y")
        ))
        db.commit()

        bot.send_message(
            call.message.chat.id,
            "✅ <b>Оплата подтверждена</b>\n\n"
            f"Товар: {order['product']}\n"
            f"Доставка: {order['delivery']}\n"
            f"Трек номер: <code>{track}</code>\n\n"
            "Ожидайте отправку товара."
        )

# ---------------- RUN ----------------
bot.remove_webhook()
bot.infinity_polling()
