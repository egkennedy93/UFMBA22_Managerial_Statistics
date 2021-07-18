import parsing_espn
import parsing_pgatour
import pandas as pd
from pandas import DataFrame

espn_data = parsing_espn.espn_scrape()
pga_data = parsing_pgatour.ball_speed


merg_espn_test = pd.merge(espn_data, pga_data, on=['PLAYER'])
merg_espn_test.to_csv(r'/home/egkennedy93/programming_projects/UFMBA22_Managerial_Statistics/team_project/DataSets/PGA_test.csv', index = False, sep=',', encoding='utf-8')

# print(merg_espn_test)
