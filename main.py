
import os
import time
import logging
import datetime
import pytz
import requests

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Переменные окружения
TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")
WIFE_ID = os.getenv("WIFE_ID")

# Список ID для отправки
CHAT_IDS = [USER_ID, WIFE_ID]

# Берлинское время
berlin = pytz.timezone("Europe/Berlin")

# Расписание (время в часах)
user_schedule = [20.966, 21.966, 22.966, 23.966, 8.966, 9.966, 10.966, 11.966]
wife_schedule = [7, 7.5, 8, 8.5, 9, 15, 20, 21, 22, 23, 0]

# Сообщения
messages = {
    "user": "запись",
    "morning": [
        "Доброе утро, зая! Подключи зарядку!",
        "Зарядка – залог здоровья. Начинай с телефона!",
        "Утренняя забота: не забудь зарядить.",
        "7:30 — ты зарядилась энергией?",
        "Порадуй меня — порадуй телефон зарядкой!"
    ],
    "day": [
        "Ты же не забыла зарядку, да?",
        "Сколько процентов осталось?",
        "Я надеюсь, ты уже подключила зарядку.",
        "Любимая, давай без риска — заряди!"
    ],
    "late": [
        "Ты опять без зарядки? Ай-ай-ай!",
        "23:00 — а ты всё ещё не зарядила?",
        "Перед сном обязательно подключи зарядку!"
    ],
    "demand": [
        "00:00! Зарядка срочно!",
        "Я СКАЗАЛ ПОДКЛЮЧИ ЗАРЯДКУ!",
        "ЭТО УЛЬТИМАТУМ: ЗАРЯДКА!"
    ]
}

def get_current_hour():
    now = datetime.datetime.now(berlin)
    return now.hour + now.minute / 60

def send(text, chat_id):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, data=payload)
        logging.info(f"Отправлено сообщение '{text}' для {chat_id}: {response.status_code}")
    except Exception as e:
        logging.error(f"Ошибка отправки сообщения для {chat_id}: {e}")

def main():
    hour = get_current_hour()
    logging.info(f"Текущее время: {hour}")

    # USER (ты)
    if any(abs(hour - t) < 0.05 for t in user_schedule):
        send(messages["user"], CHAT_IDS[0])

    # WIFE (жена)
    if any(abs(hour - t) < 0.05 for t in wife_schedule):
        if hour < 12:
            send(random_choice("morning"), CHAT_IDS[1])
        elif hour < 18:
            send(random_choice("day"), CHAT_IDS[1])
        elif hour < 23.5:
            send(random_choice("late"), CHAT_IDS[1])
        else:
            send(random_choice("demand"), CHAT_IDS[1])

def random_choice(period):
    import random
    return random.choice(messages[period])

if __name__ == "__main__":
    main()
