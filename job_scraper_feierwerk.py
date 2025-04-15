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

# URL of the Feierwerk Job Listings page
url = "https://www.feierwerk.de/ueber-uns/jobs"

# Function to scrape job listings
def scrape_feierwerk_jobs(url):
    driver.get(url)

    # Wait for the page to load completely and the job listings to appear
    try:
        # Wait until job listings container is loaded (adjust selector as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href^='/ueber-uns/jobs/']"))
        )

        # Use BeautifulSoup to parse the page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all <a> tags with href starting with '/ueber-uns/jobs/'
        job_links = soup.find_all('a', href=True)
        jobs = []

        # Iterate through found job links and extract relevant data
        for job in job_links:
            if job['href'].startswith('/ueber-uns/jobs/'):
                title = job.get_text(strip=True)  # Extract job title
                link = f"https://www.feierwerk.de{job['href']}"  # Build full job URL
                jobs.append({'title': title, 'link': link})

        # Return the found jobs
        return jobs

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

    finally:
        # Close the browser
        driver.quit()

# Start scraping for Feierwerk job listings
jobs = scrape_feierwerk_jobs(url)

# Display found jobs
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Employer: Feierwerk")
    print(f"Link: {job['link']}")
    print('---')
