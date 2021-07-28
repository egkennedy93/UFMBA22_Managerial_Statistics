import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.linear_model import LinearRegression
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(dir_path+'/DataSets/PGA_2020_Stats.csv')

x = df['PUTTING FROM INSIDE INSIDE 5\'_%'].values.reshape(-1,1)
y = df['EARNINGS'].values

model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)

#intercept is b0
print('intercept: {}'.format(model.intercept_))

# b1 is the predicted response per x
print('slope: {}'.format(model.coef_[0]))


print('r_squared: {}'.format(r_sq))

print('summary stats: {}'.format(df['PUTTING FROM INSIDE INSIDE 5\'_%'].describe()))