from random import choice
from glob import glob
import telebot
from telebot import types
import requests as r

KEY = '5126890620:AAEw-CztNB-4rldEnhO9MVrUfXafHZvSWVQ'

bot = telebot.TeleBot(KEY)


@bot.message_handler(commands=['start'])                            
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ['Обновить', 'Новости', 'Погода', 'Курсы валют', 'Хряк))))']
    for i in range(len(buttons)):
        item = types.KeyboardButton(buttons[i])
        markup.add(item)

    bot.send_message(msg.chat.id, 'Что хочешь?', reply_markup=markup)


@bot.message_handler(content_types='text')                                               
def actions(msg):
    buttons = ['Обновить', 'Новости', 'Погода', 'Курсы валют', 'Хряк))))']

    if msg.text == 'Обновить':
        start(msg)

# news

    if msg.text == 'Новости':
        dot = '\u25CF'
        message = 'Главные новости на сегодня:' + '\n' * 2
        url = 'https://newsapi.org/v2/top-headlines?country=ru&apiKey=c86169d8dfb14848a46619b9f6d4006a'
        response = r.get(url)
        data = response.json()
        for i in range(10):
            message += f"{dot} {data['articles'][i]['title']}\n{data['articles'][i]['url']}" + '\n' * 2
        bot.reply_to(msg, message)

# weather

    if msg.text == 'Погода':
        bot.reply_to(msg, 'Напиши название населенного пункта')
    if str(msg.text) not in buttons:
            coordURL = f"http://api.openweathermap.org/geo/1.0/direct?q={str(msg.text)}&limit=5&appid=2dd9ea7ad178166dee8752723832cd70"
            coordRESPONSE = r.get(coordURL)
            coordDATA = coordRESPONSE.json()
            if coordDATA!=[]:
                lat = f"{coordDATA[0]['lat']}"
                lon = f"{coordDATA[0]['lon']}"
                weatherURL = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid=2dd9ea7ad178166dee8752723832cd70"
                weatherRESPONSE = r.get(weatherURL)
                weatherDATA = weatherRESPONSE.json()
                message = f"Сейчас на улице:" + '\n' * 2 \
                    + f"{weatherDATA['weather'][0]['description']}" + '\n' \
                    + f"Температура: {weatherDATA['main']['temp']}" + '\n' \
                    + f"Ощущается как: {weatherDATA['main']['feels_like']}" + '\n' \
                    + f"Мин: {weatherDATA['main']['temp_min']}" + '\n' \
                    + f"Макс: {weatherDATA['main']['temp_max']}" + '\n' \
                    + f"Влажность: {weatherDATA['main']['humidity']}" '\n'
                bot.send_location(msg.chat.id, float(lat), float(lon))
                bot.reply_to(msg, message)

# currencies

    if msg.text == 'Курсы валют':                                                         
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

# PIGGIE

    if msg.text == 'Хряк))))':                                                             
        pigs = glob('imgs/*')
        pig = choice(pigs)
        f = open(pig, 'rb')
        bot.send_photo(msg.chat.id, f)
        f.close()

bot.infinity_polling()
