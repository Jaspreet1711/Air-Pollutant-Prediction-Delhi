# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 11:01:31 2021

@author: Jaspreet Singh
"""

import pandas as pd

aqi_av = pd.read_excel("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/1. Data Collection/Data Collected/AQI_Anand_Vihar_Nov2017-Nov2021.xlsx")

# Columns names
print(aqi_av.columns)

# -- Droped first column of python index made while scraping the data
aqi_av = aqi_av.drop('Unnamed: 0', 1)
print(aqi_av.columns)
print(" ")

# Missing Values Columns Wise
# -- Filtering out 'No data for a day' rows
aqi_av = aqi_av[(aqi_av['PM2.5'] != 'No data for a day') & (aqi_av['PM2.5'] != 'No data for a day_1')]  
# -- No. of MVs
print("Total Rows:", len(aqi_av['timestamp']))
print(" ")
aqi_av_mv = aqi_av.isnull().sum()
aqi_av_mv = aqi_av_mv.to_frame()
aqi_av_mv.columns = ['#Missing_Values']
aqi_av_mv.insert(loc=0, column='Column_Name', value=aqi_av_mv.index)
aqi_av_mv.reset_index(drop=True, inplace=True)
aqi_av_mv['%_MV-/-total'] =  (aqi_av_mv['#Missing_Values'] / len(aqi_av['timestamp']))*100
print(aqi_av_mv)
print(" ")

# Data Formating
print(aqi_av.info())
print(" ")
aqi_av['timestamp'] = pd.to_datetime(aqi_av['timestamp'])
aqi_av['PM2.5'] = pd.to_numeric(aqi_av['PM2.5'])
aqi_av['PM10'] = pd.to_numeric(aqi_av['PM10'])
aqi_av['NO2'] = pd.to_numeric(aqi_av['NO2'])
aqi_av['NH3'] = pd.to_numeric(aqi_av['NH3'])
aqi_av['SO2'] = pd.to_numeric(aqi_av['SO2'])
aqi_av['CO'] = pd.to_numeric(aqi_av['CO'])
aqi_av['OZONE'] = pd.to_numeric(aqi_av['OZONE'])
print(" ")
print("Correct DType")
print(aqi_av.info())

# Saving the clean out put
aqi_av.to_csv('AQI_AV_DC-1.csv', index=False)

# Data Visualisation
# -- will be done using Tableau

