import os
from aiogram import Bot
import asyncio

# Telegram-Bot-Token
bot_token = "7088435202:AAEiMKtFxJQvA3Shdcv8sQP6vGxyOKt7Ktw"
bot = Bot(token=bot_token)

# Kategorien und zugehörige Thread-IDs
category_thread_ids = {
    "Art, Artist Support and Event Management": 2,
    "Musicians and Singers": 5,
    "Education, Pedagogical and Social": 6,
    "Stage and Event Technology": 7,
    "Costume, Makeup and Fashion": 8,
    "Acting, Theater and Directing": 9,
    "Legal and Financial": 10,
    "Communication, PR and Press": 11,
    "IT and Digital": 27,
    "Customer Service, Catering and Cash Register": 12,
    "Other": 29
}

# Die Funktion, die die Nachrichten sendet
async def send_job_to_telegram(category, job_title, employer, job_link):
    chat_id = -1002417180355  # Chat-ID
    thread_id = category_thread_ids.get(category)  # Hole die passende Thread-ID basierend auf der Kategorie

    if thread_id:
        message = f"{job_title}\nEmployer: {employer}\nLink: {job_link}"

        # Ausgabe im Terminal
        print(f"Sending to {category} thread ({thread_id}):\n{message}")

        # Nachricht senden
        await bot.send_message(chat_id=chat_id, text=message, reply_to_message_id=thread_id)

# Funktion zum Lesen der Daten und Aufteilen nach "---"
def process_file(filename):
    with open(filename, "r") as file:
        data = file.read()

    # Zerlege die Daten in Abschnitte basierend auf "---"
    sections = data.split("---")

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Extrahiere Job-Informationen
        lines = section.splitlines()

        # Wir gehen davon aus, dass die erste Zeile die Kategorie ist
        category = lines[0].strip("[]")  # Entferne die eckigen Klammern der Kategorie
        if category not in category_thread_ids:
            continue  # Wenn die Kategorie nicht existiert, überspringen

        # Die restlichen Zeilen sind Job-Details
        job_title = None
        employer = None
        job_link = None

        for line in lines[1:]:
            if line.startswith("Job Title:"):
                job_title = line[len("Job Title:"):].strip()
            elif line.startswith("Employer:"):
                employer = line[len("Employer:"):].strip()
            elif line.startswith("Link:"):
                job_link = line[len("Link:"):].strip()

        if job_title and employer and job_link:
            # Sende die Nachricht an Telegram
            asyncio.run(send_job_to_telegram(category, job_title, employer, job_link))

# Hauptfunktion
if __name__ == "__main__":
    # Dein Datei-Name
    process_file("categorized_jobs.txt")
