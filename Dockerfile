FROM python:3.8.0

WORKDIR /

COPY requirements.txt /
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install ffmpeg -y
RUN apt-get install nodejs -y
RUN apt-get install npm -y

COPY . /

CMD python bot.py
