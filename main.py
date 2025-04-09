
import os
import time
import datetime
import pytz
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

messages_schedule = {
    "07:00": "Доброе утро, зая! Зарядочка уже ждёт тебя!",
    "07:30": "Ты моя нежная и прекрасная, не забудь зарядить телефон!",
    "08:00": "Привет, моя любовь! Телефон жив?",
    "08:30": "Как настроение? А телефон на зарядке?",
    "09:00": "Пора и зарядиться!",
    "15:00": "Днём тоже не забывай о зарядке!",
    "20:00": "Вечер без зарядки — не вечер!",
    "21:00": "Ещё немного — и день окончен. А зарядка?",
    "22:00": "Пора на зарядку, как и тебе — на отдых!",
    "23:00": "Без телефона ты как без крыльев. Заряди!",
    "00:00": "Спокойной ночи, зая. Но сперва зарядка!"
}

sent_today = set()

def send_message(text):
    for chat_id in CHAT_IDS:
        chat_id = chat_id.strip()
        if chat_id:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {"chat_id": chat_id, "text": text}
            try:
                response = requests.post(url, data=payload)
                print(f"{datetime.datetime.now()}: '{text}' → {chat_id} ({response.status_code})")
            except Exception as e:
                print(f"Ошибка при отправке: {e}")

def get_germany_time():
    tz = pytz.timezone("Europe/Berlin")
    return datetime.datetime.now(tz)

if __name__ == "__main__":
    send_message("Бот запущен. Проверка связи.")
    while True:
        now = get_germany_time()
        current_time = now.strftime("%H:%M")

        if current_time in messages_schedule and current_time not in sent_today:
            send_message(messages_schedule[current_time])
            sent_today.add(current_time)

        if current_time == "01:00":
            sent_today.clear()

        time.sleep(30)
