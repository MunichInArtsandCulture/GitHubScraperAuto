from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  # <-- hier nach oben
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

# Webdriver-Setup für Headless Mode
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# Webseite öffnen
url = "https://www.arbeitsagentur.de/jobsuche/suche?berufsfeld=B%C3%BChnen-%20und%20Kost%C3%BCmbildnerei,%20Requisite;Museumstechnik%20und%20-management;Musik-,%20Gesang-,%20Dirigentent%C3%A4tigkeiten;Schauspiel,%20Tanz%20und%20Bewegungskunst;Theater-,%20Film-%20und%20Fernsehproduktion;Veranstaltungs-,%20Kamera-,%20Tontechnik;Veranstaltungsservice%20und%20-management&angebotsart=1&arbeitsort=M%C3%BCnchen"
driver.get(url)

# Wartezeit, damit die Seite vollständig geladen wird
wait = WebDriverWait(driver, 10)

# Warte, bis die Job-Liste geladen ist (ersten Job-Elemente)
try:
    job_entries = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "jb-job-listen-eintrag")))
except Exception as e:
    print(f"Fehler beim Warten auf Job-Einträge: {e}")

# Liste für Jobs
job_links = []

# Job-Links extrahieren
for entry in job_entries:
    try:
        # Extrahieren des Job-Links
        job_link = entry.find_element(By.TAG_NAME, "a").get_attribute("href")
        job_links.append(job_link)
    except Exception as e:
        print(f"Fehler beim Verarbeiten eines Eintrags: {e}")

# WebDriver schließen
driver.quit()

# Teil 2: Funktion, um Job-Details von einem Job-Link zu extrahieren
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
                print("---")
            else:
                print("Kein 'bei' im Titel gefunden!")
        else:
            print("Kein Title-Tag gefunden!")
    else:
        print(f"Fehler beim Abrufen der Seite, Status Code: {response.status_code}")

# Teil 3: Job-Links iterieren und für jeden Link Teil 2 ausführen
for job_link in job_links:
    get_job_details(job_link)
