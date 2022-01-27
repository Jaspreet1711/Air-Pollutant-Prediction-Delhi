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
# Removing MVs of PM2.5 

# -- PM2.5 is our dependent variable. 
# -- We will not make any adjustments or treatment for missing values in PM2.5 Feature.
print("MVs after removing null values in PM2.5")
print(" ")
#aqi = aqi[aqi['PM2.5'].notna()] 
print(aqi.isnull().sum())

# Treating Missing Values in AQI Data
# For more info check Imputation_for_AQI_Weather_DC_2.py script
from Imputation_for_AQI_Weather import imputate_mv

imputate_mv(aqi, 'PM2.5', 'timestamp')
imputate_mv(aqi, 'PM10', 'timestamp')
imputate_mv(aqi, 'NO2', 'timestamp')
imputate_mv(aqi, 'SO2', 'timestamp')
imputate_mv(aqi, 'CO', 'timestamp')
imputate_mv(aqi, 'OZONE', 'timestamp')
imputate_mv(aqi, 'NH3', 'timestamp')

aqi = aqi.drop(['PM2.5_isnull', 'PM10_isnull', 'NO2_isnull', 'SO2_isnull', 'CO_isnull', 'OZONE_isnull', 'NH3_isnull'], 1)

print("MVs after treatment")
#aqi = aqi[aqi['PM2.5'].notna()] 
print(aqi.isnull().sum())
print(" ")

# Droping Ozone and NH3 as there are huge missing values. These features will not help in model.

aqi = aqi.drop(['OZONE', 'NH3'], 1)

print("Final MVs and AQI Data Shape")
#print(aqi.isnull().sum())
#print(" ")
print(aqi.shape)
print(" ")

# Downloading Imputed and final clean data for EDA and Feature Eng.
aqi.to_csv("AQI_TS_Hourly.csv", index = False)

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
# For more info check Imputation_for_AQI_Weather_DC_2.py script
imputate_mv(cal_weather, 'Temperature_in_°C', 'Date & Time')
imputate_mv(cal_weather, 'Relative_Temp_in_°C', 'Date & Time')
imputate_mv(cal_weather, 'Wind_Speed_in_Kmph', 'Date & Time')
imputate_mv(cal_weather, 'Rel_Humidity', 'Date & Time')
imputate_mv(cal_weather, 'Dew_Point_in_°C', 'Date & Time')
imputate_mv(cal_weather, 'Atmospheric_Pressure_in_mb', 'Date & Time')

cal_weather = cal_weather.drop(['Temperature_in_°C_isnull', 'Relative_Temp_in_°C_isnull', 'Wind_Speed_in_Kmph_isnull', 'Rel_Humidity_isnull', 'Dew_Point_in_°C_isnull', 'Atmospheric_Pressure_in_mb_isnull'], 1)

print("MVs in weather after Imputation Treatment")
print(cal_weather.isnull().sum())
print(" ")

from Imputation_for_AQI_Weather import imputate_dummy, hours

imputate_dummy(cal_weather, 'Thunder', 'Date & Time')
imputate_dummy(cal_weather, 'Few_clouds', 'Date & Time')
imputate_dummy(cal_weather, 'Rain', 'Date & Time')
imputate_dummy(cal_weather, 'Clear', 'Date & Time')
imputate_dummy(cal_weather, 'Cloudy', 'Date & Time')

cal_weather = cal_weather.drop(['Thunder_isnull', 'Few_clouds_isnull', 'Rain_isnull', 'Clear_isnull', 'Cloudy_isnull'], 1)

print("Final MVs after dummy variable mvs treatment")
print(cal_weather.isnull().sum())
print(" ")

# Downloading Imputed and final clean data for EDA and Feature Eng.
cal_weather.to_csv("Weather_TS_Hourly.csv", index = False)
