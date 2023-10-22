FROM python:3.8.0

WORKDIR /bot

COPY requirements.txt /bot/
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install nodejs -y
RUN apt-get install npm -y

COPY . /bot

CMD python bot.py
