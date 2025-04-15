from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Webdriver-Setup
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Ziel-URL
url = "https://www.gaertnerplatztheater.de/de/seiten/jobs.html"

# Funktion zum Scrapen der Jobs
def scrape_gaertnerplatztheater_jobs(url):
    driver.get(url)
    time.sleep(3)  # Warten, bis die Seite geladen ist

    # HTML-Quelle analysieren
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Alle h3-Elemente suchen
    job_titles = soup.find_all("h3")
    jobs = []

    # Ausschlusskriterien für Titel
    exclude_titles = ["Kontakt", "Links", "Stay in touch", "Newsletter"]

    for h3 in job_titles:
        title = h3.get_text(strip=True)  # Jobtitel extrahieren und Leerzeichen entfernen

        # Nur hinzufügen, wenn der Titel nicht leer ist und nicht auf der Ausschlussliste steht
        if title and title not in exclude_titles:
            link = url  # Der Link zur Website bleibt derselbe
            jobs.append({"title": title, "link": link})

    # Browser schließen
    driver.quit()

    return jobs

# Scraping starten
jobs = scrape_gaertnerplatztheater_jobs(url)

# Ergebnisse ausgeben
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Employer: Gärtnerplatztheater")
    print(f"Link: {job['link']}")
    print("---")
