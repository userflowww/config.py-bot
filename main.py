# main.py
import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы узнать цену на определённое количество валюты, введите команду в следующем формате:\n<имя валюты, цену которой вы хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\nНапример: USD RUB 100'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\nUSD - Доллар США\nEUR - Евро\nRUB - Российский рубль'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неверный формат команды.')

        base, quote, amount = values
        result = CurrencyConverter.get_price(base, quote, amount)
        text = f'Цена {amount} {base} в {quote} составляет {result:.2f}'
        bot.send_message(message.chat.id, text)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: {e}')


bot.polling(none_stop=True)