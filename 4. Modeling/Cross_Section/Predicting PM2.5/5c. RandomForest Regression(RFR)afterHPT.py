# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 08:24:16 2022

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
RFR = RandomForestRegressor(n_estimators =  400, min_samples_split = 5, min_samples_leaf = 2, max_features = 'sqrt', max_depth = 15, random_state = 21)
RFR.fit(X_Train, y_Train)

# R Sqaure of model on both Train and Test sets.
print("Random Forest Regression Used after HPT")
print("R-Sqaure using all 10 features: ")
print(" ")
print("R-Sqaure on Train Set = "+str(np.round(RFR.score(X_Train, y_Train), 2)))
print("R-Sqaure on Test Set = "+str(np.round(RFR.score(X_Test, y_Test), 2)))
print(" ")

# -- R Sqaure on both train and test has increased which was expected as Random Forest is an ensemble technique.
# -- But still it is overfitting as Train R Square is higher than Test.

# Y Test and Prediction Difference
Prediction = RFR.predict(X_Test)
Prediction = pd.DataFrame(Prediction, columns = ['Pred']) 
sns.distplot(y_Test['PM2.5'] - Prediction['Pred'])

# -- Graph looks very close to normal distribution.

# Checking MAE, MSE, RMSE value for our RandomForest Regression Model.
from sklearn import metrics

MAE = metrics.mean_absolute_error(y_Test['PM2.5'], Prediction['Pred'])
MSE = metrics.mean_squared_error(y_Test['PM2.5'], Prediction['Pred'])
RMSE = np.sqrt(MSE)

print("MAE: "+str(np.round(MAE, 1)))    
print("MSE: "+str(np.round(MSE, 1)))
print("RMSE: "+str(np.round(RMSE, 1)))



