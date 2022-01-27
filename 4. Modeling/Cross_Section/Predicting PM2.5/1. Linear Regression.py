# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 21:57:01 2021

@author: Jaspreet Singh
""" 
import numpy as np
import pandas as pd
import seaborn as sns
import pickle

# Reading the data
X_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Train.csv')
y_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Train.csv')
X_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Test.csv')
y_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Test.csv')

#Importing Linear Regression
from sklearn.linear_model import LinearRegression

# Fitting the Linear Regression model on Train Data.
LR = LinearRegression()
LR.fit(X_Train, y_Train)

# R Sqaure of model on both Train and Test sets.
print("Linear Regression Used")
print("R-Sqaure using all 10 features: ")
print(" ")
print("R-Sqaure on Train Set = "+str(np.round(LR.score(X_Train, y_Train), 2)))
print(" ")
print("R-Sqaure on Test Set = "+str(np.round(LR.score(X_Test, y_Test), 2)))
print(" ")

# Checking the Coeff of features in predicting our label.
intercept_coeff_10features = {"Intercept": np.round(LR.intercept_[0], 2)}
ls_coef = LR.coef_.tolist()
ls_coef = ls_coef[0]
n = -1
for col in X_Train.columns:
    n += 1
    intercept_coeff_10features[col] = np.round(ls_coef[n], 2)

print(intercept_coeff_10features)
print(" ")

# Y Test and Prediction Difference
Prediction = LR.predict(X_Test)   
sns.distplot(y_Test - Prediction)

# -- Graph looks very close to normal distribution.

# Checking MAE, MSE, RMSE value for our Linear Regression Model.
from sklearn import metrics

MAE = metrics.mean_absolute_error(y_Test, Prediction)
MSE = metrics.mean_squared_error(y_Test, Prediction)
RMSE = np.sqrt(MSE)

print("MAE: "+str(np.round(MAE, 1)))    
print("MSE: "+str(np.round(MSE, 1)))
print("RMSE: "+str(np.round(RMSE, 1)))

# converting the model into pickle
file = open('Linear_Regression_AQI.pkl', 'wb')
pickle.dump(LR, file)

