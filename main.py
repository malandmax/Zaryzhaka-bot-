import os
import time
import datetime
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, data=payload)
    print(f"{datetime.datetime.now()} - Отправлено сообщение '{text}' для {chat_id}: {response.status_code}")
    return response

sent_flags = {chat_id: {hour: False for hour in [7, 7.5, 8, 8.5, 9, 15, 20, 21, 22, 23, 0]} for chat_id in CHAT_IDS}

while True:
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=2)
    current_hour = now.hour + now.minute / 60

    for chat_id in CHAT_IDS:
        for hour in sent_flags[chat_id]:
            if abs(current_hour - hour) < 0.01 and not sent_flags[chat_id][hour]:
                if hour < 9:
                    text = "Доброе утро, зая! Подключи зарядку!"
                elif hour < 21:
                    text = "Зай, зарядка где?"
                else:
                    text = "Ты что, всё ещё не зарядила телефон???"
                send_message(chat_id, text)
                sent_flags[chat_id][hour] = True

        # сброс флагов на новый день
        if now.hour == 1 and now.minute < 5:
            sent_flags[chat_id] = {hour: False for hour in sent_flags[chat_id]}

    time.sleep(60)
