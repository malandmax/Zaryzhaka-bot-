
import os
import time
import random
import logging
import datetime
import pytz
import requests

TOKEN = "7194435988:AAGfGHdjMigOTj14XlANeVtO-QnD0I0yXps"
USER_ID = "6184719147"

# Сообщения
messages = {
    "morning": [
        "Доброе утро, зая! Подключи зарядку, пожалуйста❤️.",
        "Зарядка — залог здоровья. Начинай!",
        "Утренняя забота😉: не забудь зарядить телефон.",
        "7:30 — ты зарядилась энергией?",
        "Порадуй меня — порадуй телефон! Вставляй 😉",
        "Я всё ещё надеюсь, что телефон уже на зарядке.",
        "8:00 — всё ещё 13%?",
        "Любимая, зарядка не шутка. Хихик!",
        "Ты же знаешь, я утомлю)) давай - заряжай)."
    ],
    "evening": [
        "Вечерняя проверка: зарядка включена?",
        "Нежно напоминаю: пора заряжать телефон.",
        "21:00 — а зарядка?",
        "22:00 — ещё не на зарядке?",
        "Последний шанс! Поставь телефон на зарядку.",
        "Спокойствие в семье — зарядка в гнезде.",
        "Сделай хорошо - вставь поглубже."
    ],
    "late": [
        "Последнее предупреждение и ложись спать.",
        "Ты точно хочешь, чтобы он умер?-действуй!",
        "Я не шучу. Подключи зарядку.",
        "Мы в ответе за тех, кого не заряжаем.",
        "Даже когда я сплю - бот следит.",
        "Последний звонок. Или потом будет звонка).",
        "Если не на зарядке — я плакать."
    ],
    "special": "я заместитель Андрея Максимовича по напоминаниям о необходимости зарядки. Он Вас безумно любит и передаёт, что Вы его покорная Госпожа"
}

# Время по Берлину
berlin = pytz.timezone("Europe/Berlin")

# Часы отправки
schedule = {
    "morning": [7, 7.5, 8, 8.5, 9],
    "evening": [15, 20, 21, 22],
    "late": [23],
    "special": [17.5]
}

# Проверка текущего времени
def get_current_hour():
    now = datetime.datetime.now(berlin)
    return now.hour + now.minute / 60.0

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": USER_ID, "text": text}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        logging.error(f"Error sending message: {e}")

def main():
    hour = get_current_hour()
    logging.basicConfig(filename="bot_log.txt", level=logging.INFO)
    logging.info(f"{datetime.datetime.now(berlin)} | Executed hour: {hour}")

    tasks = 0
    for period, times in schedule.items():
        for t in times:
            if abs(hour - t) < 0.1:
                if period == "special":
                    send_message(messages["special"])
                else:
                    send_message(random.choice(messages[period]))
                tasks += 1
                break

    logging.info(f"{datetime.datetime.now(berlin)} | Executed hour: {hour}, tasks={tasks}")

if __name__ == "__main__":
    main()
