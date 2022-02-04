from random import choice
from glob import glob
import telebot
from telebot import types
import requests as r

KEY = '5126890620:AAEw-CztNB-4rldEnhO9MVrUfXafHZvSWVQ'

bot = telebot.TeleBot(KEY)


@bot.message_handler(commands=['start'])                                         # the main menu
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Покажи новости')
    item2 = types.KeyboardButton('Покажи курсы валют')
    item3 = types.KeyboardButton('Пополнить словарный запас')
    item4 = types.KeyboardButton('Покажи хряка')
    item5 = types.KeyboardButton('Покажи панков')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    markup.add(item5)
    bot.send_message(msg.chat.id, 'Что хочешь?', reply_markup=markup)


@bot.message_handler(content_types='text')                                               # news
def buttons(msg):
    if msg.text == 'Покажи новости':
        dot = '\u25CF'
        message = 'Главные новости на сегодня:' + '\n' * 2
        url = 'https://newsapi.org/v2/top-headlines?country=ru&apiKey=c86169d8dfb14848a46619b9f6d4006a'
        response = r.get(url)
        data = response.json()
        for i in range(20):
            message += f"{dot} {data['articles'][i]['title']}\n{data['articles'][i]['url']}" + '\n' * 2
        bot.reply_to(msg, message)

    if msg.text == 'Покажи курсы валют':                                                         # currencies
        GBP = 'https://v6.exchangerate-api.com/v6/b15cca4a04289cbfe1d610a2/latest/GBP'
        EUR = 'https://v6.exchangerate-api.com/v6/b15cca4a04289cbfe1d610a2/latest/EUR'
        USD = 'https://v6.exchangerate-api.com/v6/b15cca4a04289cbfe1d610a2/latest/USD'
        gbp = r.get(GBP)
        eur = r.get(EUR)
        usd = r.get(USD)
        dataGBP = gbp.json()
        dataEUR = eur.json()
        dataUSD = usd.json()
        rep = f"1 USD = {dataUSD['conversion_rates']['RUB']} RUB" + '\n' \
              f"1 EUR = {dataEUR['conversion_rates']['RUB']} RUB" + '\n' \
              f"1 GBP = {dataGBP['conversion_rates']['RUB']} RUB"
        bot.reply_to(msg, rep)

    if msg.text == 'Пополнить словарный запас':                                    # enrichment
        f = open('word.txt')
        lines = f.readlines()
        url = choice(lines)
        bot.send_message(msg.chat.id, url)
        f.close()

    if msg.text == 'Покажи панков':                                                 # punks
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Услада для ушей')
        item2 = types.KeyboardButton('Крутая репетиция')
        item3 = types.KeyboardButton('Крутые соседи')
        item4 = types.KeyboardButton('С новым годом!!!')
        item5 = types.KeyboardButton('Замерзшие пельмени куда-то едут под дикие оры панков')
        item6 = types.KeyboardButton('Вернуться назад')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(msg.chat.id, 'Ну давай, выбирай :)', reply_markup=markup)

    if msg.text == 'Услада для ушей':
        bot.send_message(msg.chat.id, 'https://vm.tiktok.com/ZSeg5Xvsa/')
    elif msg.text == 'Крутая репетиция':
        bot.send_message(msg.chat.id, 'https://vm.tiktok.com/ZSeg5yBmr/')
    elif msg.text == 'Крутые соседи':
        bot.send_message(msg.chat.id, 'https://vm.tiktok.com/ZSeg5DdWn/')
    elif msg.text == 'С новым годом!!!':
        bot.send_message(msg.chat.id, 'https://vm.tiktok.com/ZSeg5yGR7/')
    elif msg.text == 'Замерзшие пельмени куда-то едут под дикие оры панков':
        bot.send_message(msg.chat.id, 'https://vm.tiktok.com/ZSegm63pF/')

    if msg.text == 'Покажи хряка':                                                          # PIGGIE
        pigs = glob('imgs/*')
        pig = choice(pigs)
        f = open(pig, 'rb')
        bot.send_photo(msg.chat.id, f)
        f.close()

    if msg.text == 'Вернуться назад':
        start(msg)


bot.infinity_polling()
