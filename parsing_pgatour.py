"""
This file is intended to be used for parsing out all of the stats on pgatour.com/stats and adding them to pandas dataframes

"""

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame



def scrape_table_urls():
    # parent data from for the default page
    url = "https://www.pgatour.com/stats.html"
    pga_tour_stats = requests.get(url)
    soup = BeautifulSoup(pga_tour_stats.text, 'html.parser')
    menu_header_options = soup.find('ul', attrs={'role': 'tablist', 'class': 'nav nav-tabs slim nav-tabs-drop'})
    table_urls = {}
    for item in menu_header_options.find_all('a', href=True):
        table_urls.update({item.text : item['href']})
    return table_urls


scrape_table_urls()