import re
import openai

# OpenAI API-Schlüssel einbinden
openai.api_key = "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"  # <-- Hier deinen API-Key einfügen

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

processed_jobs = []
current_block = []
inside_block = False

for line in lines:
    line = line.strip()

    if line == "---":
        if current_block:
            block_text = "\n".join(current_block)
            if not re.match(r"job_scraper_\\w+\\.py", block_text):
                job_title = re.search(r"Job Title: (.+)", block_text)
                employer = re.search(r"Employer: (.+)", block_text)
                job_link = re.search(r"(Link|Job Link): (.+)", block_text)

                if job_title and employer and job_link:
                    title = job_title.group(1)
                    employer_name = employer.group(1)
                    link = job_link.group(2)

                    # API-Anfrage an GPT-3.5 Turbo
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are an expert in job categorization. Your task is to provide only the name of the category for a given job title and employer. No explanations or additional text. Just the category name."},
                            {"role": "user", "content": f"Categorize this job into one of the following categories: {categories}.\nJob Title: {title}\nEmployer: {employer_name}"}
                        ]
                    )

                    # Nur den Kategorientext extrahieren und sicherstellen, dass keine Anführungszeichen oder Erklärungen dabei sind
                    best_category = response.choices[0].message["content"].strip()
                    # In diesem Fall entfernen wir auch alle unnötigen Zeichen wie z.B. Anführungszeichen
                    best_category = best_category.replace('"', '').replace("'", "").strip()

                    # Das formatierte Job-Listing speichern
                    formatted_job = f"[{best_category}]\nJob Title: {title}\nEmployer: {employer_name}\nLink: {link}\n"
                    processed_jobs.append(formatted_job)

        current_block = []
        inside_block = True
    elif inside_block:
        current_block.append(line)

# Ergebnis in eine neue Datei schreiben
with open("categorized_jobs.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n---\n".join(processed_jobs))

print("Die Jobs wurden erfolgreich mit GPT-3.5 Turbo kategorisiert und gespeichert!")
