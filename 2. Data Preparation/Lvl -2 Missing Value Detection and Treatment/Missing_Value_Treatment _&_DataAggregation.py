# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 16:37:27 2021

@author: Jaspreet Singh
"""
# Setting up the enivronment
import pandas as pd

# Loading the Data Sets
aqi = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -1 Data Clean/AQI_PB_DC-1.csv")
weather = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -1 Data Clean/Delhi_Weather_DC-1.csv")
cal = pd.read_excel("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -1 Data Clean/Calender_Jun2015-Nov2021.xlsx")

# Cleaning the data for further analysis

# Droping Index from Cal
cal = cal.drop('Unnamed: 0', 1)

# Changing Date Format of all the datasets
cal['Date & Time'] = pd.to_datetime(cal['Date & Time'])
aqi['timestamp'] = pd.to_datetime(aqi['timestamp'], dayfirst=True)
weather['Date & Time'] = pd.to_datetime(weather['Date & Time'], dayfirst=True)

# -- Removing Duplicates from aqi
aqi = aqi.drop_duplicates(keep='last')

# -- Removing Duplicates from weather
weather = weather.drop_duplicates(keep='last')

# Checking Missing Values in AQI
print(aqi.isnull().sum())
print(" ")

# Separating PM2.5 and PM10 as they will be used as label (y).
aqi_pm25 = aqi[['timestamp','PM2.5']]
aqi_pm10 = aqi[['timestamp','PM10']]

# Removing MVs of PM2.5
# -- PM2.5 is our dependent variable. 
# -- We will not make any adjustments or treatment for missing values in PM2.5 Feature.
print("MVs after removing null values in PM2.5")
print(" ")
aqi_pm25 = aqi_pm25[aqi_pm25['PM2.5'].notna()]
print(aqi_pm25.isnull().sum())
print(aqi_pm25.shape)
print(" ")

# Removing MVs of PM10
# -- PM10 is our dependent variable.
# -- We will not make any adjustments or treatment for missing values in PM2.5 Feature.
print("MVs after removing null values in PM10")
print(" ")
aqi_pm10 = aqi_pm10[aqi_pm10['PM10'].notna()]
print(aqi_pm10.isnull().sum())
print(aqi_pm10.shape)
print(" ")

# Treating Missing Values in Weather Data
# -- Merging Weather Data with Calender (cal) to check and treat MVs properly  
cal_weather = cal.merge(weather, how = 'left', left_on = 'Date & Time', right_on = 'Date & Time')
# -- Removing Duplicates
cal_weather = cal_weather.drop_duplicates(keep='last')

# Removing December 2021 Data as we donot have AQI data for that period
cal_weather = cal_weather.loc[(cal_weather['Date & Time'] < '2021-11-29')]

# Checking Missing Values 
print(cal_weather.isnull().sum())
print(" ")

# -- Handling Few missing values in Wind_Speed_in_Kmph column as Calm was mentioned in the column. 
# -- Calm means wind speed was less than 5 Kmph as per the website. 
# -- 3 Kmph will be better if consider values [1,2,3,4,5] Kmph as 3 is in middle of these discrete values.

def wind_calm_val(r):
    r = r
    if r['Wind_Speed_Calm'] == 1:
        return 3
    else:
        return r['Wind_Speed_in_Kmph']
    
cal_weather['Wind_Speed_in_Kmph'] = cal_weather.apply(lambda x: wind_calm_val(x), axis = 1)    

print("MVs in weather after calm wind speed treated")
print(cal_weather.isnull().sum())
print(" ")

# -- Imputing Values in Weather Data
# Missing Value treatment for continuous variables
# For more info check Imputation_for_AQI_Weather_DC_2.py script
from Imputation_for_AQI_Weather import imputate_mv

imputate_mv(cal_weather, 'Temperature_in_°C', 'Date & Time')
imputate_mv(cal_weather, 'Relative_Temp_in_°C', 'Date & Time')
imputate_mv(cal_weather, 'Wind_Speed_in_Kmph', 'Date & Time')
imputate_mv(cal_weather, 'Rel_Humidity', 'Date & Time')
imputate_mv(cal_weather, 'Dew_Point_in_°C', 'Date & Time')
imputate_mv(cal_weather, 'Atmospheric_Pressure_in_mb', 'Date & Time')

cal_weather = cal_weather.drop(['Temperature_in_°C_isnull', 'Relative_Temp_in_°C_isnull', 'Wind_Speed_in_Kmph_isnull', 'Rel_Humidity_isnull', 'Dew_Point_in_°C_isnull', 'Atmospheric_Pressure_in_mb_isnull'], 1)

# Missing Value treatment for dummy variables (Discrete)
# For more info check Imputation_for_AQI_Weather_DC_2.py script
from Imputation_for_AQI_Weather import imputate_dummy, hours

imputate_dummy(cal_weather, 'Thunder', 'Date & Time')
imputate_dummy(cal_weather, 'Few_clouds', 'Date & Time')
imputate_dummy(cal_weather, 'Rain', 'Date & Time')
imputate_dummy(cal_weather, 'Clear', 'Date & Time')
imputate_dummy(cal_weather, 'Cloudy', 'Date & Time')

cal_weather = cal_weather.drop(['Thunder_isnull', 'Few_clouds_isnull', 'Rain_isnull', 'Clear_isnull', 'Cloudy_isnull'], 1)

print("MVs in weather after Imputation Treatment")
print(cal_weather.isnull().sum())
print(" ")

# Merging Weather Data (cal_weather) and AQI (aqi_pm25)
# -- aqi_pm25 - cal_weather (Left Join) as dependent variable is in aqi_pm25 data
aqi_pm25_weather = aqi_pm25.merge(cal_weather, how = 'left', left_on = 'timestamp', right_on = 'Date & Time')

print("MVs in aqi_pm2.5_combined data after total Imputation Treatment")
print(aqi_pm25_weather.isnull().sum())
print(" ")

# Removing Rows with Missing Values in Weather Data after Imputation.
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Temperature_in_°C'].notna()]
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Wind_Speed_in_Kmph'].notna()]
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Rel_Humidity'].notna()]
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Dew_Point_in_°C'].notna()]
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Atmospheric_Pressure_in_mb'].notna()]
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Thunder'].notna()]
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Few_clouds'].notna()]
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Rain'].notna()]
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Clear'].notna()]
aqi_pm25_weather = aqi_pm25_weather[aqi_pm25_weather['Cloudy'].notna()]

# Dropping Irrelvant Columns and Features with huge missing values
aqi_pm25_weather = aqi_pm25_weather.drop(['Date & Time', 'Wind_Direction_degree', 'Description', 'Wind_Speed_Variability', 'Wind_Speed_Calm'], 1)

print("Final MVs in aqi_pm2.5_combined")
print(aqi_pm25_weather.isnull().sum())
print(" ")

# Downloading Imputed and final clean data for EDA and Feature Eng.
aqi_pm25_weather.to_csv("AQI_PM2.5_Weather_combined.csv")

# ----------------------------------------------------------- #
# ----------------------------------------------------------- #

# Merging Weather Data (cal_weather) and AQI (aqi_pm10)
# -- aqi_pm10 - cal_weather (Left Join) as dependent variable is in aqi_pm25 data
aqi_pm10_weather = aqi_pm10.merge(cal_weather, how = 'left', left_on = 'timestamp', right_on = 'Date & Time')

print("MVs in combined data after total Imputation Treatment")
print(aqi_pm10_weather.isnull().sum())
print(" ")

# Removing Rows with Missing Values in Weather Data after Imputation.
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Temperature_in_°C'].notna()]
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Wind_Speed_in_Kmph'].notna()]
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Rel_Humidity'].notna()]
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Dew_Point_in_°C'].notna()]
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Atmospheric_Pressure_in_mb'].notna()]
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Thunder'].notna()]
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Few_clouds'].notna()]
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Rain'].notna()]
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Clear'].notna()]
aqi_pm10_weather = aqi_pm10_weather[aqi_pm10_weather['Cloudy'].notna()]

# Dropping Irrelvant Columns and Features with huge missing values
aqi_pm10_weather = aqi_pm10_weather.drop(['Date & Time', 'Wind_Direction_degree', 'Description', 'Wind_Speed_Variability', 'Wind_Speed_Calm'], 1)

print("Final MVs in aqi_pm10_combined")
print(aqi_pm10_weather.isnull().sum())
print(" ")

# Downloading Imputed and final clean data for EDA and Feature Eng.
aqi_pm10_weather.to_csv("AQI_PM10_Weather_combined.csv")