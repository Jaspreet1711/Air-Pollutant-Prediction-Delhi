# -*- coding: utf-8 -*-
"""
Created on Sat Jan  1 14:46:35 2022

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

# Importing RandomizedSearchCV from sklearn.
from sklearn.model_selection import RandomizedSearchCV

#----------------------------------------------------------------------------#
# -- number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1500, num =15)]
# -- number of features to consider at every split 
max_features = ['auto', 'sqrt']
# -- maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]
# -- minimum number of samples required to split a node 
min_samples_split = [ 2, 5, 10, 15, 100]
# -- minimum number of samples required at each leaf node 
min_samples_leaf = [ 1, 2, 5, 10]
#----------------------------------------------------------------------------#
  
# Creating the Random Grid 
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}
print(random_grid)
print(" ")

# Importing RandomForest Regression
from sklearn.ensemble import RandomForestRegressor
RFR = RandomForestRegressor()

# Random Searching of parameters, using 5 folds cross validation.
# -- It will try 100 different combinations of paratmeters to determine the best score.
rf_random = RandomizedSearchCV(estimator = RFR, 
                               param_distributions = random_grid, 
                               scoring = 'neg_mean_squared_error', 
                               n_iter = 100, 
                               cv = 5, 
                               verbose = 2, 
                               random_state = 10)

# Fitting the train data and searching the best parameters to get high accuracy using RandomForest Regression.
# -- It will take 8 to 10 minutes.
rf_random.fit(X_Train, y_Train) 
print(" ")

# Getting the best parameters and accuracy score.
print(rf_random.best_params_)
print(" ")
print(rf_random.best_score_)
print(" ")

# Y Test and Prediction Difference
Prediction = rf_random.predict(X_Test)
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

