# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 15:04:42 2021

@author: Jaspreet Singh
"""

import pandas as pd

dw = pd.read_excel("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/1. Data Collection/Data Collected/Delhi_Weather_report_June2015-November2021_hourly.xlsx")

# Columns in data
print(dw.columns)
print(" ")

# Dropping first column
dw = dw.drop('Unnamed: 0', 1)
print(dw.columns)
print(" ")

# checking missing data
dw_mv = dw.isnull().sum()
dw_mv = dw_mv .to_frame()
dw_mv .columns = ['#Missing_Values']
dw_mv .insert(loc=0, column='Column_Name', value=dw_mv .index)
dw_mv .reset_index(drop=True, inplace=True)
dw_mv ['%_MV-/-total'] =  (dw_mv ['#Missing_Values'] / len(dw['Date & Time']))*100
print(dw_mv )
print(" ")

# Droping Wind Gust Column as 100% is missing
dw = dw.drop('Wind_Gust', 1)
print(dw.columns)
print(" ")

# Wind Direction:- Analysing missing values
print("Total Missing Values in Wind_Direction:", dw.Wind_Direction.isnull().sum())
print(" ")
dw_winddir_df = dw[dw['Wind_Speed'] == "Calm"]
print("Total Num of Rows where Wind_Speed is Calm:", len(dw_winddir_df['Wind_Speed']))
print("Unique values in Wind_Direction column where Wind_Direction is Calm:", dw_winddir_df['Wind_Direction'].unique())
print(" ")
# -- 21,349 rows are null out of total null 21,605 where wind speed is calm (Speed is less than 6 Kmph). 
# -- Let us analyse the rest rows.
# -- From above analysis we can see that Null values in Wind_Direction are getting effected by Wind_Speed.
# -- Let's investigate Wind_Speed more
print("Unique Values in Wind_Speed Col from full data:", dw.Wind_Speed.unique())
print(" ")
print(" ")
# -- checking rows with 'variable' mentioned in rows of Wind_Speed.
dw['Wind_Speed_Variability'] = dw['Wind_Speed'].apply(lambda x: 1 if "variable" in x.lower() else 0)
dw_winddir_df = dw[dw['Wind_Speed_Variability'] == 1]
print("Total Num of Rows where Wind_Speed_Variability is 1:", len(dw_winddir_df['Wind_Speed']))
print("Unique values in Wind_Direction column where Wind_Speed_Variability is 1:", dw_winddir_df['Wind_Direction'].unique())
print(" ")
# -- Above analysis shows the complete reason for missing data in Wind_Direction.
# -- If Wind_Speed was calm or varaiable speed was mentioned then Wind_Direction is not available.
dw['Wind_Speed_Calm'] = dw['Wind_Speed'].apply(lambda x: 1 if "calm" in x.lower() else 0)
print(dw['Wind_Speed_Calm'].sum())
print(" ")

# Cleaning Wind_Speed
# -- We will removing 'km/h', 'calm', 'variable at' and 'Wind Gust'.
# -- We have handled Calm and Variability above already by creating new columns.
dw.rename({'Wind_Speed': 'Wind_Speed_in_Kmph'}, axis=1, inplace=True)
dw['Wind_Speed_in_Kmph'] = dw['Wind_Speed_in_Kmph'].apply(lambda x: x.replace(' Km/h', '').replace('Variable at ', '').replace('Calm', '').replace(' Wind Gust', ''))
dw['Wind_Speed_in_Kmph'] = dw['Wind_Speed_in_Kmph'].apply(lambda x: x.replace(',', ''))
dw['Wind_Speed_in_Kmph'] = dw['Wind_Speed_in_Kmph'].apply(lambda x: x.replace(' 46 km/h', ''))
print("Unique Values in Wind_Speed_in_Kmph Col from full data:", dw.Wind_Speed_in_Kmph.unique())
print(" ")
print(" ")

# Cleaning Temperature, Relative_Temp, Dew_Point
dw.rename({'Temperature': 'Temperature_in_°C', 'Relative_Temp': 'Relative_Temp_in_°C', 'Dew_Point': 'Dew_Point_in_°C'}, axis=1, inplace=True)
dw['Temperature_in_°C'] = dw['Temperature_in_°C'].apply(lambda x: x.replace('°C', ''))
dw['Relative_Temp_in_°C'] = dw['Relative_Temp_in_°C'].apply(lambda x: x.replace('°C', ''))
dw['Dew_Point_in_°C'] = dw['Dew_Point_in_°C'].apply(lambda x: x.replace('°C', ''))

# Cleaning Wind_Direction
dw.rename({'Wind_Direction': 'Wind_Direction_degree'}, axis=1, inplace=True)
dw['Wind_Direction_degree'] = dw['Wind_Direction_degree'].apply(lambda x: str(x))
dw['Wind_Direction_degree'] = dw['Wind_Direction_degree'].apply(lambda x: x.replace('°', ''))
dw['Wind_Direction_degree'] = dw['Wind_Direction_degree'].apply(lambda x: x.replace('nan', ''))


# Cleaning Rel_Humidity
dw['Rel_Humidity'] = dw['Rel_Humidity'].apply(lambda x: x.replace('%', ''))
dw['Rel_Humidity'] = dw['Rel_Humidity'].apply(lambda x: int(x))
dw['Rel_Humidity'] = dw['Rel_Humidity']/100

# Cleaning Atmospheric_Pressure
dw.rename({'Atmospheric_Pressure': 'Atmospheric_Pressure_in_mb'}, axis=1, inplace=True)
dw['Atmospheric_Pressure_in_mb'] = dw['Atmospheric_Pressure_in_mb'].apply(lambda x: x.replace('mb', ''))

# Changing Data Types
print(dw.info())
print(" ")
dw['Date & Time'] = pd.to_datetime(dw['Date & Time'])
dw['Temperature_in_°C'] = pd.to_numeric(dw['Temperature_in_°C'])
dw['Relative_Temp_in_°C'] = pd.to_numeric(dw['Relative_Temp_in_°C'])
dw['Wind_Speed_in_Kmph'] = pd.to_numeric(dw['Wind_Speed_in_Kmph'])
dw['Wind_Direction_degree'] = pd.to_numeric(dw['Wind_Direction_degree'])
dw['Dew_Point_in_°C'] = pd.to_numeric(dw['Dew_Point_in_°C'])
dw['Atmospheric_Pressure_in_mb'] = pd.to_numeric(dw['Atmospheric_Pressure_in_mb'])
print(" ")

# Creating Dummy Variable of Description
print("Unique Variables of Description Col:", dw['Description'].unique())
# -- Changing 'Partly cloudy' to 'Partly Cloudie' as it can conflict with 'Cloudy'.
dw['Description'] = dw['Description'].apply(lambda x: x.replace('Partly cloudy', 'Partly cloudie'))
# -- There are 6 unique Description, We will create 5 Dummy Variables.
dw['Thunder'] = dw['Description'].apply(lambda x: 1 if "thunder" in x.lower() else 0)
dw['Few_clouds'] = dw['Description'].apply(lambda x: 1 if "few clouds" in x.lower() else 0)
dw['Rain'] = dw['Description'].apply(lambda x: 1 if "rain" in x.lower() else 0)
dw['Clear'] = dw['Description'].apply(lambda x: 1 if "clear" in x.lower() else 0)
dw['Cloudy'] = dw['Description'].apply(lambda x: 1 if "cloudy" in x.lower() else 0)

print(dw.info())

# Saving the clean out put
dw.to_csv('Delhi_Weather_DC-1.csv', index=False)
