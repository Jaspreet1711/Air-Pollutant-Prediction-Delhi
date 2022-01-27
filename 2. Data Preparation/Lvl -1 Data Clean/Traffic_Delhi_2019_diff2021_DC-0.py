# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 12:24:42 2021

@author: Jaspreet Singh
"""

import pandas as pd

tf_19 = pd.read_excel("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/1. Data Collection/Data Collected/Delhi_Traffic_Congestion_Data_2019_daily_diff-from-21.xlsx")

# Columns in data
print(tf_19.columns)
print(" ")

# Dropping first column
tf_19 = tf_19.drop('Unnamed: 0', 1)
print(tf_19.columns)
print(" ")

# checking missing data
tf_19_mv = tf_19.isnull().sum()
tf_19_mv = tf_19_mv .to_frame()
tf_19_mv .columns = ['#Missing_Values']
tf_19_mv .insert(loc=0, column='Column_Name', value=tf_19_mv .index)
tf_19_mv .reset_index(drop=True, inplace=True)
tf_19_mv ['%_MV-/-total'] =  (tf_19_mv ['#Missing_Values'] / len(tf_19['Date']))*100
print(tf_19_mv )
print(len(tf_19['Date']))
print(" ")

# Correcting Data Types
print(tf_19.info())
print(" ")
tf_19['Date'] = pd.to_datetime(tf_19['Date'])
print(tf_19.info())
print(" ")

# Saving the clean output
tf_19.to_csv('Traffic_Delhi_2019_diff2021_DC-0.csv', index=False)
