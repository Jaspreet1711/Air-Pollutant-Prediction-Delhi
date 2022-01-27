# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 12:30:04 2022

@author: Jaspreet Singh
"""
import pandas as pd
import numpy as np
import seaborn as sns

# Reading the data
X_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Train.csv')
y_Train = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Train.csv')
X_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/X_PM2.5_Test.csv')
y_Test = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/y_PM2.5_Test.csv')

# Importing Keras for making ANN Model
from keras.models import Sequential
from keras.layers import Dense, LeakyReLU, PReLU, ELU, Dropout

# Crearing the Neural Network
NN_Model = Sequential()

# -- Input Layer 
NN_Model.add(Dense(128, kernel_initializer = 'normal', input_dim = X_Train.shape[1]))

# -- Hidden Layer
NN_Model.add(Dense(256, kernel_initializer = 'normal', activation = 'relu'))
NN_Model.add(Dense(256, kernel_initializer = 'normal', activation = 'relu'))
NN_Model.add(Dense(256, kernel_initializer = 'normal', activation = 'relu'))

# -- Output Layer
NN_Model.add(Dense(1, kernel_initializer = 'normal', activation = 'linear'))

# Compiling and summarizing the Network
NN_Model.compile(loss = 'mean_absolute_error', 
                 optimizer = 'adam', 
                 metrics = ['mean_absolute_error'])
    
NN_Model.summary()
 
# Fitting the ANN Model to Training Dataset
NNModel_Fit = NN_Model.fit(X_Train, y_Train, 
                             validation_split = 0.1,
                             batch_size = 10,
                             epochs = 100, 
                             )


# Y Test and Prediction Difference
Prediction = NN_Model.predict(X_Test)
Prediction = pd.DataFrame(Prediction, columns = ['Pred']) 
sns.distplot(y_Test['PM2.5'] - Prediction['Pred'])

# Checking MAE, MSE, RMSE value for our RandomForest Regression Model.
from sklearn import metrics

MAE = metrics.mean_absolute_error(y_Test['PM2.5'], Prediction['Pred'])
MSE = metrics.mean_squared_error(y_Test['PM2.5'], Prediction['Pred'])
RMSE = np.sqrt(MSE)

print("MAE: "+str(np.round(MAE, 1)))    
print("MSE: "+str(np.round(MSE, 1)))
print("RMSE: "+str(np.round(RMSE, 1)))




