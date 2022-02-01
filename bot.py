from random import choice
from glob import glob
import telebot
from telebot import types
import requests as r

KEY = '5126890620:AAEw-CztNB-4rldEnhO9MVrUfXafHZvSWVQ'
NEWS_KEY = 'c86169d8dfb14848a46619b9f6d4006a'

bot = telebot.TeleBot(KEY)


@bot.message_handler(commands=['start'])                                         # the main menu
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Покажи новости')
    item2 = types.KeyboardButton('Пополнить словарный запас')
    item3 = types.KeyboardButton('Покажи хряка')
    item4 = types.KeyboardButton('Покажи панков')
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item4)
    bot.send_message(msg.chat.id, 'Что хочешь?', reply_markup=markup)


@bot.message_handler(content_types='text')                                               # news
def buttons(msg):
    if msg.text == 'Покажи новости':
        message = ''
        url = 'https://newsapi.org/v2/top-headlines?country=ru&apiKey=c86169d8dfb14848a46619b9f6d4006a'
        response = r.get(url)
        data = response.json()
        for i in range(10):
            message += format(str(data['articles'][i]['title']) + '\n' + '\n')
        bot.reply_to(msg, message)

    if msg.text == 'Пополнить словарный запас':                                       # enrichment
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('A snapchat pic')
        item2 = types.KeyboardButton('Quaaludes')
        item3 = types.KeyboardButton('Вернуться назад')
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        bot.send_message(msg.chat.id, 'Ну давай, выбирай :)', reply_markup=markup)

    if msg.text == 'A snapchat pic':
        bot.send_message(msg.chat.id, 'https://youtu.be/ll5xceTACEI')
    elif msg.text == 'Quaaludes':
        bot.send_message(msg.chat.id, 'https://youtu.be/IG2JF0P4GFA')

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
        bot.send_photo(msg.chat.id, open(pig, 'rb'))

    if msg.text == 'Вернуться назад':
        start(msg)


bot.infinity_polling()
