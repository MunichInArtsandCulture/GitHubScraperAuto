import requests
from bs4 import BeautifulSoup

# Funktion zum Abrufen der Jobdetails von einem Job-Link
def get_job_details(job_link):
    # Senden einer GET-Anfrage an die Seite
    response = requests.get(job_link)

    # Überprüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        # BeautifulSoup für das Parsen der HTML-Daten
        soup = BeautifulSoup(response.text, 'html.parser')

        # Den Inhalt des <title>-Tags extrahieren
        title_tag = soup.find('title')

        if title_tag:
            # Den Text des Title-Tags extrahieren
            title_text = title_tag.get_text()

            # Suche nach dem Wort "bei" und teile den Text
            if " bei " in title_text:
                job_title, employer = title_text.split(" bei ", 1)  # Teilung des Texts bei "bei"

                # Ausgabe der Jobdetails
                print(f"Job Title: {job_title}")
                print(f"Employer: {employer}")
                print(f"Link: {job_link}")
            else:
                print("Kein 'bei' im Titel gefunden!")
        else:
            print("Kein Title-Tag gefunden!")
    else:
        print(f"Fehler beim Abrufen der Seite, Status Code: {response.status_code}")
