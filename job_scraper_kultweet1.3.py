from bs4 import BeautifulSoup
import requests

# URL der Seite mit den Stellenangeboten
url = "https://www.kultweet.de/jobs.php?af_id=3&Arbeitsfeld=Kunst+%7C+Kultur+%7C+Musik"

# Funktion zum Scrapen der Stellenangebote
def scrape_kultweet_jobs(url):
    response = requests.get(url)
    response.raise_for_status()  # Überprüfe, ob die Seite erfolgreich geladen wurde

    # BeautifulSoup zur Analyse des HTMLs verwenden
    soup = BeautifulSoup(response.text, 'html.parser')

    # Klassen der <li>-Elemente, die Job-Einträge darstellen
    li_classes = ["box premium-jobs", "box row_1", "box row_2"]
    valid_locations = ["München", "Munich", "Muenchen", "Munchen"]

    jobs = []

    # Durchsuche die entsprechenden <li>-Elemente
    for li in soup.find_all('li', class_=li_classes):
        # Extrahiere das <a>-Tag und seinen href-Link
        a_tag = li.find('a', href=True)
        if not a_tag:
            continue

        link = a_tag['href']  # Link zum Job
        job_title_div = a_tag.find('div', class_='jobtitle')  # Jobtitel
        location_div = a_tag.find('div', class_='ort')  # Arbeitsort
        employer_div = li.find('div', class_='firma')  # Arbeitgeber

        # Überprüfe, ob Jobtitel und Ort vorhanden sind
        if job_title_div and location_div and employer_div:
            job_title = job_title_div.get_text(strip=True)
            location = location_div.get_text(strip=True)

            # Filtere nach validen Orten
            if any(valid_location in location for valid_location in valid_locations):
                # Entferne das Wort "Arbeitgeber:" und unnötige Tags wie <span class="neu"> und <span class="premium">
                employer_text = employer_div.get_text(strip=True)
                employer_text = employer_text.replace('Arbeitgeber:', '').strip()

                # Füge den Job mit Arbeitgeber hinzu
                jobs.append({
                    'title': job_title,
                    'link': link,  # Keine doppelte Basis-URL
                    'employer': employer_text
                })

    return jobs

# Starte das Scraping
jobs = scrape_kultweet_jobs(url)

# Zeige die gefundenen Jobs an
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Employer: {job['employer']}")
    print(f"Link: {job['link']}")
    print('---')
