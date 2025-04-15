from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Setze den WebDriver (z. B. ChromeDriver)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL der Kunsthalle München Stellenangebote-Seite
url = "https://www.kunsthalle-muc.de/stellenangebote/"

# Funktion zum Scrapen der Stellenangebote
def scrape_kunsthalle_jobs(url):
    driver.get(url)
    time.sleep(3)  # Warte auf das Laden der Seite (3 Sekunden, je nach Internetgeschwindigkeit anpassen)

    # BeautifulSoup zur Analyse des HTMLs verwenden
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extrahiere alle relevanten div-Tags mit der Klasse "is-anchor"
    job_divs = soup.find_all('div', class_='is-anchor')
    jobs = []

    for div in job_divs:
        # Entferne alle <p> und <h6>-Elemente innerhalb des div
        for tag in div.find_all(['p', 'h6']):
            tag.decompose()  # Entferne die Elemente aus dem DOM-Baum

        # Extrahiere den reinen Textinhalt des div (ohne <p> und <h6>)
        title = div.get_text(strip=True)
        link = url  # Setze die Website als Quelllink
        jobs.append({'title': title, 'link': link})

    # Schließe den Browser
    driver.quit()

    # Gib die gefundenen Jobs zurück
    return jobs

# Starte das Scraping für Kunsthalle München
jobs = scrape_kunsthalle_jobs(url)

# Zeige die gefundenen Jobs an
for job in jobs:
    print(f"Job Title: {job['title']}")
    print("Employer: Kunsthalle München")
    print(f"Link: {job['link']}")
    print('---')
