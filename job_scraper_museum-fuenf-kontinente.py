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
url = "https://www.museum-fuenf-kontinente.de/museum/stellenangebote/"

# Function to scrape job listings
def scrape_museum_fuenf_kontinente_jobs(url):
    driver.get(url)

    # Wait for the page to load completely and the job listings to appear
    try:
        # Wait until the job titles are visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.press-item h3"))
        )

        # Use BeautifulSoup to parse the page content
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all job titles and their links inside <li class="press-item">
        job_titles = []
        items = soup.find_all('li', class_='press-item')

        for item in items:
            h3_tag = item.find('h3')  # Find the h3 tag which contains the job title
            a_tag = item.find('a')    # Find the <a> tag which contains the link to the job
            if h3_tag and a_tag:
                title = h3_tag.get_text(strip=True)  # Extract job title
                link = a_tag['href']  # Extract the job link (href attribute)
                job_titles.append({'title': title, 'link': link})

        # Return the found jobs
        return job_titles

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

    finally:
        # Close the browser
        driver.quit()

# Start scraping for Museum Fünf Kontinente job listings
jobs = scrape_museum_fuenf_kontinente_jobs(url)

# Display found jobs
for job in jobs:
    print(f"Job Title: {job['title']}")
    print(f"Employer: Museum Fünf Kontinente")
    print(f"Link: https://www.museum-fuenf-kontinente.de/{job['link']}")
    print('---')
