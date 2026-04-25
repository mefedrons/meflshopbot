import telebot
from telebot import types
import os

TOK. TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Каталог", "Контакты")
    markup.row("Заказать")

    bot.send_message(
        message.chat.id,
        "Добро пожаловать в mefl•shop 🔥\nБрендовая одежда в наличии.",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def msg(message):
    if message.text == "Каталог":
        bot.send_message(message.chat.id,
        "Stone Island Hoodie — 6990₽\n"
        "CP Company Jacket — 9990₽\n"
        "D&G Tee — 4990₽")

    elif message.text == "Контакты":
        bot.send_message(message.chat.id,
        "Telegram: @mefedronshope")

    elif message.text == "Заказать":
        bot.send_message(message.chat.id,
        "Напиши менеджеру: @mefedronshope")

    else:
        bot.send_message(message.chat.id, "Нажми кнопку ниже.")

bot.infinity_polling()
