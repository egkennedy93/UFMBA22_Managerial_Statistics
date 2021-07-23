#%%
import matplotlib
from matplotlib.image import BboxImage
import pandas as pd
import merging_datasets
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# plot_df = merging_datasets.final_merge
# sns.lmplot(data = plot_df, y='EARNINGS', x='RK')

# y = plot_df['EARNINGS']
# x = plot_df['RK']


# plt.ticklabel_format(useOffset=False, style='plain')
# plt.yticks()
# plt.yticks(np.arange(0,8000000,1000000.0))
# # plt.yticks(np.arange(min(y), max(y)+1, 5.0))


plot_df = merging_datasets.final_merge

val = 'AGE'

plot_df[val] = pd.to_numeric(plot_df[val])
ax = sns.scatterplot(data = plot_df, y='EARNINGS', x=val, hue='PLAYER', palette='rocket')
sns.regplot(data = plot_df, y='EARNINGS', x=val, scatter=False, ax=ax)
plt.legend(bbox_to_anchor=(1,1))




y = plot_df['EARNINGS']
x = plot_df[val]


plt.ticklabel_format(useOffset=False, style='plain')
plt.yticks()
plt.yticks(np.arange(0,8000000,1000000.0))


plt.savefig(val+'.png', format='png', facecolor='w', edgecolor='w', transparent='false', bbox_inches='tight', dpi=750)





# %%
