from bs4 import BeautifulSoup
import requests

# Ziel-URL
url = "https://www.bahnwaerterthiel.de/jobs/"

# Funktion zum Scrapen der Stellenanzeigen
def scrape_jobs(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Fehler beim Abrufen der Seite: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Das <fieldset> mit dem legend-Tag "Checkboxen" finden
    fieldsets = soup.find_all("fieldset")
    jobs = []

    for fieldset in fieldsets:
        legend_tag = fieldset.find("legend", class_="wpforms-field-label")
        if legend_tag and "Checkboxen" in legend_tag.get_text(strip=True):
            # Alle <li>-Elemente innerhalb des fieldset durchsuchen
            list_items = fieldset.find_all("li")
            for li in list_items:
                job_title = li.get_text(strip=True)
                if job_title:
                    jobs.append({"title": job_title, "link": url})  # Der Link bleibt die Seite selbst

    return jobs

# Scraping starten
jobs = scrape_jobs(url)

# Ergebnisse ausgeben
if jobs:
    for job in jobs:
        print(f"Job Title: {job['title']}")
        print(f"Employer: Bahnwärter Thiel")
        print(f"Link: {job['link']}")
        print("---")
