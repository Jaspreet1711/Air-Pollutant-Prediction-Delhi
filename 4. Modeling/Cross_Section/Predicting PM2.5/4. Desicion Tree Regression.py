# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 11:47:53 2021

@author: Jaspreet Singh
"""
import numpy as np
import pandas as pd

# Reading the data
X_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Train.csv')
y_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Train.csv')
X_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Test.csv')
y_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Test.csv')

# Importing the desicion tree regressor from sklearn.
from sklearn.tree import DecisionTreeRegressor

dtree = DecisionTreeRegressor(criterion = 'mse')

# Fitting the Model on Training Set
dtree.fit(X_Train, y_Train)

# R Sqaure of model on both Train and Test sets.
print("Decision Tree Regression Used")
print("R-Sqaure using all 10 features: ")
print(" ")
print("R-Sqaure on Train Set = "+str(np.round(dtree.score(X_Train, y_Train), 2)))
print(" ")
print("R-Sqaure on Test Set = "+str(np.round(dtree.score(X_Test, y_Test), 2)))
print(" ")

# -- This model is overfitting.