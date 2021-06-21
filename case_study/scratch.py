#%%
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame, Series
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import os, sys
import matplotlib as plt
import seaborn as sns



df = pd.read_excel('/mnt/g/programing_projects/UFMBA_stats/UFMBA22_Managerial_Statistics/case_study/hprice1.xls')
#%%
plt = sns.lmplot(x='bdrms', y='price', data=df)
# %%
plt = sns.lmplot(x='sqrft', y='price', data=df)

# %%
df
# %%
