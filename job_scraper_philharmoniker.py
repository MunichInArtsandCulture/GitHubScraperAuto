import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Warnungen unterdrücken
warnings.filterwarnings("ignore", category=DeprecationWarning)

# WebDriver konfigurieren (Headless-Modus für Effizienz)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL der Website
url = "https://www.mphil.de/ueber-uns/offene-stellen"

# Funktion zum Scrapen der Stellenangebote
def scrape_mphil_jobs(url):
    driver.get(url)

    try:
        # Warte, bis mindestens ein Jobtitel geladen ist
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.u-text-uppercase"))
        )

        # HTML mit BeautifulSoup analysieren
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Alle Jobtitel in <span class="u-text-uppercase"> finden
        job_titles = soup.find_all('span', class_='u-text-uppercase')

        jobs = [{'title': job.get_text(strip=True), 'employer': 'Münchner Philharmoniker', 'link': url} for job in job_titles]

        return jobs

    except Exception as e:
        print(f"Fehler: {e}")
        return []

    finally:
        driver.quit()

# Scraper starten
jobs = scrape_mphil_jobs(url)

# Ergebnisse ausgeben
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Employer: {job['employer']}")
    print(f"Link: {job['link']}")
    print('---')
