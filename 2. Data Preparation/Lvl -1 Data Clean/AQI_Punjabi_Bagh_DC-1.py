# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 20:46:23 2021

@author: Jaspreet Singh
"""

import pandas as pd

aqi_pb = pd.read_excel("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/1. Data Collection/Data Collected/AQI_Punjabi_Bagh_Jun2015-Nov2021_hourly.xlsx")

# Columns names
print(aqi_pb.columns)

# -- Droped first column of python index made while scraping the data
aqi_pb = aqi_pb.drop('Unnamed: 0', 1)
print(aqi_pb.columns)
print(" ")

# Missing Values Columns Wise
# -- Filtering out 'No data for a day' rows
aqi_pb = aqi_pb[(aqi_pb['PM2.5'] != 'No data for a day') & (aqi_pb['PM2.5'] != 'No data for a day_1')]  
# -- No. of MVs
print("Total Rows:", len(aqi_pb['timestamp']))
print(" ")
aqi_pb_mv = aqi_pb.isnull().sum()
aqi_pb_mv = aqi_pb_mv.to_frame()
aqi_pb_mv.columns = ['#Missing_Values']
aqi_pb_mv.insert(loc=0, column='Column_Name', value=aqi_pb_mv.index)
aqi_pb_mv.reset_index(drop=True, inplace=True)
aqi_pb_mv['%_MV-/-total'] =  (aqi_pb_mv['#Missing_Values'] / len(aqi_pb['timestamp']))*100
print(aqi_pb_mv)
print(" ")

# Data Formating
print(aqi_pb.info())
print(" ")
aqi_pb['timestamp'] = pd.to_datetime(aqi_pb['timestamp'])
aqi_pb['PM2.5'] = pd.to_numeric(aqi_pb['PM2.5'])
aqi_pb['PM10'] = pd.to_numeric(aqi_pb['PM10'])
aqi_pb['NO2'] = pd.to_numeric(aqi_pb['NO2'])
aqi_pb['NH3'] = pd.to_numeric(aqi_pb['NH3'])
aqi_pb['SO2'] = pd.to_numeric(aqi_pb['SO2'])
aqi_pb['CO'] = pd.to_numeric(aqi_pb['CO'])
aqi_pb['OZONE'] = pd.to_numeric(aqi_pb['OZONE'])
print(" ")
print("Correct DType")
print(aqi_pb.info())

# Saving the clean out put
aqi_pb.to_csv('AQI_PB_DC-1.csv', index=False)

# Data Visualisation
# -- will be done using Tableau

