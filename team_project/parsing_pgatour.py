"""
This file is intended to be used for parsing out all of the stats on pgatour.com/stats and adding them to pandas dataframes

"""

import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
import re


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


# used to build all of the different URLS for the different tabs
def mainmenu_tab_selector(menu_key_name):
    menu_dict = scrape_table_urls()
    url_endpoint = menu_dict[menu_key_name]
    url = "https://www.pgatour.com{}".format(str(url_endpoint))
    return url


def tab_sub_menu_urls(tab_name, season_year):
    tee_url = mainmenu_tab_selector(tab_name.upper())
    radar_stats = requests.get(str(tee_url))
    soup = BeautifulSoup(radar_stats.text, 'html.parser')
    sub_menus = soup.find_all('div', attrs={'class': 'module-statistics-off-the-tee-table'})
    sub_menu_urls = {}
    for items in sub_menus:
        for a_tags in items.find_all('a', href=True):
            tag = a_tags['href']
            season_adjusted_tag = str(tag).replace('.html','.y{}.html').format(season_year)
            # print(tag)
            sub_menu_urls.update({a_tags.text.upper(): season_adjusted_tag})
    return sub_menu_urls


def parse_menu(endpoint, data_name):
    # need to edit this so that it regexes out the url and adds y2019 before the .html
    url = "https://www.pgatour.com/content/pgatour{}".format(endpoint)
    pga_tour_stats = requests.get(url)
    soup = BeautifulSoup(pga_tour_stats.text, 'html.parser')
    # grabbing the column headers
    raw_header = soup.find('thead')
    # grabbing headers
    columns = [col.get_text().strip('\n\s') for col in raw_header.find_all('th')]

    # parse golfers
    golfers = soup.find('tbody')
    
    holder = []
    for golfer in golfers.find_all('tr'):
        holder.append([stat.get_text().strip('\n\s') for stat in golfer.find_all('td')])
    golfer_df = DataFrame(holder)
    golfer_df.columns = columns
    save_path = '/home/egkennedy93/programming_projects/UFMBA22_Managerial_Statistics/team_project/PGA_stats_{}.csv'.format(data_name)
    golfer_df.to_csv(save_path, index = False, sep=',', encoding='utf-8')
    return golfer_df



if __name__ == '__main__':
    off_the_tee_urls = tab_sub_menu_urls('off the tee', '2020')
    t2g_data = parse_menu(off_the_tee_urls['CLUB HEAD SPEED'], 'club_head_speed')

    print(t2g_data)    
    # print(off_the_tee_urls)
