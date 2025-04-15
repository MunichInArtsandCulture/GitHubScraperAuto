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

url = "https://www.residenztheater.de/jobs"

def scrape_residenztheater_jobs(url):
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.accordion__title-text-wrapper"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        title_wrappers = soup.find_all('span', class_='accordion__title-text-wrapper')
        subtitles = soup.find_all('span', class_='accordion__subtitle-text')

        jobs = []

        for title_wrapper, subtitle in zip(title_wrappers, subtitles):
            title = title_wrapper.get_text(strip=True)
            subtitle_text = subtitle.get_text(strip=True)
            combined_title = f"{title}"
            jobs.append({'title': combined_title, 'link': url})

        return jobs

    except Exception as e:
        print(f"Error occurred: {e}")
        return []
    finally:
        driver.quit()

jobs = scrape_residenztheater_jobs(url)
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Employer: Residenztheater")
    print(f"Link: {job['link']}")
    print('---')
