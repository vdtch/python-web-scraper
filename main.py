import requests
from bs4 import BeautifulSoup

from writer import write_quote_to_csv_file
from scraper import web_page_scraper


# URL of the homepage of the target website
base_url = 'https://quotes.toscrape.com/'

# Define User Agent header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# Connection to the target URL
page = requests.get(base_url, headers=headers)

# Parse the HTML content
soup = BeautifulSoup(page.text, 'html.parser')

# Intialize element to store quotes
quotes = []

# Select HTML elements with Beautiful Soup
## Get all h1 elements in the page
h1_elements = soup.find_all('h1')

## Get the element with id = 'main-title'
main_title_element = soup.find(id='main-title')

# Scraping the homepage of the target website
web_page_scraper(soup, quotes)

# Get the next HTML element
next_li_element = soup.find('li', class_='next')

while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    # getting the new page
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    # parsing the new page
    soup = BeautifulSoup(page.text, 'html.parser')

    # scraping the new page
    web_page_scraper(soup, quotes)

    # looking for the "Next →" HTML element in the new page
    next_li_element = soup.find('li', class_='next')

write_quote_to_csv_file(quotes)