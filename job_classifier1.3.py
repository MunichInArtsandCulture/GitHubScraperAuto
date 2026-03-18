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
                employer = re.search(r"Employer: (.+)", block_text)
                job_link = re.search(r"(Link|Job Link): (.+)", block_text)

                if job_title and employer and job_link:
                    title = job_title.group(1)
                    employer_name = employer.group(1)
                    link = job_link.group(2)

                    category_examples = "\n".join([f"- {cat}: {', '.join(examples)}" for cat, examples in categories_with_examples.items()])

                    try:
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are an expert in job categorization. Your task is to provide only the name of the category for a given job title and employer. No explanations or additional text. Just the category name."},
                                {"role": "user", "content": f"Categorize this job into one of the following categories with examples:\n\n{category_examples}\n\nJob Title: {title}\nEmployer: {employer_name}"}
                            ]
                        )
                        best_category = response.choices[0].message["content"].strip()
                        best_category = best_category.replace('"', '').replace("'", "").strip()

                        formatted_job = f"[{best_category}]\nJob Title: {title}\nEmployer: {employer_name}\nLink: {link}"
                        processed_jobs.append(formatted_job)

                    except Exception as e:
                        print(f"❌ GPT Error for job '{title}': {type(e).__name__}: {e}")

        current_block = []
        inside_block = True
    elif inside_block:
        current_block.append(line)

# Speichern in Datei
print("Processed jobs count:", len(processed_jobs))
with open("categorized_jobs.txt", "w", encoding="utf-8") as output_file:
    output_file.write("\n---\n".join(processed_jobs))

print("✅ Die Jobs wurden erfolgreich mit GPT-3.5 Turbo kategorisiert und in 'categorized_jobs.txt' gespeichert!")
