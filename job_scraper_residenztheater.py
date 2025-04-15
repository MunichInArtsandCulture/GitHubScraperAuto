import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Disable Deprecation Warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set WebDriver (Headless Mode for no GUI)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no browser window)
options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
driver = webdriver.Chrome(options=options)

# URL of the website
url = "https://www.residenztheater.de/jobs"

# Function to scrape job listings
def scrape_residenztheater_jobs(url):
    driver.get(url)

    # Wait for the page to load completely and the job listings to appear
    try:
        # Wait until the job titles are visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.accordion__title-text"))
        )

        # Use BeautifulSoup to parse the page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all <span> tags with the job title class
        job_titles = soup.find_all('span', class_='accordion__title-text')
        jobs = []

        # Iterate through found job titles and extract relevant data
        for job in job_titles:
            title = job.get_text(strip=True)  # Extract job title
            jobs.append({'title': title, 'link': url})

        # Return the found jobs
        return jobs

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

    finally:
        # Close the browser
        driver.quit()

# Start scraping for Residenztheater job listings
jobs = scrape_residenztheater_jobs(url)

# Display found jobs
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Employer: Residenztheater")
    print(f"Link: {job['link']}")
    print('---')
