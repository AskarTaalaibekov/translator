import telebot
from telebot import types
from dotenv import load_dotenv
import os
from googletrans import Translator

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot('BOT_TOKEN')
translator = Translator()

languages = {
    "Английский": "en",
    "Корейский": "ko",
    "Русский": "ru",
    "Китайский": "zh-cn",
    "Турецкий": "tr"
    }

selected_language = None

@bot.message_handler(commands=['start'])
def start(message):
    global selected_language
    selected_language = None

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for language in languages.keys():
        markup.add(types.KeyboardButton(language))

    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Я бот-переводчик. Выберите язык, на который хотите переводить:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text in languages.keys())
def set_language(message):
    global selected_language
    selected_language = languages[message.text]
    bot.send_message(
        message.chat.id,
        f"Вы выбрали язык: {message.text}. Теперь отправьте мне текст для перевода."
    )

@bot.message_handler(func=lambda message: True)
def translate_message(message):
    if selected_language:
        try:
            translation = translator.translate(message.text, dest=selected_language)
            bot.send_message(
                message.chat.id,
                f"Перевод:\n{translation.text}"
            )
        except Exception as e:
            bot.send_message(
                message.chat.id,
                "Ошибка перевода. Пожалуйста, попробуйте снова."
            )
    else:
        bot.send_message(
            message.chat.id,
            "Пожалуйста, сначала выберите язык для перевода с помощью команды /start."
        )

bot.polling(none_stop=True)
