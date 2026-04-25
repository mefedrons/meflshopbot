import telebot
from telebot import types

TOKEN = "8763154419:AAFaaCS4i0hNXGwAOgGK82WVjmBFWRtaeAw"
MANAGER = "@mefedronshope"

bot = telebot.TeleBot(TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛍 Каталог", "🔥 Новинки")
    markup.row("⭐ Отзывы", "📦 Как заказать")
    markup.row("📞 Контакты")
    return markup

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🔥 <b>Добро пожаловать в mefl•shop</b>\n\n"
        "В этом боте можно посмотреть актуальный каталог одежды, выбрать бренд, узнать цены и быстро оформить заказ.\n\n"
        "У нас:\n"
        "• Stone Island\n"
        "• C.P. Company\n"
        "• Dolce & Gabbana\n"
        "• другие бренды\n\n"
        "Ниже кнопки для навигации 👇",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: True)
def menu(message):
    text = message.text

    if text == "🛍 Каталог":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("Stone Island", "C.P. Company")
        markup.row("D&G", "Другие бренды")
        markup.row("⬅️ Назад")
        bot.send_message(message.chat.id, "Выбери бренд:", reply_markup=markup)

    elif text == "Stone Island":
        bot.send_message(
            message.chat.id,
            "🧥 <b>Stone Island</b>\n\n"
            "1. Hoodie Black — 6 990₽\n"
            "Размеры: M / L / XL\n\n"
            "2. Soft Shell Jacket — 11 990₽\n"
            "Размеры: L / XL\n\n"
            f"Для заказа: {MANAGER}",
            parse_mode="HTML"
        )

    elif text == "C.P. Company":
        bot.send_message(
            message.chat.id,
            "👕 <b>C.P. Company</b>\n\n"
            "1. Zip Hoodie — 7 490₽\n"
            "Размеры: M / L\n\n"
            "2. Jacket — 12 990₽\n"
            "Размеры: L / XL\n\n"
            f"Для заказа: {MANAGER}",
            parse_mode="HTML"
        )

    elif text == "D&G":
        bot.send_message(
            message.chat.id,
            "👔 <b>Dolce & Gabbana</b>\n\n"
            "1. Tee Black — 5 990₽\n"
            "Размеры: M / L / XL\n\n"
            "2. Sweatshirt — 8 490₽\n"
            "Размеры: L\n\n"
            f"Для заказа: {MANAGER}",
            parse_mode="HTML"
        )

    elif text == "Другие бренды":
        bot.send_message(
            message.chat.id,
            "🛒 <b>Другие бренды</b>\n\n"
            "• Premium Cargo Pants — 4 990₽\n"
            "• Oversize Hoodie Black — 4 590₽\n"
            "• Longsleeve Basic — 3 990₽\n\n"
            f"Для заказа: {MANAGER}",
            parse_mode="HTML"
        )

    elif text == "🔥 Новинки":
        bot.send_message(
            message.chat.id,
            "🔥 <b>Новинки mefl•shop</b>\n\n"
            "• Stone Island Hoodie — 6 990₽\n"
            "• C.P. Company Jacket — 12 990₽\n"
            "• D&G Tee — 5 990₽\n\n"
            "Наличие обновляется регулярно.",
            parse_mode="HTML"
        )

    elif text == "⭐ Отзывы":
        bot.send_message(
            message.chat.id,
            "⭐ <b>Отзывы</b>\n\n"
            "Отзывы скоро будут добавлены.\n\n"
            "Пока можешь написать менеджеру и запросить реальные отзывы/скрины заказов.",
            parse_mode="HTML"
        )

    elif text == "📦 Как заказать":
        bot.send_message(
            message.chat.id,
            "📦 <b>Как оформить заказ</b>\n\n"
            "1. Выбери товар в каталоге\n"
            "2. Напиши менеджеру размер и модель\n"
            "3. Подтверждаем наличие\n"
            "4. Оплата / доставка\n\n"
            f"Менеджер: {MANAGER}",
            parse_mode="HTML"
        )

    elif text == "📞 Контакты":
        bot.send_message(
            message.chat.id,
            f"📞 <b>Контакты mefl•shop</b>\n\n"
            f"Telegram: {MANAGER}\n"
            "VK: vk.com/mefedronshope\n"
            "Поддержка: +7 (999) 000-00-00",
            parse_mode="HTML"
        )

    elif text == "⬅️ Назад":
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())

    else:
        bot.send_message(message.chat.id, "Выбери кнопку ниже 👇", reply_markup=main_menu())

bot.remove_webhook()
bot.infinity_polling()
