from bs4 import BeautifulSoup
import requests

# Ziel-URL
url = "https://www.tollwood.de/stellenangebote/#v"

# Funktion zum Scrapen der Stellenanzeigen
def scrape_jobs(url):
    response = requests.get(url)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Alle relevanten <h1> mit <strong> finden
    job_titles = soup.find_all("h1")
    jobs = []

    for h1 in job_titles:
        strong_tag = h1.find("strong")
        if strong_tag and strong_tag.get_text(strip=True):  # Nur hinzufügen, wenn der <strong>-Text vorhanden ist
            job_title = strong_tag.get_text(strip=True)
            # Der Link zum Job (die Seite selbst als Link verwenden)
            job_link = url
            jobs.append({"title": job_title, "link": job_link})

    return jobs

# Scraping starten
jobs = scrape_jobs(url)

# Ergebnisse ausgeben (falls vorhanden)
for job in jobs:
    print(f"Job Title: {job['title']}")
    print("Employer: Tollwood")
    print(f"Link: {job['link']}")
    print("---")
