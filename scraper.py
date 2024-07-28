import csv
import requests
from bs4 import BeautifulSoup


def write_quote_to_csv_file(quotes: dict):
    # Read csv file and create if not exist
    csv_file = open('quotes.csv', 'w', encoding='utf-8', newline='')

    # Initialize writer object
    writer = csv.writer(csv_file)

    # Write the header of the file
    writer.writerow(['Text', 'Author', 'Tags'])

    # Write quotes in csv file
    for quote in quotes:
        writer.writerow(quote.values())
    
    csv_file.close()


def web_page_scraper(soup: BeautifulSoup, quotes: list):
    # retrieving all the quote <div> HTML element on the page
    quote_elements = soup.find_all('div', class_='quote')

    # iterating over the list of quote elements to extract the data of interest and store it
    # in quotes
    for quote_element in quote_elements:
        # extract the text of the quote
        text = quote_element.find('span', class_='text').text
        # extract the author of the quote
        author = quote_element.find('small', class_='author').text
        # extracting the tag <a> HTML elements related to the quote
        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')

        # storing the list of tag strings in a list
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)
        
        # appending a dictionary containing the quote data in a new format in the quote list
        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ','.join(tags)
            }
        )

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

