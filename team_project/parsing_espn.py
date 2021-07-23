import pandas as pd
import numpy as np
import re
import requests
import os
from bs4 import BeautifulSoup
from pandas import DataFrame


def espn_scrape():
    # parent data from for the default page
    reg_df = pd.DataFrame()
    for i in range(1,193, 40):
        url = "https://www.espn.com/golf/statistics/_/year/2020/count/{}".format(i)
        pga_tour_stats = requests.get(url)
        soup = BeautifulSoup(pga_tour_stats.text, 'html.parser')

        # grabbing the column headers
        raw_header = soup.find('tr', attrs={'class':'colhead'})
        # for each column found, get the text value
        columns = [col.get_text() for col in raw_header.find_all('td')]

        #identifying the player rows
        players = soup.find_all('tr', attrs={'class':re.compile('row player-11')})

        
        for player in players:
            # for each stat value found, grab the text value
            stats = [stat.get_text() for stat in player.find_all('td')]

            # transposing the rows and columns
            player_df = DataFrame(stats).transpose()
            player_df.columns = columns
            # players_with_earnings = player_df.query('EARNINGS != "--"')
            reg_df = pd.concat([reg_df, player_df], ignore_index=True)

    # parent data frame for the Expanded I page
    Expanded_I_df = pd.DataFrame()
    for i in range(1,193, 40):
        url = "https://www.espn.com/golf/statistics/_/year/2020/type/expanded/count/{}".format(i)
        pga_tour_stats = requests.get(url)
        soup = BeautifulSoup(pga_tour_stats.text, 'html.parser')

        # grabbing the column headers
        raw_header = soup.find('tr', attrs={'class':'colhead'})
        columns = [col.get_text() for col in raw_header.find_all('td')]

        #identifying the player rows
        players = soup.find_all('tr', attrs={'class':re.compile('row player-11')})

        
        for player in players:
            stats = [stat.get_text() for stat in player.find_all('td')]

            # transposing the rows and columns
            player_df = DataFrame(stats).transpose()
            player_df.columns = columns
            player_df.drop(columns=['RK', 'AGE'], inplace=True, axis=1)

            # players_with_earnings = player_df.query('EARNINGS != "--"')
            Expanded_I_df = pd.concat([Expanded_I_df, player_df], ignore_index=True)


    # parent data frame for the expanded II page
    Expanded_II_df = pd.DataFrame()
    for i in range(1,193, 40):
        url = "https://www.espn.com/golf/statistics/_/year/2020/type/expanded2/count/{}".format(i)
        pga_tour_stats = requests.get(url)
        soup = BeautifulSoup(pga_tour_stats.text, 'html.parser')

        # grabbing the column headers
        raw_header = soup.find('tr', attrs={'class':'colhead'})
        columns = [col.get_text() for col in raw_header.find_all('td')]

        #identifying the player rows
        players = soup.find_all('tr', attrs={'class':re.compile('row player-11')})

        
        for player in players:
            stats = [stat.get_text() for stat in player.find_all('td')]

            player_df = DataFrame(stats).transpose()
            player_df.columns = columns
            player_df.drop(columns=['RK', 'AGE'], inplace=True, axis=1)

            # players_with_earnings = player_df.query('EARNINGS != "--"')

            Expanded_II_df = pd.concat([Expanded_II_df, player_df], ignore_index=True)       


    merg_reg_expanded = pd.merge(reg_df, Expanded_I_df, on=['PLAYER'])
    merg_extra_expanded2 = pd.merge(merg_reg_expanded, Expanded_II_df, on=['PLAYER'])
    sorted_df = merg_extra_expanded2
    sorted_df['AGE'].replace(['--', '', ' '], np.nan, inplace=True)
    sorted_df.dropna(subset=['AGE'], inplace=True)
    
    #fixing iregularities in the earnings data
    sorted_df['EARNINGS'] = sorted_df['EARNINGS'].str.replace('$','', regex=True)
    sorted_df['EARNINGS'] = sorted_df['EARNINGS'].str.replace(',','', regex=True)
    sorted_df['EARNINGS'] = pd.to_numeric(sorted_df['EARNINGS'])
    sorted_df['RK'] = pd.to_numeric(sorted_df['RK'])

    sorted_df.sort_values('EARNINGS')


    dir_path = os.path.dirname(os.path.realpath(__file__))
    sorted_df.to_csv(dir_path+'/DataSets/ESPN_2020_Stats.csv', index=False, sep=',', encoding='utf-8-sig')
    
    return sorted_df

   
espn_scrape()
