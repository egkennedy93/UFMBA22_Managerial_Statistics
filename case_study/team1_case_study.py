import pandas as pd
import numpy as np
from sklearn import linear_model
import os


dirpath = os.path.dirname(os.path.realpath(__file__))

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
    print("Average salary")
    print(df['lsalary'].mean())
    print("\n")

    # average tenure
    print("Average tenure")
    print(df['ceoten'].mean())
    print("\n")

    # Question 1 part II

    # beginner CEOs
    print("Question 1, Part II")
    print("how many CEOs are in their first year as CEO?")
    print(df['ceoten'].value_counts()[0])
    print("\n")

    #longest running CEO
    print("What is the longest tenure as a CEO")
    print(df['ceoten'].max())
    print("\n")

    # Question  1 part III
    print("simple regression result")

    # independent variable
    x = df
    # dependent variable
    y = df['lsalary']
    
    # building model
    lm = linear_model.LinearRegression()
    model = lm.fit(x,y)

    #predicting the value
    predictions = lm.predict(x)

    print(model)
    print(predictions)


def question_2():
    
    # Question 1
    print("QUESTION 2")
    print("========================================")
    # this will utilize the WAGE2.XLS file
    # df is a pandas dataframe object
    df = pd.read_excel(dirpath+'/WAGE2.xls')

    # Question 2, part I
    print("Average salary ")
    print(df['lwage'].mean())
    print("\n")

    print("Average IQ")
    print(df['IQ'].mean())
    print("\n")

    print("IQ Standard deviation")
    print(df['IQ'].std())







# print(question_1())
print(question_2())