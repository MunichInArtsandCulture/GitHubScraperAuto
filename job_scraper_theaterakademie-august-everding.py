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
url = "https://www.theaterakademie.de/jobs"

# Funktion zum Scrapen der Jobs
def scrape_theaterakademie_jobs(url):
    driver.get(url)
    time.sleep(3)  # Warten, bis die Seite geladen ist

    # HTML-Quelle analysieren
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Alle h2-Tags mit der entsprechenden Klasse finden
    job_titles = soup.find_all("h2", class_="")
    jobs = []

    for h2 in job_titles:
        title = h2.get_text(strip=True)  # Jobtitel extrahieren und Leerzeichen entfernen

        # Nur hinzufügen, wenn der Titel nicht leer ist
        if title:
            jobs.append({"title": title, "link": url})

    # Browser schließen
    driver.quit()

    return jobs

# Scraping starten
jobs = scrape_theaterakademie_jobs(url)

# Ergebnisse ausgeben
for job in jobs:
    print(f"Job Title: {job['title']}")
    print("Employer: Theaterakademie August Everding")
    print(f"Link: {job['link']}")
    print("---")
