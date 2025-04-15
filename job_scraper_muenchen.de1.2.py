import requests
from bs4 import BeautifulSoup

# Die URL der Seite, die du scrapen möchtest
url = "https://karriere.muenchen.de/go/Kultur/8927601/"

# Senden einer GET-Anfrage an die Seite
response = requests.get(url)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    # BeautifulSoup für das Parsen der HTML-Daten
    soup = BeautifulSoup(response.text, 'html.parser')

    # Alle Job-Elemente extrahieren
    job_entries = soup.find_all('div', class_='job-tile-cell')

    for entry in job_entries:
        try:
            # Jobtitel und Job-Link extrahieren
            job_title = entry.find('a').text.strip()  # Text innerhalb des <a> Tags
            job_link = entry.find('a')['href']  # Der Job-Link aus dem href-Attribut

            # Arbeitgeber extrahieren (letztes <div> innerhalb des job-tile-cell)
            employer = entry.find_all('div')[-1].text.strip()

            # Ergebnisse ausgeben
            print(f"Job Title: {job_title}")
            print(f"Employer: {employer}")
            print(f"Link: https://karriere.muenchen.de{job_link}\n")
            print("---")

        except Exception as e:
            print(f"Fehler beim Verarbeiten eines Eintrags: {e}")
else:
    print(f"Fehler beim Abrufen der Seite, Status Code: {response.status_code}")
