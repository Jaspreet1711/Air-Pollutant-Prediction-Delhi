# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 15:48:03 2021

@author: Jaspreet Singh
"""
import pandas as pd

aqi_pm25_df = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -2 Missing Value Detection and Treatment/AQI_PM2.5_Weather_combined.csv")
aqi_pm10_df = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -2 Missing Value Detection and Treatment/AQI_PM10_Weather_combined.csv")

# Splitting Data into Train and Test then performing scaling
# Import the modules
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # --- Z Score Method
# -- Zscore Standardization Dataset
scaler = StandardScaler()

# ------------------------------------------------------------------------------- #

# -- Preparing Train-Test for AQI_PM2.5
X_pm25 = aqi_pm25_df[['timestamp', 'Temperature_in_°C', 'Relative_Temp_in_°C', 'Wind_Speed_in_Kmph', 'Rel_Humidity', 'Dew_Point_in_°C', 'Atmospheric_Pressure_in_mb', 'Thunder', 'Few_clouds', 'Rain', 'Clear', 'Cloudy']]
y_pm25 = aqi_pm25_df['PM2.5']

X_pm25_train, X_pm25_test, y_pm25_train, y_pm25_test = train_test_split(X_pm25, y_pm25, test_size = 0.2, random_state= 21)

y_pm25_Train, y_pm25_Test = y_pm25_train.to_frame('PM2.5'), y_pm25_test.to_frame('PM2.5')

# Removing columns which should not be scaled
X_train_pm25_1 = X_pm25_train.drop(['timestamp', 'Thunder', 'Few_clouds','Rain','Clear','Cloudy'], 1)
X_test_pm25_1 = X_pm25_test.drop(['timestamp', 'Thunder', 'Few_clouds','Rain','Clear','Cloudy'], 1)

### Feature Scaling ###

# Fit the model for X 
scaler.fit(X_train_pm25_1)

# Transforming the both train and test based on train dataset fit.   
X_pm25_Train = scaler.transform(X_train_pm25_1)
X_pm25_Test = scaler.transform(X_test_pm25_1)

X_pm25_Train = pd.DataFrame(data = X_pm25_Train, columns = X_train_pm25_1.columns, index = X_pm25_train.index)
X_pm25_Test = pd.DataFrame(data = X_pm25_Test, columns = X_test_pm25_1.columns, index = X_pm25_test.index)

# -- We donot want to apply StandardScaler on these dicrete columns. So, replacing them with orignal values.   

X_pm25_Train.insert(loc = 0, column='Timestamp', value = X_pm25_train['timestamp'])
X_pm25_Train['Thunder'] = X_pm25_train['Thunder']
X_pm25_Train['Few_clouds'] = X_pm25_train['Few_clouds']
X_pm25_Train['Rain'] = X_pm25_train['Rain']
X_pm25_Train['Clear'] = X_pm25_train['Clear']
X_pm25_Train['Cloudy'] = X_pm25_train['Cloudy']

X_pm25_Test.insert(loc = 0, column='Timestamp', value = X_pm25_test['timestamp'])
X_pm25_Test['Thunder'] = X_pm25_test['Thunder']
X_pm25_Test['Few_clouds'] = X_pm25_test['Few_clouds']
X_pm25_Test['Rain'] = X_pm25_test['Rain']
X_pm25_Test['Clear'] = X_pm25_test['Clear']
X_pm25_Test['Cloudy'] = X_pm25_test['Cloudy']

# Downloading Scaled Datasets
X_pm25_Train.to_csv("X_PM2.5_Train.csv", index = False)
y_pm25_Train.to_csv("y_PM2.5_Train.csv", index = False)
X_pm25_Test.to_csv("X_PM2.5_Test.csv", index = False)
y_pm25_Test.to_csv("y_PM2.5_Test.csv", index = False)

# ------------------------------------------------------------------------------- #

# -- Preparing Train-Test for AQI_PM10
X_pm10 = aqi_pm10_df[['timestamp', 'Temperature_in_°C', 'Relative_Temp_in_°C', 'Wind_Speed_in_Kmph', 'Rel_Humidity', 'Dew_Point_in_°C', 'Atmospheric_Pressure_in_mb', 'Thunder', 'Few_clouds', 'Rain', 'Clear', 'Cloudy']]
y_pm10 = aqi_pm10_df['PM10']

X_pm10_train, X_pm10_test, y_pm10_train, y_pm10_test = train_test_split(X_pm10, y_pm10, test_size = 0.2)

y_pm10_Train, y_pm10_Test = y_pm10_train.to_frame('PM10'), y_pm10_test.to_frame('PM10')

# Removing columns which should not be scaled
X_train_pm10_1 = X_pm10_train.drop(['timestamp', 'Thunder', 'Few_clouds','Rain','Clear','Cloudy'], 1)
X_test_pm10_1 = X_pm10_test.drop(['timestamp', 'Thunder', 'Few_clouds','Rain','Clear','Cloudy'], 1)

### Feature Scaling ###

# Fit the model for X
scaler.fit(X_train_pm25_1)

# Transforming the both train and test based on train dataset fit.
X_pm10_Train = scaler.transform(X_train_pm10_1)
X_pm10_Test = scaler.transform(X_test_pm10_1)

X_pm10_Train = pd.DataFrame(data = X_pm10_Train, columns = X_train_pm10_1.columns, index = X_pm10_train.index)
X_pm10_Test = pd.DataFrame(data = X_pm10_Test, columns = X_test_pm10_1.columns, index = X_pm10_test.index)

# -- We donot want to apply StandardScaler on these dicrete columns. So, replacing them with orignal values.

X_pm10_Train.insert(loc = 0, column='Timestamp', value = X_pm10_train['timestamp'])
X_pm10_Train['Thunder'] = X_pm10_train['Thunder']
X_pm10_Train['Few_clouds'] = X_pm10_train['Few_clouds']
X_pm10_Train['Rain'] = X_pm10_train['Rain']
X_pm10_Train['Clear'] = X_pm10_train['Clear']
X_pm10_Train['Cloudy'] = X_pm10_train['Cloudy']

X_pm10_Test.insert(loc = 0, column='Timestamp', value = X_pm10_test['timestamp'])
X_pm10_Test['Thunder'] = X_pm10_test['Thunder']
X_pm10_Test['Few_clouds'] = X_pm10_test['Few_clouds']
X_pm10_Test['Rain'] = X_pm10_test['Rain']
X_pm10_Test['Clear'] = X_pm10_test['Clear']
X_pm10_Test['Cloudy'] = X_pm10_test['Cloudy']

# Downloading Scaled Datasets
X_pm10_Train.to_csv("X_PM10_Train.csv", index = False)
y_pm10_Train.to_csv("y_PM10_Train.csv", index = False)
X_pm10_Test.to_csv("X_PM10_Test.csv", index = False)
y_pm10_Test.to_csv("y_PM10_Test.csv", index = False)

