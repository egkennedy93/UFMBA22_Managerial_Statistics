#%%
import matplotlib
from matplotlib.image import BboxImage
import pandas as pd
import merging_datasets
from pandas import DataFrame
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# the plot DataFrame
plot_df = merging_datasets.final_merge

#holding variable for the independent variables
val = 'TOTAL CLUB HEAD SPEED'
#validating that all values are numeric
plot_df[val] = pd.to_numeric(plot_df[val])
#building the scatterplot
ax = sns.scatterplot(data = plot_df, y='EARNINGS', x=val, hue='PLAYER', palette='rocket')
sns.regplot(data = plot_df, y='EARNINGS', x=val, scatter=False, ax=ax)
plt.legend(bbox_to_anchor=(1,1))

#setting the x and y variables 
y = plot_df['EARNINGS']
x = plot_df[val]

#formatting the plot
plt.ticklabel_format(useOffset=False, style='plain')
plt.yticks()
plt.yticks(np.arange(0,8000000,1000000.0))

#saving to a PNG file
plt.savefig(val+'.png', format='png', facecolor='w', edgecolor='w', transparent='false', bbox_inches='tight', dpi=750)





# %%
