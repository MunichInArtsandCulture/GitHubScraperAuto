import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setze den WebDriver (z. B. ChromeDriver)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL der Haus der Kunst Seite
url = "https://www.hausderkunst.de/ueber-uns/stellenangebote-praktika"

# Funktion zum Scrapen der Stellenangebote
def scrape_house_of_art_jobs(url):
    driver.get(url)
    time.sleep(3)  # Warte auf das Laden der Seite (3 Sekunden, je nach Internetgeschwindigkeit anpassen)

    # BeautifulSoup zur Analyse des HTMLs verwenden
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extrahiere alle Jobtitel und Links
    job_titles = soup.find_all('a', href=True, text=True)  # Suche nach allen Links mit Text
    jobs = []

    # Iteriere durch alle gefundenen Links und filtere die relevanten Jobangebote
    for job in job_titles:
        # Überprüfe, ob der Link ein Jobangebot ist (durch das Vorhandensein von "stellenangebote-praktika" im href)
        if "stellenangebote-praktika" in job['href'] and job.get_text(strip=True) != "Stellenangebote & Praktika":
            title = job.get_text(strip=True)  # Jobtitel extrahieren
            link = job['href']  # Joblink extrahieren
            jobs.append({'title': title, 'link': link})

    # Schließe den Browser
    driver.quit()

    # Gib die gefundenen Jobs zurück
    return jobs

# Starte das Scraping für Haus der Kunst
jobs = scrape_house_of_art_jobs(url)

# Zeige die gefundenen Jobs an
for job in jobs:
    print(f"Job Title: {job['title']}")
    print("Employer: Haus der Kunst")
    print(f"Link: {job['link']}")
    print('---')
