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


menu_dict = scrape_table_urls()

# used to build all of the different URLS for the different tabs
def tab_selector(menu_key_name):
    url_endpoint = menu_dict[menu_key_name]
    url = "https://www.pgatour.com{}".format(str(url_endpoint))
    return url


def tab_sub_menu_urls(tab_name):
    tee_url = tab_selector(tab_name.upper())
    radar_stats = requests.get(str(tee_url))
    soup = BeautifulSoup(radar_stats.text, 'html.parser')
    sub_menus = soup.find_all('div', attrs={'class': 'module-statistics-off-the-tee-table'})
    sub_menu_urls = {}
    for items in sub_menus:
        for a_tags in items.find_all('a', href=True):
            sub_menu_urls.update({a_tags.text: a_tags['href']})
    return sub_menu_urls

    #return sub_menus

print(tab_sub_menu_urls('off the tee'))
