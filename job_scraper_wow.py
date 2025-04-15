from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Webdriver-Setup
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Ziel-URL
url = "https://www.wow-museum.de/jobs"

# Funktion zum Scrapen der Jobs
def scrape_wow_museum_jobs(url):
    driver.get(url)
    time.sleep(3)  # Warten, bis die Seite geladen ist

    # HTML-Quelle analysieren
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Jobliste-Div (div(1)) finden
    job_list_wrapper = soup.find("div", class_="stellenangebote_job-list-wrapper w-dyn-list")
    jobs = []

    if job_list_wrapper:
        # Alle Job-Einträge durchsuchen
        job_entries = job_list_wrapper.find_all("a", class_="stellenangebote_job-item-link align-center text-align-center w-inline-block")

        for entry in job_entries:
            # Stellenbezeichnung finden
            job_title_div = entry.find("div", class_="stellenangebote_job-name text-align-center align-center")
            if job_title_div:
                title = job_title_div.get_text(strip=True)
                link = entry["href"]  # Relativer Link
                full_link = f"https://www.wow-museum.ch{link}"  # Absoluter Link
                jobs.append({"title": title, "link": full_link})

    # Browser schließen
    driver.quit()

    return jobs

# Scraping starten
jobs = scrape_wow_museum_jobs(url)

# Ergebnisse ausgeben
for job in jobs:
    print(f"Job Title: {job['title']}")
    print("Employer: WOW Museum")
    print(f"Link: {job['link']}")
    print("---")
