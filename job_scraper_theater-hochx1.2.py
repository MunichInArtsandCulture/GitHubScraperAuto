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
url = "https://theater-hochx.de/jobs/"

# Funktion zum Scrapen der Jobs
def scrape_theater_hochx_jobs(url):
    driver.get(url)
    time.sleep(3)  # Warten, bis die Seite geladen ist

    # HTML-Quelle analysieren
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Alle <h2>-Tags mit der Klasse "has-text-align-center wp-block-heading" finden
    job_titles = soup.find_all("h2", class_="has-text-align-center wp-block-heading")
    jobs = []

    for h2 in job_titles:
        # Das <a>-Tag im <h2> finden
        a_tag = h2.find("a", href=True)

        # Wenn ein <a>-Tag vorhanden ist, den Jobtitel und den Link extrahieren
        if a_tag:
            job_title = a_tag.get_text(strip=True)  # Jobtitel extrahieren und Leerzeichen entfernen
            job_link = a_tag['href']  # Link zum Job

            # Nur hinzufügen, wenn der Titel nicht leer ist
            if job_title and job_link:
                jobs.append({"title": job_title, "link": job_link})

    # Browser schließen
    driver.quit()

    return jobs

# Scraping starten
jobs = scrape_theater_hochx_jobs(url)

# Ergebnisse ausgeben
for job in jobs:
    print(f"Job Title: {job['title']}")
    print("Employer: HochX Theater")
    print(f"Link: {job['link']}")
    print("---")
