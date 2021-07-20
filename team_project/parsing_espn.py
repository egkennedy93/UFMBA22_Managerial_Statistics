import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame


def espn_scrape():
    # parent data from for the default page
    reg_df = pd.DataFrame()
    for i in range(1,882, 40):
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
    merg_extra_expanded2 = pd.merge(Expanded_II_df, merg_reg_expanded, on=['PLAYER'])



    merg_extra_expanded2.to_csv(r'/home/egkennedy93/programming_projects/UFMBA22_Managerial_Statistics/team_project/DataSets/PGA_2020_Stats.csv', index = False, sep=',', encoding='utf-8')
    
    return merg_extra_expanded2

   
espn_scrape()
