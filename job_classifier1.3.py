import re
import openai

# OpenAI API-Key
openai.api_key = "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"

# Kategorien mit Beispielen
categories_with_examples = {
    "Art, Artist Support and Event Management": ["Eventmanager:in", "Bühnenbildner:in"],
    "Musicians and Singers": ["Musiker:in", "Sänger:in", "Instrumentalist:in"],
    "Education, Pedagogical and Social": ["Lehrer:in", "Sozialarbeiter:in", "Erzieher:in"],
    "Stage and Event Technology": ["Veranstaltungstechniker:in", "Lichttechniker:in"],
    "Costume, Makeup and Fashion": ["Modedesigner:in", "Maskenbildner:in"],
    "Acting, Theater and Directing": ["Schauspieler:in", "Regisseur:in", "Soufflage"],
    "Legal and Financial": ["Betriebsmanagement", "Steuerberater:in", "Finanzcontroller:in"],
    "Communication, PR and Press": ["PR-Manager:in", "Pressesprecher:in"],
    "IT and Digital": ["Softwareentwickler:in", "IT-Support", "Webdesigner:in"],
    "Customer Service, Catering and Cash Register": ["Einlassdienst", "Kundenbetreuer:in", "Küchenhilfe"],
    "Other": ["Anlagenmechaniker:in", "Facility Manager:in", "Hausmeister:in"]
}

# Datei einlesen
with open("cooljobs.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

processed_jobs = []
current_block = []
inside_block = False

for line in lines:
    line = line.strip()

    if line == "---":
        if current_block:
            block_text = "\n".join(current_block)
            if not re.match(r"job_scraper_\w+\.py", block_text):
                job_title = re.search(r"Job Title: (.+)", block_text)
                employer = re.search(r"Employer: (.+)", block
