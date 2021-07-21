#%%
import pandas as pd
import merging_datasets
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb



plot_df = merging_datasets.final_merge

# y = plot_df['EARNINGS']
# x = plot_df['YDS/DRIVE']
# # x = np.arange(0, len(plot_df['RK']))

# plt.scatter(x,y)
# plt.xlabel("Rank")
# plt.ylabel("Earnings", labelpad=50)
# plt.xticks(np.arange(0, len(x)+1, 15))
# # plt.ticklabel_format(useOffset=False, style='plain')
# plt.show()

 
sb.scatterplot(x="YDS/DRIVE",
                    y="EARNINGS",
                    data=plot_df)







# %%
