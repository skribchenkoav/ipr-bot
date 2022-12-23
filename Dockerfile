FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install requests

RUN pip install aiogram

CMD ["python3", "./bot.py"]