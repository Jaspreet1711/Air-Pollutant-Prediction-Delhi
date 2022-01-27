# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 21:51:06 2021

@author: Jaspreet Singh
"""
import pandas as pd

tf_21 = pd.read_excel("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/1. Data Collection/Data Collected/Delhi_Traffic_Congestion_Data_2021.xlsx")

# Columns in data
print(tf_21.columns)
print(" ")

# Dropping first column
tf_21 = tf_21.drop('Unnamed: 0', 1)
print(tf_21.columns)
print(" ")

# checking missing data
tf_21_mv = tf_21.isnull().sum()
tf_21_mv = tf_21_mv .to_frame()
tf_21_mv .columns = ['#Missing_Values']
tf_21_mv .insert(loc=0, column='Column_Name', value=tf_21_mv .index)
tf_21_mv .reset_index(drop=True, inplace=True)
tf_21_mv ['%_MV-/-total'] =  (tf_21_mv ['#Missing_Values'] / len(tf_21['Date']))*100
print(tf_21_mv )
print(len(tf_21['Date']))
print(" ")

# Removing Missing Values
tf_21 = tf_21[tf_21['Avg Congestion'].notna()] 

tf_21_mv_1 = tf_21.isnull().sum()
tf_21_mv_1 = tf_21_mv_1 .to_frame()
tf_21_mv_1 .columns = ['#Missing_Values']
tf_21_mv_1 .insert(loc=0, column='Column_Name', value=tf_21_mv_1 .index)
tf_21_mv_1 .reset_index(drop=True, inplace=True)
tf_21_mv_1 ['%_MV-/-total'] =  (tf_21_mv_1 ['#Missing_Values'] / len(tf_21['Date']))*100
print(tf_21_mv_1 )
print(len(tf_21['Date']))
print(" ")

# Cleaning Avg Congestion 
tf_21['Avg Congestion'] = tf_21['Avg Congestion'].apply(lambda x: x.replace('%', ''))
tf_21['Avg Congestion'] = tf_21['Avg Congestion'].apply(lambda x: int(x))
tf_21['Avg Congestion'] = tf_21['Avg Congestion']/100

# Correcting Data Types
print(tf_21.info())
print(" ")
tf_21['Date'] = pd.to_datetime(tf_21['Date'])
print(tf_21.info())
print(" ")

# Saving the clean output
tf_21.to_csv('Traffic_Delhi_2021_DC-1.csv', index=False)