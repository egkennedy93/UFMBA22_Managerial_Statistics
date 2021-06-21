
import pandas as pd
import numpy as np
from pandas.core.frame import DataFrame, Series
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import os, sys


dirpath = os.path.dirname(os.path.realpath(__file__))
#dirpath = os.path.dirname(os.path.realpath('/mnt/g/programing_projects/UFMBA_stats/UFMBA22_Managerial_Statistics/case_study'))


# This is the file that will return all of the answers for the case project
def question_1():
    # Question 1
    print("QUESTION 1")
    print("========================================")
    # this will utilize the CEOSAL2.XLS file

    # df is a pandas dataframe object
    df = pd.read_excel(dirpath+'/CEOSAL2.xls')

    # Question 1 part i

    #average salary
    print("Question 1, Part I")
    print("========================================")
    print("Average salary")
    print(df['lsalary'].mean())

    # average tenure
    print("Average tenure")
    print(df['ceoten'].mean())

    # Question 1 part II

    # beginner CEOs
    print("Question 1, Part II")
    print("========================================")
    print("how many CEOs are in their first year as CEO?")
    print(df['ceoten'].value_counts()[0])

    #longest running CEO
    print("What is the longest tenure as a CEO")
    print(df['ceoten'].max())

    # Question  1 part III
    print("Question 1, Part III")
    print("========================================")
    print("simple regression result")

    # independent variable
    x = df['ceoten'].values.reshape(-1,1)
    y = np.log(df['salary'].values)
    

    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)
    
    #intercept is b0
    print('intercept: {}'.format(model.intercept_))

    # b1 is the predicted response per x
    print('slope: {}'.format(model.coef_[0]))


    print('r_squared: {}'.format(r_sq))

    print('predicted percentage increase given one more year as CEO: {} %'.format(model.predict(np.arange(1).reshape(1,-1))))
    return " "
    
def question_2():
    
    # Question 2
    print("QUESTION 2")
    print("========================================")
    # this will utilize the WAGE2.XLS file
    # df is a pandas dataframe object
    df = pd.read_excel(dirpath+'/WAGE2.xls')

    # Question 2, part I
    print("Question 2, Part I")
    print("========================================")

    print("Average salary ")
    print(df['wage'].mean())

    print("Average IQ")
    print(df['IQ'].mean())

    print("IQ Standard deviation")
    print(df['IQ'].std())

    #Question 2, part2
    print("Question 2, Part II")
    print("========================================")

    x = df['IQ'].to_numpy().reshape((-1,1))
    y = df['wage'].to_numpy()
    model = LinearRegression().fit(x, y)
    r_sq = model.score(x, y)

    #intercept is b0
    print('intercept: {}'.format(model.intercept_))

    # b1 is the predicted response per x
    print('slope: {}'.format(model.coef_[0]))
    print('r_squared: {}'.format(r_sq))

    predicted_values = model.predict(np.arange(16).reshape(-1,1))
    print('1 pt increase in IQ will increase wage by: {}'.format(predicted_values[1]))
    print('a 15 pt increase in IQ will increase wage by: {}'.format(predicted_values[15]))

    print("Question 2, Part III")
    print("========================================")
    y_log = df['lwage'].to_numpy()
    log_model = LinearRegression().fit(x, y_log)
    log_r_sq = log_model.score(x, y_log)

    #intercept is b0
    print('intercept: {}'.format(log_model.intercept_))

    # b1 is the predicted response per x
    print('slope: {}'.format(log_model.coef_[0]))
    print('r_squared: {}'.format(log_r_sq))

    predicted_values = log_model.predict(np.arange(16).reshape(-1,1))
    print('a 15 pt increase in IQ will increase wage by a percent of: {}'.format(predicted_values[15]))
    return " "

def question_3():
    print("QUESTION 3")
    print("========================================")
    print("building data....")
    df = pd.read_excel(dirpath+'/hprice1.xls')
    y = df['price'].values.reshape(-1,1)
    x_values_df = df.filter(['sqrft', 'bdrms']).values
    model = LinearRegression().fit(x_values_df, y)
    #r-squared
    print('rsquared: {}'.format(model.score(x_values_df, y)))
    #intercept is b0
    print('intercept: {}'.format(model.intercept_[0]))
    # b1 is the predicted response per x
    print('sqrft slope: {}'.format(model.coef_[0][0]))
    print('bdrms slope: {}'.format(model.coef_[0][1]))
    # # Question 3 part I
    print("Question 3 Part I")
    print("========================================")
    b_0 = np.round(model.intercept_[0]*1000,decimals=4)
    b_1 = np.round(model.coef_[0][0]*1000,decimals=4)
    b_2 = np.round(model.coef_[0][1]*1000,decimals=4)

    print('y={} + {}sqrft + {}bdrms + u'.format(b_0, b_1, b_2))
    # Question 3 Part II
    print("Question 3 Part II")
    print("========================================")
    q3_p2 = np.round(model.predict([[1,1]])[0][0]*1000, decimals=4)
    print('Price increase when 1 bedroom is added, holding sqrft constant:\n{}'.format(q3_p2))
    # Question 3 Part III
    print("Question 3 Part III")
    print("========================================")
    print("what is the estimated increase in price for a house with an additional bedroom that is 140sqrft in size")

    adjusted_b_1 = np.round(model.predict([[140,1]])[0][0]*1000, decimals=4)
    # solve = b_1*140 + b_2
    # print(np.round(solve,decimals=4))
    print(adjusted_b_1)
    print("adding 140 sqrft, increased the price by an additional compared to part II\n{}".format(np.round(adjusted_b_1 - q3_p2, decimals=4)))
    # Question 3 Part IV
    print("question 3 Part IV")
    print("========================================")
    print(model.score(x_values_df, y))
    # Question 3 Part V
    print("Question 3 Part V")
    print("========================================")
    predicted_val = np.round(model.predict([[2438, 4]])[0][0], decimals=4)
    print(predicted_val)
    # Question 3 Part VI
    print("Question 3 part VI")
    print("========================================")
    print("Predicted: {} Actual:{} \nresidual:  {}".format(predicted_val, 300, np.round(predicted_val - 300, decimals=4)))
    print("\n")
    return " "

def question_4():
    print("QUESTION 4")
    print("========================================")
    df = pd.read_excel(dirpath+'/ATTEND.xls')

    # Question 4 Part I
    print("Question 4 Part I")
    print("========================================")
    print("the min, max, and mean for atndrte, priGPA, and ACT are:\n")
    print(df[['atndrte', 'priGPA', 'ACT']].describe().loc[['mean', 'min','max']])
    print("\n")
    
    # Question 4 part II
    print("Question 4 Part II")
    print("========================================")
    y = df['atndrte'].values.reshape(-1,1)
    x = df.filter(['priGPA', 'ACT']).values
    model = LinearRegression().fit(x,y)
    r_sq=model.score(x,y)

    intercept = np.round(model.intercept_[0],decimals=4) 
    priGPA_coef = np.round(model.coef_[0][0],decimals=4)
    ACT_coef = np.round(model.coef_[0][1],decimals=4)

    #intercept is b0
    print('intercept: {}'.format(intercept))
    # b1 is the predicted response per x
    print('priGPA slope: {}'.format(priGPA_coef))
    print('ACT slope: {}'.format(ACT_coef))
    print("\n")
    print('y={} + {}priGPA {}ACT + u'.format(intercept, priGPA_coef, ACT_coef))
    print("regardless of any coefficent, a student will have a atndrte of {}".format(intercept))
    print("\n")

    # Question 4 Part III
    print("Question 4 part III")
    print("========================================")
    person_predicted = np.round(model.predict([[3.1,21],[2.1,26]]),decimals=4)
    person_A = person_predicted[0][0]
    person_B = person_predicted[1][0]
    print("Person A is predicted {} and person B is predicted {} for a difference of {}".format(person_A, person_B, person_A-person_B))
    return " "

def question_5():
    print("QUESTION 5")
    print("========================================")
    df = pd.read_excel(dirpath+'/MLB1.xls')

    # Question 5 part I
    print("Question 5 Part I")
    print("========================================")
    y = df['lsalary'].values.reshape(-1,1)
    x = df.filter(['years', 'gamesyr','bavg', 'hrunsyr']).values
    model = LinearRegression().fit(x,y)
    print(model.coef_)
    print(model.intercept_)


    # Question 5 Part II
    print("Question 5 part II")
    print("========================================")
    new_x = df.filter(['years', 'gamesyr','bavg', 'hrunsyr', 'runsyr', 'fldperc', 'sbasesyr']).values
    new_model = LinearRegression().fit(new_x, y)
    print(new_model.coef_)

    # Question 5 Part III
    print("Question 5 part III")
    print("========================================")

# import pandas as pd
# import numpy as np
# from pandas.core.frame import DataFrame, Series
# import sklearn
# from sklearn.linear_model import LinearRegression
# from sklearn import metrics
# import os, sys

# df.plot(x=['years', 'gamesyr','bavg', 'hrunsyr', 'runsyr', 'fldperc', 'sbasesyr'], y='wage', style='o')
# plt.title('IQ VS Wage')
# plt.xlabel('IQ')
# plt.ylabel('wage')
# plt.show()
    


# printing results to results.txt file
original_stdout = sys.stdout
with open(dirpath+'/results.txt', 'w') as f:
    sys.stdout = f
    print(question_1())
    print("\n")
    print(question_2())
    print("\n")
    print(question_3())
    print("\n")
    print(question_4())
    print("\n")
    print(question_5())
    sys.stdout = original_stdout

# print(question_3())



