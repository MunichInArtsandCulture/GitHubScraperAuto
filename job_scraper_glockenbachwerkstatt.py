from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

# Ziel-URL
url = "https://www.glockenbachwerkstatt.de/ueber-uns/jobs/"

# Funktion zum Scrapen der Stellenanzeigen
def scrape_jobs(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Alle relevanten <div>-Tags finden
    job_divs = soup.find_all("div", class_="wp-block-column is-layout-flow wp-block-column-is-layout-flow")
    jobs = []

    for div in job_divs:
        # Innerhalb des <div> nach einem <h2> mit Klasse "wp-block-heading" suchen
        h2_tag = div.find("h2", class_="wp-block-heading")
        if h2_tag:
            job_title = h2_tag.get_text(strip=True)  # Jobtitel aus dem <h2> extrahieren
            # Den Link aus einem <a>-Tag innerhalb des <div> suchen
            a_tag = div.find("a", href=True)
            job_link = a_tag['href'] if a_tag else url  # Fallback: URL der Seite selbst

            # Wenn der Link relativ ist, den absoluten Link bilden
            job_link = urljoin(url, job_link)

            # Nur hinzufügen, wenn ein Jobtitel vorhanden ist
            if job_title:
                jobs.append({"title": job_title, "link": job_link})

    return jobs

# Scraping starten
jobs = scrape_jobs(url)

# Ergebnisse ausgeben
if jobs:
    for job in jobs:
        print(f"Job Title: {job['title']}")
        print("Employer: Glockenbachwerkstatt")
        print(f"Link: {job['link']}")
        print("---")
