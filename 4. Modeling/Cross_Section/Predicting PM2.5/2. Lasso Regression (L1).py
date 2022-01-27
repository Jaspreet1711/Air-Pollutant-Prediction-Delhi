# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 21:44:54 2021

@author: Jaspreet Singh
"""
import numpy as np
import pandas as pd
import seaborn as sns

# Reading the data
X_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Train.csv')
y_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Train.csv')
X_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Test.csv')
y_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Test.csv')

#Importing Lasso Regression
from sklearn.linear_model import Lasso 
a = 2.1
lasso = Lasso(alpha = a, max_iter = 100, tol = 0.1)
lasso.fit(X_Train, y_Train)

# R Sqaure of model on both Train and Test sets.
print("Lasso Regression Used with alpha: "+str(a))
print("R-Sqaure using all 14 features: ")
print(" ")
print("R-Sqaure on Train Set = "+str(np.round(lasso.score(X_Train, y_Train), 2)))
print(" ")
print("R-Sqaure on Test Set = "+str(np.round(lasso.score(X_Test, y_Test), 2)))
print(" ")

# Y Test and Prediction Difference
Prediction = lasso.predict(X_Test)   
#sns.distplot(y_Test - Prediction)

# -- Graph looks very close to normal distribution.

# Checking MAE, MSE, RMSE value for our Linear Regression Model.
from sklearn import metrics

MAE = metrics.mean_absolute_error(y_Test, Prediction)
MSE = metrics.mean_squared_error(y_Test, Prediction)
RMSE = np.sqrt(MSE)

print("MAE: "+str(np.round(MAE, 1)))    
print("MSE: "+str(np.round(MSE, 1)))
print("RMSE: "+str(np.round(RMSE, 1)))