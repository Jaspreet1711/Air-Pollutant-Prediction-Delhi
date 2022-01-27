# -*- coding: utf-8 -*-
"""
Created on Fri Dec 24 17:28:50 2021

@author: Jaspreet Singh
"""
# Based upon analysis done in "Feature_Selection_Analysis.ipynb" (In EDA Folder Lvl -3), I will be removing one column for now because of Multicollinearity issue.

import pandas as pd

# --------- For PM2.5 ----------- #
# Loading Data Sets
X_pm25_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/X_PM2.5_Train.csv')
y_pm25_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/y_PM2.5_Train.csv')
X_pm25_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/X_PM2.5_Test.csv')
y_pm25_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/y_PM2.5_Test.csv')

# Removing Column Relative Temperature as it was highly correlated with Temperature column.
X_pm25_Train = X_pm25_Train.drop(['Relative_Temp_in_°C'], 1)
X_pm25_Test = X_pm25_Test.drop(['Relative_Temp_in_°C'], 1)

# Removing Column Timestamp.
X_pm25_Train = X_pm25_Train.drop(['Timestamp'], 1)
X_pm25_Test = X_pm25_Test.drop(['Timestamp'], 1)

# Exporting the Dataframes in Final Data Folder
X_pm25_Train.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Train.csv", index = False)
y_pm25_Train.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Train.csv", index = False)
X_pm25_Test.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Test.csv", index = False)
y_pm25_Test.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Test.csv", index = False)

# ------------------------------------------------------------- #

# --------- For PM2.5 ----------- #
# Loading Data Sets
X_pm10_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/X_PM10_Train.csv')
y_pm10_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/y_PM10_Train.csv')
X_pm10_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/X_PM10_Test.csv')
y_pm10_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/y_PM10_Test.csv')

# Removing Column Relative Temperature as it was highly correlated with Temperature column.
X_pm10_Train = X_pm10_Train.drop(['Relative_Temp_in_°C'], 1)
X_pm10_Test = X_pm10_Test.drop(['Relative_Temp_in_°C'], 1)

# Removing Column Timestamp.
X_pm10_Train = X_pm10_Train.drop(['Timestamp'], 1)
X_pm10_Test = X_pm10_Test.drop(['Timestamp'], 1)

# Exporting the Dataframes in Final Data Folder
X_pm10_Train.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM10_Train.csv", index = False)
y_pm10_Train.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM10_Train.csv", index = False)
X_pm10_Test.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM10_Test.csv", index = False)
y_pm10_Test.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM10_Test.csv", index = False)


