import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", category=DeprecationWarning)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

url = "https://www.blitz.club/jobs/"

def scrape_blitzclub_jobs(url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "summary"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        job_titles = soup.find_all('summary')
        jobs = []

        for job in job_titles:
            title = job.get_text(strip=True)
            jobs.append({'title': title, 'link': url})

        return jobs

    except Exception as e:
        print(f"Error occurred: {e}")
        return []
    finally:
        driver.quit()

jobs = scrape_blitzclub_jobs(url)
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Employer: BLITZ Club")
    print(f"Link: {job['link']}")
    print('---')
