import requests
from bs4 import BeautifulSoup

# Die URL, die wir scrapen möchten
url = "https://bergson.com/jobs"

# HTTP-Request an die URL senden
response = requests.get(url)

# Prüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    # BeautifulSoup-Objekt erstellen
    soup = BeautifulSoup(response.text, 'html.parser')

    # Alle Stellenangebote auf der Seite finden
    job_listings = soup.find_all('a', class_='job')

    # Jede Jobbeschreibung extrahieren und im Terminal ausgeben
    for job in job_listings:
        job_title = job.find('div', class_='job-title').text.strip()  # Jobtitel extrahieren
        job_link = "https://bergson.com" + job['href'].strip()  # Job-Link (vollständig) extrahieren

        # Daten im Terminal ausgeben
        print(f"Job Title: {job_title}")
        print(f"Employer: Bergson")
        print(f"Link: {job_link}")
        print("---")

else:
    print(f"Error: {response.status_code}")
