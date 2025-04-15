from bs4 import BeautifulSoup
import requests

# URL der Seite mit den Stellenangeboten
url = "https://www.unterfahrt.de/info.php?action=jobs"

# Funktion zum Scrapen der Stellenangebote
def scrape_unterfahrt_jobs(url):
    response = requests.get(url)
    response.raise_for_status()  # Überprüfe, ob die Seite erfolgreich geladen wurde

    # BeautifulSoup zur Analyse des HTMLs verwenden
    soup = BeautifulSoup(response.text, 'html.parser')

    # Finde alle <h4>, denen direkt ein <p> folgt
    jobs = []
    for h4 in soup.find_all('h4'):
        next_element = h4.find_next_sibling()
        if next_element and next_element.name == 'p':
            job_title = h4.get_text(strip=True)
            jobs.append({'title': job_title, 'link': url})

    return jobs

# Starte das Scraping
jobs = scrape_unterfahrt_jobs(url)

# Zeige die gefundenen Jobs an
for job in jobs:
    print(f"Job Title: {job['title']}")
    print("Employer: Jazzclub Unterfahrt")
    print(f"Link: {job['link']}")
    print('---')
