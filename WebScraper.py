'''
Web Scraper:
    This file scrapes data from a website.
'''

import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import re

def scraper(webpage):
    data = requests.get(webpage)
    soup = BeautifulSoup(data.content, 'html.parser')    

    only_data = soup.find_all(class_='article-container')

    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext
    soup = cleanhtml(str(only_data))
    
    return soup