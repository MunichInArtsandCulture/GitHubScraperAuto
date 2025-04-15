from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # ⬅️ Das hier auch!
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Webdriver-Setup
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)  # ⬅️ HIER options übergeben

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

for entry in job_entries:
    try:
        # Extrahieren des Job-Links
        job_link = entry.find_element(By.TAG_NAME, "a").get_attribute("href")
        job_links.append(job_link)
    except Exception as e:
        print(f"Fehler beim Verarbeiten eines Eintrags: {e}")

# WebDriver schließen
driver.quit()

# Liste der Job-Links zurückgeben
print(f"Gefundene Job-Links: {len(job_links)}")
return job_links  # Diese Rückgabe sorgt dafür, dass der Code die Job-Links zurückgibt
