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
url = "https://www.museum-brandhorst.de/stellenangebote/"

# Function to scrape job listings
def scrape_museum_brandhorst_jobs(url):
    driver.get(url)

    # Wait for the page to load completely and the job listings to appear
    try:
        # Wait until the job titles are visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.text-inner p strong"))
        )

        # Use BeautifulSoup to parse the page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all divs with class 'text-inner', then select the first <strong> tag in each <p>
        job_titles = []
        divs = soup.find_all('div', class_='text-inner')

        for div in divs:
            # Find the first <strong> in a <p> within this div
            strong_tag = div.find('p').find('strong')  # Get the first strong inside the first p
            if strong_tag:
                title = strong_tag.get_text(strip=True)  # Extract job title
                job_titles.append({'title': title, 'link': url})

        # Return the found jobs
        return job_titles

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

    finally:
        # Close the browser
        driver.quit()

# Start scraping for Museum Brandhorst job listings
jobs = scrape_museum_brandhorst_jobs(url)

# Display found jobs
for job in jobs:
    print(f"Job Title: {job['title']}")
    print("Employer: Museum Brandhorst")
    print(f"Link: {job['link']}")
    print('---')
