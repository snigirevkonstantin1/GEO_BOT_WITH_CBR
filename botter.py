from secrettoken import telegramtoken
import telebot
from telebot import apihelper
import time
from telebot import types
from cbparser import check_currency_nominal as ccn, check_currency_value as ccv
from ymap import closest_metro
import os
from flask import Flask, request

server = Flask(__name__)


token = telegramtoken
bot = telebot.TeleBot(token)
currensi = ['AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL', 'HUF', 'HKD', 'DKK', 'USD', 'EUR', 'INR', 'KZT', 'CAD', 'KGS', 'CNY', 'MDL', 'NOK', 'PLN', 'RON', 'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS', 'UAH', 'CZK', 'SEK', 'CHF', 'ZAR', 'KRW', 'JPY']


def keyboard():
    key = types.InlineKeyboardMarkup(row_width=12)
    buttons =[types.InlineKeyboardButton(text=c, callback_data=c) for c in currensi]
    key.add(*buttons)
    return key


@bot.callback_query_handler(func=lambda x: True)
def callback_handler(query):
    message = query.message
    text = query.data
    currency, value = ccv(text)
    nominal = ccn(text)
    if currency:
        bot.answer_callback_query(query.id,
                                  text="{} {} равен {} рублей".format(nominal, currency, value)
                                 )
    else:
        bot.send_message(chat_id=message.chat.id, text="Узнай курс валют")


def check_currency(message):
    if (message.content_type) == 'text':
        for c in currensi:
            if c in message.text.upper():
                return True
        return False



@bot.message_handler(func=check_currency)
def handle_currency(message):
    currency, value = ccv(message.text)
    nominal = ccn(message.text)
    if currency:
        bot.send_message(chat_id=message.chat.id, text="{} {} равен {} рублей".format(nominal, currency, value))
    else:
        bot.send_message(chat_id=message.chat.id, text="Узнай курс валют")


@bot.message_handler(content_types=['location'])
def handle_location(message):
    metro_adres, metro_lat, metro_lon, temp = closest_metro(message.location)
    bot.send_message(chat_id=message.chat.id, text="ближайшее метро - {}, сейчас {} градусов °C"
                     .format(metro_adres, temp))
    bot.send_location(message.chat.id,  metro_lon, metro_lat)


@bot.message_handler()
def handle_message(message):
    key = keyboard()
    bot.send_message(chat_id=message.chat.id, text="Узнай курс валют \nсписок доступных валют - {} "
                     .format((currensi)),
                     reply_markup=key)

@server.route('/' + token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://trybotter.herokuapp.com/' + token)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
