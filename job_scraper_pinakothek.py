from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# Webdriver-Setup
service = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=service, options=options)

# Ziel-URL
url = "https://www.pinakothek.de/de/museum/team/stellenangebote"

# Funktion zum Scrapen der Jobs
def scrape_pinakothek_jobs(url):
    driver.get(url)
    time.sleep(3)  # Warten, bis die Seite geladen ist

    # HTML-Quelle analysieren
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Alle strong-Tags finden (Jobtitel sind innerhalb von strong)
    job_titles = soup.find_all("strong")
    jobs = []

    for strong in job_titles:
        title = strong.get_text(strip=True)  # Jobtitel extrahieren und Leerzeichen entfernen

        # Nur hinzufügen, wenn der Titel nicht leer ist
        if title:
            jobs.append({"title": title, "link": url})

    # Browser schließen
    driver.quit()

    return jobs

# Scraping starten
jobs = scrape_pinakothek_jobs(url)

# Ergebnisse ausgeben
for job in jobs:
    print(f"Job Title: {job['title']}")
    print("Employer: --not determinable-- ")
    print(f"Link: {job['link']}")
    print("---")
