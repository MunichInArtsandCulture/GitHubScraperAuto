from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL der Bühnenjobs-Seite
url = "https://buehnenjobs.de/intern/jobs/?jobs_start=0&region=1&showall=1&cat="

# Liste der erlaubten Institutionen
allowed_institutions = [
    "Bayerische Staatsoper",
    "Bayerisches Staatsschauspiel",
    "Residenztheater",
    "Münchner Kammerspiele",
    "Staatstheater am Gärtnerplatz",
    "theaterakademie august everding",
    "Münchner Volkstheater",
]

# Funktion zum Scrapen der Stellenangebote
def scrape_buehnenjobs(url):
    driver.get(url)
    time.sleep(3)  # Warte auf das Laden der Seite (3 Sekunden, je nach Geschwindigkeit)

    # BeautifulSoup zur Analyse des HTMLs verwenden
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Finde alle Zeilen in der Jobtabelle
    rows = soup.find_all('tr')  # Jede Tabellenzeile wird geprüft
    jobs = []

    for row in rows:
        # Finde die Institution in der aktuellen Zeile
        institution_cell = row.find('td', {'data-title': 'Institution'})
        if institution_cell and institution_cell.get_text(strip=True) in allowed_institutions:
            # Finde den Jobtitel und den Link
            job_link = row.find('a', class_='iframe')
            if job_link:
                title = job_link.get_text(strip=True)
                href = "https://buehnenjobs.de" + job_link['href']
                institution = institution_cell.get_text(strip=True)  # Extrahiere die Institution

                # Füge die Institution zusammen mit den anderen Job-Daten hinzu
                jobs.append({'title': title, 'link': href, 'institution': institution})

    # Schließe den Browser
    driver.quit()

    # Gib die gefundenen Jobs zurück
    return jobs

# Starte das Scraping für Bühnenjobs
jobs = scrape_buehnenjobs(url)

# Zeige die gefundenen Jobs an
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Institution: {job['institution']}")
    print(f"Link: {job['link']}")
    print('---')
