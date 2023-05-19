import telebot
from telebot import types

from config import TOKEN, keys
from extensions import ConvertionException, CurceConverter

conv_markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
buttons = []
for val in keys.keys():
    buttons.append(types.KeyboardButton(val.capitalize()))

conv_markup.add(*buttons)





bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет! \n Увидеть список всех доступных валют: /values \n Начать конвертацию: /convert'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n' .join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(commands = ['convert'])
def values(message: telebot.types.Message):
    text = 'Выберете валюту, из которой конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=conv_markup)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'Выберете валюту, в которую конвертировать:'
    bot.send_message(message.chat.id, text, reply_markup=conv_markup)
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = 'Выберете количество валюты'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
       total_base = CurceConverter.convert(base, quote, amount)
    except ConvertionException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()




