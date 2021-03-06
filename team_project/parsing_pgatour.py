"""
This file is intended to be used for parsing out all of the stats on pgatour.com/stats and adding them to pandas dataframes

"""
import numpy as np
import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from requests.api import put


def scrape_table_urls():
    """
    builds a dictionary for all of the different menu options at pgatour.com/stats.html
    """
    # parent data from for the default page
    url = "https://www.pgatour.com/stats.html"
    pga_tour_stats = requests.get(url)
    # builds a BeautifulSoup Object
    soup = BeautifulSoup(pga_tour_stats.text, 'html.parser')
    #searches for any ul tages with the specified attribtues. This identifies all of the menu_headers
    menu_header_options = soup.find('ul', attrs={'role': 'tablist', 'class': 'nav nav-tabs slim nav-tabs-drop'})
    table_urls = {}
    # looks at each ul item found and takes the href address and adds it to a dictionary. The key is the name of the menu option
    for item in menu_header_options.find_all('a', href=True):
        table_urls.update({item.text : item['href']})
    return table_urls


# used to build all of the different URLS for the different tabs
def mainmenu_tab_selector(menu_key_name):
    """
    menu_key_name: str: name of one of the main menu options. Example: "OFF THE TEE"
    helper function for building the sub urls
    """
    menu_dict = scrape_table_urls()
    url_endpoint = menu_dict[menu_key_name]
    url = "https://www.pgatour.com{}".format(str(url_endpoint))
    return url


def tab_sub_menu_urls(tab_name, season_year):
    """
    tab_name: str: name of the specific menu tab to pull all the various datasets
    season_year: str: needed so the specific year is pulled

    returns a dictionary that has each sub-menus url path
    """
    # takes the tab_name and sets tee-url to the specified url 
    tee_url = mainmenu_tab_selector(tab_name.upper())
    # request to get the specified submenu data
    dataset_stats = requests.get(str(tee_url))
    # BeautifulSoup object instantiation
    soup = BeautifulSoup(dataset_stats.text, 'html.parser')
    # need to look at this, but it will idenfify the block of html that has all of the needed urls for the sub-menus
    sub_menus = soup.find_all('div', attrs={'class': 'module-statistics-off-the-tee-table'})
    sub_menu_urls = {}
    for items in sub_menus:
        # parses through each item found and grabs the url
        for a_tags in items.find_all('a', href=True):
            tag = a_tags['href']
            # adjusting the url to handle the specified season
            season_adjusted_tag = str(tag).replace('.html','.y{}.html').format(season_year)
            # updating the dictionary value with the season adjusted value
            sub_menu_urls.update({a_tags.text.upper(): season_adjusted_tag})
    return sub_menu_urls


def parse_menu(endpoint, data_name):
    # need to edit this so that it regexes out the url and adds y2019 before the .html
    url = "https://www.pgatour.com/content/pgatour{}".format(endpoint)
    pga_tour_stats = requests.get(url)
    soup = BeautifulSoup(pga_tour_stats.text, 'html.parser')
    # grabbing the column headers
    raw_header = soup.find('thead')
    # grabbing column values
    columns = [col.get_text() for col in raw_header.find_all('th')]
    # parse golfers
    golfers = soup.find('tbody')
    
    holder = []
    # parses through each golfer found
    for golfer in golfers.find_all('tr'):
        # for each golfer found 
        holder.append([stat.get_text().strip('\t\n') for stat in golfer.find_all('td')])
    golfer_df = DataFrame(holder)
    golfer_df.columns = columns

    # this is cleaning up a bunch of data points that had the incorrect data format and 
    # had duplicate names to other fields so I overwrite the field name by appending the dataset name to the field
    new_avg = "{}_AVG".format(data_name)
    new_round = "{}_ROUNDS".format(data_name)
    new_fast_speed = "{}_FASTEST SPEED".format(data_name)
    new_slow_speed = "{}_SLOWEST SPEED".format(data_name)
    new_percent = "{}_%".format(data_name)
    new_percent_made = "{}_% MADE".format(data_name)
    new_attempts = "{}_ATTEMPTS".format(data_name)
    new_putts_made = "{}_PUTTS_MADE".format(data_name)
    new_total_attempts = "{}_TOTAL ATTEMPTS".format(data_name)
    
    # applying the renames
    golfer_df.rename(columns={'PLAYER NAME': "PLAYER"}, inplace=True)
    golfer_df.rename(columns={'AVG.': new_avg.upper()}, inplace=True)
    golfer_df.rename(columns={'ROUNDS': new_round.upper()}, inplace=True)
    golfer_df.rename(columns={'FASTEST SPEED': new_fast_speed.upper()}, inplace=True)
    golfer_df.rename(columns={'SLOWEST SPEED': new_slow_speed.upper()}, inplace=True)
    golfer_df.rename(columns={'TOTAL ATTEMPTS_x': new_total_attempts.upper()}, inplace=True)
    golfer_df.rename(columns={'%': new_percent.upper()}, inplace=True)
    golfer_df.rename(columns={'ATTEMPTS': new_attempts.upper()}, inplace=True)
    golfer_df.rename(columns={'PUTTS MADE': new_putts_made.upper()}, inplace=True)
    golfer_df.rename(columns={'% MADE': new_percent_made.upper()}, inplace=True)
    golfer_df.rename(columns={'TOTAL ATTEMPTS': new_total_attempts.upper()}, inplace=True)

    # certain fields weren't necessary
    del golfer_df['\n                                RANK LAST WEEK']
    del golfer_df['RANK\xa0THIS WEEK']
    
    #saving the final fomrat to a CSV file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    save_path = dir_path+'/DataSets/PGA_stats_{}.csv'.format(data_name)
    golfer_df.to_csv(save_path, index = False, sep=',', encoding='utf-8-sig')
    return golfer_df


# #selecting which menu to use
off_the_tee_urls = tab_sub_menu_urls('off the tee', '2020')
putting_urls = tab_sub_menu_urls('putting', '2020')


# this is parsing the menus
longest_drive = parse_menu(off_the_tee_urls['LONGEST DRIVES'], 'longest_drives')
Driving_distance = parse_menu(off_the_tee_urls['DRIVING DISTANCE'], 'driving_distance')


# RADAR Data
chs_data = parse_menu(off_the_tee_urls['CLUB HEAD SPEED'], 'club_head_speed')
ball_speed = parse_menu(off_the_tee_urls['BALL SPEED'], 'ball_speed')
smash_factor = parse_menu(off_the_tee_urls['SMASH FACTOR'], 'smash_factor')
launch_angle = parse_menu(off_the_tee_urls['LAUNCH ANGLE'], 'launch_angle')
spin_rate = parse_menu(off_the_tee_urls['SPIN RATE'], 'spin_rate')
distance_to_apex = parse_menu(off_the_tee_urls['DISTANCE TO APEX'], 'distance_to_apex')
apex_height = parse_menu(off_the_tee_urls['APEX HEIGHT'], 'apex_height')
hang_time = parse_menu(off_the_tee_urls['HANG TIME'], 'hang_time')
carry_distance = parse_menu(off_the_tee_urls['CARRY DISTANCE'], 'carry_distance')
carry_efficiency = parse_menu(off_the_tee_urls['CARRY EFFICIENCY'], 'carry_efficiency')

#PUTTING Data
inside_5 = parse_menu(putting_urls['PUTTING FROM INSIDE 5\''], 'PUTTING FROM INSIDE INSIDE 5\'')
inside_5_10 = parse_menu(putting_urls['PUTTING FROM 5-10\''], 'PUTTING FROM 5-10\'')
inside_10_15 = parse_menu(putting_urls['PUTTING FROM - 10-15\''], 'PUTTING FROM - 10-15\'')
inside_15_20 = parse_menu(putting_urls['PUTTING FROM - 15-20\''], 'PUTTING FROM - 15-20\'')
inside_20_25 = parse_menu(putting_urls['PUTTING FROM - 20-25\''], 'PUTTING FROM - 20-25\'')
