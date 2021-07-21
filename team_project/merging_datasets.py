import parsing_espn
import parsing_pgatour
import pandas as pd
from pandas import DataFrame

espn_data = parsing_espn.espn_scrape()
pga_data = parsing_pgatour.ball_speed



merg_espn_test = pd.merge(espn_data, pga_data, on=['PLAYER'])
merge2 = pd.merge(merg_espn_test, parsing_pgatour.Driving_distance, on=['PLAYER'])
merge3 = pd.merge(merge2, parsing_pgatour.spin_rate, on=['PLAYER'])
merge4 = pd.merge(merge3, parsing_pgatour.chs_data, on=['PLAYER'])


final_merge = merge4
final_merge.to_csv(r'/home/egkennedy93/programming_projects/UFMBA22_Managerial_Statistics/team_project/DataSets/PGA_2020_Stats.csv', index=False, sep=',', encoding='utf-8-sig')
