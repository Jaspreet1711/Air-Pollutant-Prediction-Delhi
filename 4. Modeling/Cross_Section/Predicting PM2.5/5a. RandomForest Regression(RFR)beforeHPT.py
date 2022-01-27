# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 14:56:14 2021

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

#Importing RandomForest Regression
from sklearn.ensemble import RandomForestRegressor

# Fitting the RandomForest Regression model on Train Data.
RFR = RandomForestRegressor()
RFR.fit(X_Train, y_Train)

# R Sqaure of model on both Train and Test sets.
print("Random Forest Regression Used before HPT")
print("R-Sqaure using all 10 features: ")
print(" ")
print("R-Sqaure on Train Set = "+str(np.round(RFR.score(X_Train, y_Train), 2)))
print("R-Sqaure on Test Set = "+str(np.round(RFR.score(X_Test, y_Test), 2)))
print(" ")

# -- R Sqaure on both train and test has increased which was expected as Random Forest is an ensemble technique.
# -- But still it is overfitting as Train R Square is higher than Test.

# Y Test and Prediction Difference
Prediction = RFR.predict(X_Test)
Prediction = pd.DataFrame(Prediction) 
sns.distplot(y_Test - Prediction)

# -- Graph looks very close to normal distribution.

# Checking MAE, MSE, RMSE value for our RandomForest Regression Model.
from sklearn import metrics

MAE = metrics.mean_absolute_error(y_Test, Prediction)
MSE = metrics.mean_squared_error(y_Test, Prediction)
RMSE = np.sqrt(MSE)

print("MAE: "+str(np.round(MAE, 1)))    
print("MSE: "+str(np.round(MSE, 1)))
print("RMSE: "+str(np.round(RMSE, 1)))

# -- Let's perform hyperparameter tuning to overcome this overfitting issue and also increase the overall accuracy








