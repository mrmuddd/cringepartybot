from random import choice
from glob import glob
import telebot
from telebot import types
import requests as r
from bs4 import BeautifulSoup as bs

KEY = '5126890620:AAEw-CztNB-4rldEnhO9MVrUfXafHZvSWVQ'

bot = telebot.TeleBot(KEY)

buttons = ['Обновить', 'Небо над головой 🔭', 'Погода 🌦', 'Курсы валют 😭', 'Новости 💀', 'ХРЯК 🐖']
@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(buttons)):
        if buttons[i] == 'Небо над головой 🔭':
            item = types.KeyboardButton(buttons[i],request_location=True)
        else:
            item = types.KeyboardButton(buttons[i])
        markup.add(item)

    bot.send_message(msg.chat.id, 'Что хочешь?', reply_markup=markup)


@bot.message_handler(content_types=['text','location'])
def actions(msg):
    if msg.text == 'Обновить':
        start(msg)

    # weather

    if msg.text == 'Погода 🌦':
        bot.reply_to(msg, 'Напиши название населенного пункта')
        @bot.message_handler(content_types=['text'])
        def weather(msg):
                coordURL = f"http://api.openweathermap.org/geo/1.0/direct?q={str(msg.text)}&limit=5&appid=2dd9ea7ad178166dee8752723832cd70"
                coordRESPONSE = r.get(coordURL)
                coordDATA = coordRESPONSE.json()
                if coordDATA != []:
                    lat = f"{coordDATA[0]['lat']}"
                    lon = f"{coordDATA[0]['lon']}"
                    weatherURL = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid=2dd9ea7ad178166dee8752723832cd70"
                    weatherRESPONSE = r.get(weatherURL)
                    weatherDATA = weatherRESPONSE.json()

                    placeURL = f"https://www.geonames.org/search.html?q={str(msg.text)}"
                    placeidRESPONSE = r.get(placeURL)
                    soup = bs(placeidRESPONSE.text, 'html.parser')
                    ids = [link['href'] for link in soup.find_all('a', href=True)]
                    ID = ids[6][1:8]

                    astroURL = f"https://www.meteoblue.com/en/weather/outdoorsports/seeing/" \
                               f"{coordDATA[0]['name'].replace(' ', '-')}_" \
                               f"{coordDATA[0]['country']}_{ID}"
                    astro_message = 'Астрономическая видимость:' + '\n' + astroURL

                    weather_message = f"Сейчас на улице:" + '\n' * 2 \
                                      + f"{weatherDATA['weather'][0]['description']}" + '\n' \
                                      + f"Температура: {weatherDATA['main']['temp']}" + '\n' \
                                      + f"Ощущается как: {weatherDATA['main']['feels_like']}" + '\n' \
                                      + f"Мин: {weatherDATA['main']['temp_min']}" + '\n' \
                                      + f"Макс: {weatherDATA['main']['temp_max']}" + '\n' \
                                      + f"Влажность: {weatherDATA['main']['humidity']}" '\n'

                    bot.send_location(msg.chat.id, float(lat), float(lon))
                    bot.reply_to(msg, astro_message)
                    bot.reply_to(msg, weather_message)
                else:
                    bot.reply_to(msg, 'Не знаю такого😭😭😭')

        bot.register_next_step_handler(msg, weather)

    #sky

    if msg.location is not None:
        lat = msg.location.latitude
        lon = msg.location.longitude
        url = f'https://www.heavens-above.com/SkyChart.aspx?lat={str(lat)}&lng={str(lon)}&loc=Unspecified&alt=0&tz=UCT'
        skyRESPONSE = r.get(url)
        soup = bs(skyRESPONSE.content, 'html.parser')
        image_soup = soup.select('img[id=ctl00_cph1_imgSkyChart]')
        image_url = image_soup[0]['src']
        img_data = r.get(f'https://www.heavens-above.com/{image_url}').content
        weatherURL = f"http://api.openweathermap.org/data/2.5/weather?lat={str(lat)}&lon={str(lon)}&units=metric&lang=ru&appid=2dd9ea7ad178166dee8752723832cd70"
        weatherRESPONSE = r.get(weatherURL)
        weatherDATA = weatherRESPONSE.json()
        place = weatherDATA['name']
        bot.send_photo(msg.chat.id, img_data, reply_to_message_id=msg.message_id,caption=f'Небо над {place}')

    # currencies

    if msg.text == 'Курсы валют 😭':
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

    # news

    if msg.text == 'Новости 💀':
        dot = '\u25CF'
        message = 'Главные новости на сегодня:' + '\n' * 2
        url = 'https://newsapi.org/v2/top-headlines?country=ru&apiKey=c86169d8dfb14848a46619b9f6d4006a'
        response = r.get(url)
        data = response.json()
        for i in range(10):
            message += f"{dot} {data['articles'][i]['title']}\n{data['articles'][i]['url']}" + '\n' * 2
        bot.reply_to(msg, message)

    # PIGGIE

    if msg.text == 'ХРЯК 🐖':
        pigs = glob('imgs/*')
        pig = choice(pigs)
        f = open(pig, 'rb')
        bot.send_photo(msg.chat.id, f)
        f.close()

bot.infinity_polling()
