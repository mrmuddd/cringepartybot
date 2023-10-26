from random import choice
from glob import glob
import telebot
from telebot import types
import requests as r
from bs4 import BeautifulSoup as bs


KEY = '5126890620:AAEw-CztNB-4rldEnhO9MVrUfXafHZvSWVQ'

bot = telebot.TeleBot(KEY)

buttons = ['Обновить', 'Небо над головой 🔭', 'Погода 🌦', 'Курсы валют 😭', 'Новости 💀', 'ХРЯК 🐖', 'КАБАН 🦍']
@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('Обновить')
    markup.row(types.KeyboardButton('Небо 🔭', request_location=True), 'Погода 🌦')
    markup.row('Земля 🌎', 'Солнце ☀')
    markup.row('Курсы валют 😭', 'Новости 💀')
    markup.row('ХРЯК 🐖', 'КАБАН 🦍')

    bot.send_message(msg.chat.id, 'Что хочешь?', reply_markup=markup)


@bot.message_handler(content_types=['text','location','InputMediaPhoto','animation'])
def actions(msg):
    if msg.text == 'Обновить':
        start(msg)

    # weather

    if msg.text == 'Погода 🌦':
        bot.reply_to(msg, 'Напиши название населенного пункта')
        @bot.message_handler(content_types=['text'])
        def weather(msg):
                coord_url = f"http://api.openweathermap.org/geo/1.0/direct?q={str(msg.text)}&limit=5&appid=2dd9ea7ad178166dee8752723832cd70"
                coord_data = r.get(coord_url).json()
                if coord_data != []:
                    lat = f"{coord_data[0]['lat']}"
                    lon = f"{coord_data[0]['lon']}"
                    weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&lang=ru&appid=2dd9ea7ad178166dee8752723832cd70"
                    weather_data = r.get(weather_url).json()

                    placeURL = f"https://www.geonames.org/search.html?q={str(msg.text)}"
                    soup = bs(r.get(placeURL).text, 'html.parser')
                    ids = [link['href'] for link in soup.find_all('a', href=True)]
                    ID = ids[6][1:8]

                    astroURL = f"https://www.meteoblue.com/en/weather/outdoorsports/seeing/" \
                               f"{coord_data[0]['name'].replace(' ', '-')}_" \
                               f"{coord_data[0]['country']}_{ID}"
                    astro_message = 'Астрономическая видимость:' + '\n' + astroURL

                    weather_message = f"Сейчас на улице:" + '\n' * 2 \
                                      + f"{weather_data['weather'][0]['description']}" + '\n' \
                                      + f"Температура: {weather_data['main']['temp']}" + '\n' \
                                      + f"Ощущается как: {weather_data['main']['feels_like']}" + '\n' \
                                      + f"Мин: {weather_data['main']['temp_min']}" + '\n' \
                                      + f"Макс: {weather_data['main']['temp_max']}" + '\n' \
                                      + f"Влажность: {weather_data['main']['humidity']}" '\n'

                    bot.send_location(msg.chat.id, float(lat), float(lon))
                    bot.reply_to(msg, astro_message)
                    bot.reply_to(msg, weather_message)
                else:
                    bot.reply_to(msg, 'Не знаю такого😭😭😭')

        bot.register_next_step_handler(msg, weather)

    #Earth pics

    if msg.text == 'Земля 🌎':
        url = 'https://api.nasa.gov/EPIC/api/natural/images?api_key=iCd9fDWK0WiK09yYma0dW5w1dNbRYjVaDx8Ho2bk'
        data = r.get(url).json()
        imgs = []
        dates = []
        count = 0
        message = bot.send_message(msg.chat.id, f'Загрузка изображений: {count}/{len(data)}')
        for i in data:
            dates.append(i['date'])
            count+=1
            img = r.get(f"https://epic.gsfc.nasa.gov./epic-archive/jpg/{i['image']}.jpg").content
            imgs.append(types.InputMediaPhoto(img))
            bot.edit_message_text(f'Загрузка изображений: {count}/{len(data)}', msg.chat.id, message.message_id)
            
        bot.delete_message(msg.chat.id, message.message_id)
        for i in range(len(dates)):
            dates[i] = f"{i+1} снимок: "+str(dates[i])
        bot.send_media_group(msg.chat.id, imgs[0:10])
        if len(imgs) > 10:
            bot.send_media_group(msg.chat.id, imgs[10:len(imgs)])
        bot.send_message(msg.chat.id, 'NOAA DSCOVR - последние снимки' + '\n\n'
                         + 'Дата и время (YYYY-MM-DD, UTC+0): ' + f'\n\n' + '\n'.join(map(str, dates)))

    #sun

    if msg.text == 'Солнце ☀':
        aurora = r.get('https://services.swpc.noaa.gov/images/aurora-forecast-northern-hemisphere.jpg').content
        message = bot.send_message(msg.chat.id,'Загрузка видео: 0/2')
        soho_c3_data = r.get('https://soho.nascom.nasa.gov/data/LATEST/current_c3small.mp4', stream=True).content
        bot.edit_message_text('Загрузка видео: 1/2', msg.chat.id, message.message_id)
        soho_c2_data = r.get('https://soho.nascom.nasa.gov/data/LATEST/current_c2small.mp4', stream=True).content
        bot.edit_message_text('Загрузка видео: 2/2', msg.chat.id, message.message_id)
        bot.send_video(msg.chat.id, soho_c3_data, caption='LASCO C3')
        bot.send_video(msg.chat.id, soho_c2_data, caption='LASCO C2')
        bot.send_photo(msg.chat.id, aurora, reply_to_message_id=msg.message_id, caption='Вероятность сияния - прогноз на 30 минут')
        bot.delete_message(msg.chat.id, message.message_id)

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
        RUB = 'https://v6.exchangerate-api.com/v6/b15cca4a04289cbfe1d610a2/latest/RUB'
        dataGBP = r.get(GBP).json()
        dataEUR = r.get(EUR).json()
        dataUSD = r.get(USD).json()
        dataRUB = r.get(RUB).json()
        rep = f"1 USD = {dataUSD['conversion_rates']['RUB']} RUB" + '\n' \
              f"1 EUR = {dataEUR['conversion_rates']['RUB']} RUB" + '\n' \
              f"1 GBP = {dataGBP['conversion_rates']['RUB']} RUB" + '\n' \
              f"1 RUB = {dataRUB['conversion_rates']['KRW']} KRW" + '\n' \
              f"1 RUB = {dataRUB['conversion_rates']['MNT']} MNT"
        bot.reply_to(msg, rep)

    # news

    if msg.text == 'Новости 💀':
        dot = '\u25CF'
        message = 'Главные новости на сегодня:' + '\n' * 2
        url = 'https://newsapi.org/v2/top-headlines?country=ru&apiKey=c86169d8dfb14848a46619b9f6d4006a'
        data = r.get(url).json()
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

    if msg.text == 'КАБАН 🦍':
        pigs = glob('cabany/*')
        pig = choice(pigs)
        f = open(pig, 'rb')
        bot.send_photo(msg.chat.id, f)
        f.close()

bot.infinity_polling()
