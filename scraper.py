import csv
import requests
from bs4 import BeautifulSoup


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
