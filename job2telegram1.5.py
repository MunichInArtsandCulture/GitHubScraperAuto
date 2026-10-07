import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Load API token and chat ID from environment / .env
API_TOKEN = os.getenv('BOT_TOKEN') or os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '-1002417180355')

CATEGORY_THREAD_IDS = {
    'Art, Artist Support and Event Management': 2,
    'Musicians and Singers': 5,
    'Education, Pedagogical and Social': 6,
    'Stage and Event Technology': 7,
    'Costume, Makeup and Fashion': 8,
    'Acting, Theater and Directing': 9,
    'Legal and Financial': 10,
    'Communication, PR and Press': 11,
    'IT and Digital': 27,
    'Customer Service, Catering and Cash Register': 12,
    'Other': 29,
}


def send_job_to_telegram(category: str, job_title: str, employer: str, job_link: str):
    if not API_TOKEN:
        print("⚠️  [Telegram] Kein BOT_TOKEN / TELEGRAM_BOT_TOKEN gesetzt. Nachricht übersprungen.")
        return

    thread_id = CATEGORY_THREAD_IDS.get(category, 2)
    message = f"<b>{job_title}</b>\n\n<b>Employer:</b> {employer}\n<b>Link:</b> <a href='{job_link}'>{job_link}</a>"

    print(f"📤 Sende Job an Telegram (Topic {thread_id} - {category}):\n{job_title} ({employer})\n")

    url = f"https://api.telegram.org/bot{API_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": thread_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }

    try:
        resp = requests.post(url, json=payload, timeout=15)
        if resp.status_code == 200:
            print("✅ Nachricht erfolgreich an Telegram gesendet.\n")
        else:
            print(f"⚠️  [Telegram API Error] HTTP {resp.status_code}: {resp.text}\n")
    except Exception as e:
        print(f"❌ [Telegram Error]: {e}\n")

    time.sleep(3)


def process_file(file_path: str):
    if not os.path.exists(file_path):
        print(f"⚠️  Datei '{file_path}' nicht gefunden.")
        return

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().splitlines()

    datapoints = []
    datapoint = []

    for line in content:
        if line.strip() == "---":
            if datapoint:
                datapoints.append(datapoint)
                datapoint = []
        else:
            datapoint.append(line)

    if datapoint:
        datapoints.append(datapoint)

    print(f"📋 Verarbeite {len(datapoints)} Jobs für den Telegram-Versand...")

    for datapoint in datapoints:
        if not datapoint:
            continue
        category_line = datapoint[0]
        category = category_line.strip("[]")
        job_title = ""
        employer = ""
        job_link = ""

        for line in datapoint:
            if line.startswith("Job Title: "):
                job_title = line.replace("Job Title: ", "").strip()
            elif line.startswith("Employer: "):
                employer = line.replace("Employer: ", "").strip()
            elif line.startswith("Link: "):
                job_link = line.replace("Link: ", "").strip()

        if job_title and employer and job_link:
            send_job_to_telegram(category, job_title, employer, job_link)


def main():
    if not API_TOKEN:
        print("⚠️  [Telegram Dispatcher] Kein BOT_TOKEN in Umgebungsvariablen gefunden. Überspringe Telegram-Versand.")
        return
    process_file("categorized_jobs.txt")


if __name__ == "__main__":
    main()
