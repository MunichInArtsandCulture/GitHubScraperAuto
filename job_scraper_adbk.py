import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Disable Deprecation Warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set WebDriver (Headless Mode for no GUI)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
driver = webdriver.Chrome(options=options)

# URL of the AdBK Job Listings page
url = "https://www.adbk.de/de/aktuell/stellenangebote.html"

# Function to scrape job listings
def scrape_jobs(url):
    driver.get(url)

    # Wait for the page to load completely and the job listings to appear (adjust the wait condition as needed)
    try:
        # Wait until job listings container is loaded (adjust selector based on the actual HTML structure)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".bite-container--entry--anker"))
        )

        # Use BeautifulSoup to parse the page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all job titles and links (target <a> tags with the class 'bite-container--entry--anker')
        job_titles = soup.find_all('a', class_='bite-container--entry--anker')
        jobs = []

        # Iterate through found job links and extract relevant data
        for job in job_titles:
            title = job.get_text(strip=True)  # Extract job title
            link = job['href']  # Extract job link
            jobs.append({'title': title, 'link': link})

        # Return the found jobs
        return jobs

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

    finally:
        # Close the browser
        driver.quit()

# Start scraping for AdBK job listings
jobs = scrape_jobs(url)

# Display found jobs
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Employer: Akademie der Bildenden Künste München")
    print(f"Link: {job['link']}")
    print('---')
