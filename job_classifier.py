import re
from transformers import pipeline

# Hugging Face Zero-Shot-Classification-Modell laden
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

processed_jobs = []
current_block = []
inside_block = False

for line in lines:
    line = line.strip()

    if line == "---":
        if current_block:
            block_text = "\n".join(current_block)

            # job_scraper_*.py-Blöcke ignorieren
            if not re.match(r"job_scraper_\w+\.py", block_text):
                job_title = re.search(r"Job Title: (.+)", block_text)
                employer = re.search(r"Employer: (.+)", block_text)
                job_link = re.search(r"(Link|Job Link): (.+)", block_text)

                if job_title and employer and job_link:
                    title = job_title.group(1)
                    employer_name = employer.group(1)
                    link = job_link.group(2)

                    # KI-Klassifizierung
                    category_result = classifier(title, categories)
                    best_category = category_result["labels"][0]

                    formatted_job = f"[{best_category}]\nJob Title: {title}\nEmployer: {employer_name}\nLink: {link}"
                    processed_jobs.append(formatted_job)

        current_block = []
        inside_block = True
    elif inside_block:
        current_block.append(line)

# Ergebnisse speichern
with open("categorized_jobs.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n---\n".join(processed_jobs))
    output_file.write("\n")  # Extra line break for clean end

print(f"✅ {len(processed_jobs)} Jobs wurden erfolgreich kategorisiert und in 'categorized_jobs.txt' gespeichert!")
