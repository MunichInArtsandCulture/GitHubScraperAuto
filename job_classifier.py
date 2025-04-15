import re
from transformers import pipeline

# Hugging Face Zero-Shot-Classification-Modell laden (kostenlos)
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Kategorien
categories = [
    "Art, Artist Support and Event Management",
    "Musicians and Singers",
    "Education, Pedagogical and Social",
    "Stage and Event Technology",
    "Costume, Makeup and Fashion",
    "Acting, Theater and Directing",
    "Legal and Financial",
    "Communication, PR and Press",
    "IT and Digital",
    "Customer Service, Catering and Cash Register",
    "Other"
]

# Datei einlesen
with open("cooljobs.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

# Job-Daten verarbeiten
processed_jobs = []
current_block = []
inside_block = False

for line in lines:
    line = line.strip()

    if line == "---":  # Block-Trennung
        if current_block:  # Wenn Block nicht leer, dann verarbeiten
            block_text = "\n".join(current_block)

            # Prüfen, ob der Block ein "job_scraper_*.py" ist -> Ignorieren
            if not re.match(r"job_scraper_\w+\.py", block_text):
                # Job-Daten extrahieren
                job_title = re.search(r"Job Title: (.+)", block_text)
                employer = re.search(r"Employer: (.+)", block_text)
                job_link = re.search(r"(Link|Job Link): (.+)", block_text)

                if job_title and employer and job_link:
                    title = job_title.group(1)
                    employer_name = employer.group(1)
                    link = job_link.group(2)

                    # Kategorie mit KI bestimmen
                    category_result = classifier(title, categories)
                    best_category = category_result["labels"][0]

                    # Neue formatierte Zeile erstellen
                    formatted_job = f"[{best_category}]\nJob Title: {title}\nEmployer: {employer_name}\nLink: {link}\n"
                    processed_jobs.append(formatted_job)

        # Block-Reset
        current_block = []
        inside_block = True
    elif inside_block:
        current_block.append(line)

# Ergebnisse speichern
with open("categorized_jobs.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n---\n".join(processed_jobs))

print("Die Jobs wurden erfolgreich kategorisiert und in 'categorized_jobs.txt' gespeichert!")
