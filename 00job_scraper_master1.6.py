import os
import runpy
import openai
import json

# Set up OpenAI API key (replace with your actual API key)
openai.api_key = 'blub blub'

# Name save location of JSON-file
print("Die JSON-Datei wurde hier gespeichert: ", 'jobs_data.json')

# Directory containing the scrapers (current directory)
scrapers_dir = os.getcwd()

# List of scraper filenames
scraper_files = [
    "job_scraper_adbk.py",
    "job_scraper_bahnwaerterthiel.py",
    "job_scraper_bergson.py",
    "job_scraper_buehnenjobs1.2.py",
    "job_scraper_feierwerk.py",
    "job_scraper_gaertnerplatztheater1.2.py",
    "job_scraper_glockenbachwerkstatt.py",
    "job_scraper_HDK1.6.py",
    "job_scraper_kultweet1.3.py",
    "job_scraper_kunsthalle-muc.py",
    "job_scraper_museum-brandhorst.py",
    "job_scraper_museum-fuenf-kontinente.py",
    "job_scraper_pasinger-fabrik1.2.py",
    "job_scraper_philharmoniker.py",
    "job_scraper_pinakothek.py",
    "job_scraper_residenztheater.py",
    "job_scraper_staatsoper_buehne.py",
    "job_scraper_staatsoper_buero.py",
    "job_scraper_staatsoper_praktika-ausbildung.py",
    "job_scraper_theaterakademie-august-everding.py",
    "job_scraper_theater-hochx1.2.py",
    "job_scraper_tollwood_jobs.py",
    "job_scraper_tollwood_praktikum.py",
    "job_scraper_unterfahrts.py",
    "job_scraper_wow.py",
    "job_scraper_arbeitsagentur_teil3.py",
    "job_scraper_muenchen.de1.2.py",
]

# Placeholder for collected job data
collected_jobs = []

# Function to remove unwanted text from job titles or descriptions
def clean_job_data(job_title, job_description):
    unwanted_strings = [
        "No jobs found.",
        "DevTools listening",
        "Executing"
    ]

    # Remove unwanted strings from the title and description
    for unwanted in unwanted_strings:
        job_title = job_title.replace(unwanted, "").strip()
        job_description = job_description.replace(unwanted, "").strip()

    return job_title, job_description

# Function to execute each script dynamically
def execute_scripts():
    for script in scraper_files:
        script_path = os.path.join(scrapers_dir, script)
        if os.path.exists(script_path):
            try:
                print(f"Executing {script}...")
                runpy.run_path(script_path)  # Execute the script
                # Assume each script appends jobs to collected_jobs
            except Exception as e:
                print(f"Error executing {script}: {e}")
        else:
            print(f"Script {script} not found!")

# Function to categorize jobs with GPT
def categorize_jobs_with_gpt(jobs):
    prompt = "Here is a list of job titles and their descriptions. Please categorize these jobs into relevant groups like 'Customer Service', 'Stage Jobs', 'Music Jobs', etc. Provide a list of categories and the jobs within each category.\n\n"

    # Adding job data to the prompt
    for job in jobs:
        # Clean up the job title and description before adding them to the prompt
        job_title, job_description = clean_job_data(job['title'], job['description'])

        # Add the cleaned job data to the prompt
        prompt += f"Job Title: {job_title}\nDescription: {job_description}\n\n"

    try:
        # Send the request to the OpenAI API for categorization
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use the appropriate model
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Extract the result from the response
        categories = response.choices[0].text.strip()
        print("Categorized Jobs:")
        print(categories)

        return categories

    except Exception as e:
        print(f"Error with GPT categorization: {e}")
        return None

# Main function to run the scraping and categorization
def main():
    # Step 1: Execute all scrapers and collect the jobs
    execute_scripts()

    # Step 2: Send the job data to GPT for categorization (if collected_jobs is populated)
    if collected_jobs:
        categorized_data = categorize_jobs_with_gpt(collected_jobs)

        # Step 3: Optionally, store or process the categorized data further
        # For now, you can print it or save it to a file
        if categorized_data:
            with open('categorized_jobs.json', 'w') as f:
                json.dump(categorized_data, f, indent=4)
    else:
        print("No jobs found.")

if __name__ == "__main__":
    main()
