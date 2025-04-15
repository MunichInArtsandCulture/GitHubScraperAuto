import asyncio
from aiogram import Bot
from aiogram.types import Message
from aiogram import exceptions

# Hier deinen API-Token einfügen
API_TOKEN = '7088435202:AAEiMKtFxJQvA3Shdcv8sQP6vGxyOKt7Ktw'
CHAT_ID = -1002417180355  # Die Chat-ID, in den die Nachrichten gesendet werden
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

bot = Bot(token=API_TOKEN)

async def send_job_to_telegram(category, job_title, employer, job_link):
    thread_id = CATEGORY_THREAD_IDS.get(category, 2)  # Standardmäßig Kategorie 2 (Art, Artist Support and Event Management)

    message = f"{job_title}\nEmployer: {employer}\nLink: {job_link}"

    # Sende Nachricht an Telegram
    try:
        await bot.send_message(
            chat_id=CHAT_ID,
            text=message,
            reply_to_message_id=thread_id,
            parse_mode="Markdown"  # Statt ParseMode.MARKDOWN, einfach "Markdown" als String
        )
    except exceptions.TelegramAPIError as e:
        print(f"Fehler beim Senden der Nachricht: {e}")

async def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().splitlines()

    datapoints = []
    datapoint = []

    # Gehe durch jede Zeile und bilde die einzelnen Datapoints
    for line in content:
        if line.strip() == "---":
            if datapoint:  # Falls das Datapoint nicht leer ist
                datapoints.append(datapoint)
                datapoint = []  # Leere das Datapoint für den nächsten Abschnitt
        else:
            datapoint.append(line)

    if datapoint:  # Füge das letzte Datapoint hinzu
        datapoints.append(datapoint)

    # Gehe jedes Datapoint durch und sende die Nachrichten an Telegram
    for datapoint in datapoints:
        category_line = datapoint[0]
        category = category_line.strip("[]")  # Entferne die Klammern
        job_title = ""
        employer = ""
        job_link = ""

        # Verarbeite jede Zeile im Datapoint
        for line in datapoint:
            if line.startswith("Job Title: "):
                job_title = line.replace("Job Title: ", "").strip()
            elif line.startswith("Employer: "):
                employer = line.replace("Employer: ", "").strip()
            elif line.startswith("Link: "):
                job_link = line.replace("Link: ", "").strip()

        # Sende die Nachricht an Telegram
        if job_title and employer and job_link:
            await send_job_to_telegram(category, job_title, employer, job_link)

async def main():
    await process_file("categorized_jobs.txt")

if __name__ == "__main__":
    asyncio.run(main())
