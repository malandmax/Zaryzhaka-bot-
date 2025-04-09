
import os
import time
import random
import logging
import datetime
import pytz
import requests

TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS", "").split(",")

# Твоё локальное системное время (по хостингу)
local = datetime.datetime.now().astimezone().tzinfo
berlin = pytz.timezone("Europe/Berlin")

# Расписание для жены по Берлину
wife_schedule = {
    7: "morning", 7.5: "morning", 8: "morning", 8.5: "morning", 9: "morning",
    15: "evening", 20: "evening", 21: "evening", 22: "evening",
    23: "late", 0: "late"
}

# Расписание "запись" по системному времени (твое текущее местное время)
your_schedule = [8.966, 9.966, 10.966, 11.966, 20.966, 21.966, 22.966, 23.966]

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
    ]
}

def send(text, cid):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": cid.strip(), "text": text})
    except Exception as e:
        print(f"Ошибка отправки {cid}: {e}")

def hour_now(tz):
    now = datetime.datetime.now(tz)
    return now.hour + now.minute / 60.0

def main():
    log = []
    h_local = hour_now(local)
    h_berlin = hour_now(berlin)

    wife_id = CHAT_IDS[0]
    me_id = CHAT_IDS[1]

    if any(abs(h_local - t) < 0.05 for t in your_schedule):
        send("запись", me_id)
        log.append("запись отправлена")

    for h, category in wife_schedule.items():
        if abs(h_berlin - h) < 0.05:
            send(random.choice(messages[category]), wife_id)
            log.append(f"{category} отправлено жене")
            break

    with open("bot_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | Берлин: {h_berlin:.2f}, Локальное: {h_local:.2f} | {log}\n")

send("Тестовое сообщение: бот запущен", CHAT_IDS[1])

if __name__ == "__main__":
    main()
