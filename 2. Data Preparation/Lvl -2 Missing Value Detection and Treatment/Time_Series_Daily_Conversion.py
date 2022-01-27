import pandas as pd
import numpy as np
from datetime import datetime
d = datetime.now()

# ------ Loading the AQI Time Series Dataset ------ #
aqi_ts = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -2 Missing Value Detection and Treatment/AQI_TS_Hourly.csv")

# ------ Cleaning the AQI Time Series Dataset ------ #
# Formating 'timestamp' to Datetime format
aqi_ts['timestamp'] = pd.to_datetime(aqi_ts['timestamp'])

# In 2016 PM2.5 is Not Calculated as time format was changed. At some timestamp PM2.5 is given 0 which is wrong.
aqi_ts_15_16 = aqi_ts[aqi_ts['timestamp'] <= '2016-08-03 05:30:00']
aqi_ts_16_21 = aqi_ts[aqi_ts['timestamp'] > '2016-08-03 05:30:00']

# -- Removing PM2.5 with 0 (Error) from aqi_ts_15_16
aqi_ts_pm25_0 = aqi_ts_15_16[aqi_ts_15_16['PM2.5'] == 0] # -- Just to check
aqi_ts_15_16 = aqi_ts_15_16[aqi_ts_15_16['PM2.5'] != 0]

# -- Joining both the datasets
aqi_df = pd.concat([aqi_ts_15_16, aqi_ts_16_21], axis=0)

# Missing values in aqi_df
print("MVs")
print(aqi_df.isnull().sum())
print(" ")

# Taking out Date from timestamp
aqi_df['timestamp'] = pd.to_datetime(aqi_df['timestamp'])
Date_Time = aqi_df['timestamp']
aqi_df['Date'] = [d.date() for d in Date_Time]

# Computing Missing Hours data Datewise (Date with less than 10 hours will not be considered in calculating Day Wise Average)
Missing_Time_Datewise = pd.pivot_table(aqi_df, 
                              values = 'timestamp', 
                              index = 'Date', 
                              aggfunc = {'timestamp':['count']})

# -- Sorting the columns and Dataframe structure.
Missing_Time_Datewise.columns.name = None               
Missing_Time_Datewise = Missing_Time_Datewise.reset_index()

aqi_df = aqi_df.merge(Missing_Time_Datewise, how = 'left', left_on = 'Date', right_on = 'Date')

aqi_df = aqi_df.rename({'count': 'Hours_Data_Avail_Count'}, axis=1)

# -- Droping Date Column
aqi_df = aqi_df.drop(['Date'], axis = 1)

# Droping Date with less than 8 hours of Data ("Hours_Data_Avail_Count") will be dropped
aqi_df = aqi_df[aqi_df['Hours_Data_Avail_Count'] >= 8]

# Missing values in aqi_df
print("MVs after removing dates with less hours of data")
print(aqi_df.isnull().sum())
print(" ")

# ------ Converting the AQI Time Series Hourly Dataset to Daily Dataset ------ #
# Taking out the Average of Data Day wise using our hourly Data ("Hours_Data_Avail_Count" will remain same in average).
aqi_df_daily = aqi_df.resample('d', on='timestamp').mean()
aqi_df_daily.index = pd.to_datetime(aqi_df_daily.index, format = '%d/%m/%Y').strftime('%d-%m-%Y')

# Dropping 'Hours_Data_Avail_Count' 
aqi_df_daily = aqi_df_daily.drop(['Hours_Data_Avail_Count'], axis = 1)

# Checking the Missing Values
print("MVs in AQI Daily DF")
print(aqi_df_daily.isnull().sum())
print(" ")

#### ------------------------------------------------------------------------------------------------------------------------------ ####
#### ------------------------------------------------------------------------------------------------------------------------------ ####

# ------ Visualising to see Auto Correlation ------ #
# Removing Null Values just for plotting Autocorrelation of PM2.5 and PM10
aqi_df_daily_n = aqi_df_daily.dropna()

pm25_autocorr = pd.plotting.autocorrelation_plot(aqi_df_daily_n['PM2.5'])
pm10_autocorr = pd.plotting.autocorrelation_plot(aqi_df_daily_n['PM10'])

########## ----------- ############################### ----------- ##########
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
########## ----------- ############################### ----------- ##########

# ------ Loading the Delhi Weather Time Series Dataset ------ #
weath_ts = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -2 Missing Value Detection and Treatment/Weather_TS_Hourly.csv")

# ------ Cleaning the Delhi Weather Time Series Dataset ------ #
weath_df = weath_ts[['Date & Time', 'Temperature_in_°C', 'Wind_Speed_in_Kmph', 'Rel_Humidity', 'Dew_Point_in_°C', 'Atmospheric_Pressure_in_mb']]
weath_df = weath_df.rename({'Date & Time': 'timestamp'}, axis=1)

# Removing Rows with Missing Values
weath_df = weath_df[weath_df['Temperature_in_°C'].notna()]

# Taking out Date from timestamp
weath_df['timestamp'] = pd.to_datetime(weath_df['timestamp'])
Date_Time_w = weath_df['timestamp']
weath_df['Date'] = [d.date() for d in Date_Time_w]

# Computing Missing Hours data Datewise (Date with less than 10 hours will not be considered in calculating Day Wise Average)
Missing_Time_Datewise_w = pd.pivot_table(weath_df, 
                              values = 'timestamp', 
                              index = 'Date', 
                              aggfunc = {'timestamp':['count']})

# -- Sorting the columns and Dataframe structure.
Missing_Time_Datewise_w.columns.name = None               
Missing_Time_Datewise_w = Missing_Time_Datewise_w.reset_index()

weath_df = weath_df.merge(Missing_Time_Datewise_w, how = 'left', left_on = 'Date', right_on = 'Date')

weath_df = weath_df.rename({'count': 'Hours_Data_Avail_Count'}, axis=1)

# -- Droping Date Column
weath_df = weath_df.drop(['Date'], axis = 1)

# Weather Data is Recorded in every 30 mins so we can have maximum 48 Records in a day.
# Droping Date with less than 15 Half-Hours of Data ("Hours_Data_Avail_Count") will be dropped
weath_df = weath_df[weath_df['Hours_Data_Avail_Count'] >= 15]

# Missing values in weath_df
print("MVs after removing dates with less hours of data")
print(weath_df.isnull().sum())
print(" ")

# ------ Converting the Delhi Weather Time Series Hourly Dataset to Daily Dataset ------ #
# Taking out the Average of Data Day wise using our hourly Data ("Hours_Data_Avail_Count" will remain same in average).
weath_df_daily = weath_df.resample('d', on='timestamp').mean()
weath_df_daily.index = pd.to_datetime(weath_df_daily.index, format = '%d/%m/%Y').strftime('%d-%m-%Y')

# Dropping 'Hours_Data_Avail_Count' 
weath_df_daily = weath_df_daily.drop(['Hours_Data_Avail_Count'], axis = 1)

# Checking the Missing Values
print("MVs in Weather Daily DF")
print(weath_df_daily.isnull().sum())
print(" ")

########## ----------- ############################### ----------- ##########
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
########## ----------- ############################### ----------- ##########

# ------ Joining AQI Daily Average Data with Weather Daily Average ------ #
aqi_weath_daily_comb = aqi_df_daily.merge(weath_df_daily, how = 'left', left_on = 'timestamp', right_on = 'timestamp')
aqi_weath_daily_comb.index = pd.to_datetime(aqi_weath_daily_comb.index, dayfirst = True)

# Checking the Missing Values
print("MVs in Combined Daily DF")
print(aqi_weath_daily_comb.isnull().sum())
print(" ")

########## ----------- ############################### ----------- ##########
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
########## ----------- ############################### ----------- ##########

# ------ Treating Missing Values ------ #
# Imputing Next year(s) values from 2015 to 2019 and Previous Year(2) Values from 2020 to 2021
# There are some missing values in consective year same date we will those value with 2 year back data.
# Increasing Index (timestamp) by 1 year with data at same position (aqi_weath_daily_comb). (2015 data will become 2016 and so on).
comb_cols = aqi_weath_daily_comb.columns.values.tolist()

# -- 1 year plus minus data for imputation
# -- Minus 1 Year (n1) # --- These values will be imputed in 2015, 2016, 2017, 2018 and 2019 (This Data contains 1 year ahead values against the timestamp) # for example values in year 2022 is actually of 2021.
aqi_weath_daily_comb_n1 = pd.DataFrame()

for col in comb_cols:
    col_name = str(col+'_n1')    
    aqi_weath_daily_comb_n1[col_name] = aqi_weath_daily_comb[col] 
    
aqi_weath_daily_comb_n1.index = aqi_weath_daily_comb.index - pd.offsets.DateOffset(years = 1)
aqi_weath_daily_comb_n1 = aqi_weath_daily_comb_n1[aqi_weath_daily_comb_n1.index < '2020-01-01 00:00:00' ]

# -- Plus 1 Year (p1)  # --- These values will be imputed in 2020 and 2021 (This Data contains 1 year back values against the timestamp) # for example values in year 2018 is actually of 2017.
aqi_weath_daily_comb_p1 = pd.DataFrame()

for col in comb_cols:
    col_name = str(col+'_p1')    
    aqi_weath_daily_comb_p1[col_name] = aqi_weath_daily_comb[col] 

    
aqi_weath_daily_comb_p1.index = aqi_weath_daily_comb.index + pd.offsets.DateOffset(years = 1)
aqi_weath_daily_comb_p1 = aqi_weath_daily_comb_p1[aqi_weath_daily_comb_p1.index >= '2020-01-01 00:00:00' ]


#### ------------------------------------------------------------------------------------------------------------------------------ ####
### --- if 1 year plus or minus is also null it will impute with null values only. So we will create data with plus minus years. --- ### 
#### ------------------------------------------------------------------------------------------------------------------------------ ####


# -- 2 year plus minus data for imputation
# -- Minus 2 Year (n1) # --- These values will be imputed in 2015, 2016, 2017, 2018 and 2019 (This Data contains 2 years ahead values against the timestamp) # for example values in year 2016 is actually of 2018. 
aqi_weath_daily_comb_n2 = pd.DataFrame()

for col in comb_cols:
    col_name = str(col+'_n2')    
    aqi_weath_daily_comb_n2[col_name] = aqi_weath_daily_comb[col] 
    
aqi_weath_daily_comb_n2.index = aqi_weath_daily_comb.index - pd.offsets.DateOffset(years = 2)
aqi_weath_daily_comb_n2 = aqi_weath_daily_comb_n2[aqi_weath_daily_comb_n2.index < '2020-01-01 00:00:00' ]

# -- Plus 2 Year (p2)  # --- These values will be imputed in 2020 and 2021 (This Data contains 2 years back values against the timestamp) # for example values in year 2018 is actually of 2016. 
aqi_weath_daily_comb_p2 = pd.DataFrame()


for col in comb_cols:
    col_name = str(col+'_p2')    
    aqi_weath_daily_comb_p2[col_name] = aqi_weath_daily_comb[col] 

    
aqi_weath_daily_comb_p2.index = aqi_weath_daily_comb.index + pd.offsets.DateOffset(years = 2)
aqi_weath_daily_comb_p2 = aqi_weath_daily_comb_p2[aqi_weath_daily_comb_p2.index >= '2020-01-01 00:00:00' ]

#### ------------------------------------------------------------------------------------------------------------------------------ ####
#### ------------------------------------------------------------------------------------------------------------------------------ ####

# -- We will left inner join the new tables to aqi_weath_daily_comb (I will rename this Merged df as 'aqi_weath_daily_comb_clean0') 
aqi_weath_daily_comb_clean0 = aqi_weath_daily_comb.merge(aqi_weath_daily_comb_n1, how = 'left', left_index=True, right_index=True)
aqi_weath_daily_comb_clean0 = aqi_weath_daily_comb_clean0.merge(aqi_weath_daily_comb_p1, how = 'left', left_index=True, right_index=True)
aqi_weath_daily_comb_clean0 = aqi_weath_daily_comb_clean0.merge(aqi_weath_daily_comb_n2, how = 'left', left_index=True, right_index=True)
aqi_weath_daily_comb_clean0 = aqi_weath_daily_comb_clean0.merge(aqi_weath_daily_comb_p2, how = 'left', left_index=True, right_index=True)

aqi_weath_daily_comb_clean0 = aqi_weath_daily_comb_clean0.replace(np.nan, 'NA')

# -- Making the functions for imputation using n1, p1, n2, p2 Data.
def impute_n1(r, col):
    if r[col] == 'NA':
        col_name = str(col+'_n1')
        return r[col_name]
    else:
        return r[col]
    
def impute_p1(r, col):
    if r[col] == 'NA':
        col_name = str(col+'_p1')
        return r[col_name]
    else:
        return r[col]

def impute_n2(r, col):
    if r[col] == 'NA':
        col_name = str(col+'_n2')
        return r[col_name]
    else:
        return r[col]
    
def impute_p2(r, col):
    if r[col] == 'NA':
        col_name = str(col+'_p2')
        return r[col_name]
    else:
        return r[col]            

# -- Performing all the functions for all the columns in sequence of n1, p1, n2, p2. (Year 1 is given higher priority than Year 2 gap imputation).    
for col in comb_cols:
    aqi_weath_daily_comb_clean0[col] = aqi_weath_daily_comb_clean0.apply(lambda x: impute_n1(x, col), axis = 1)
    aqi_weath_daily_comb_clean0[col] = aqi_weath_daily_comb_clean0.apply(lambda x: impute_p1(x, col), axis = 1)
    aqi_weath_daily_comb_clean0[col] = aqi_weath_daily_comb_clean0.apply(lambda x: impute_n2(x, col), axis = 1)
    aqi_weath_daily_comb_clean0[col] = aqi_weath_daily_comb_clean0.apply(lambda x: impute_p2(x, col), axis = 1)
    
aqi_weath_daily_comb_clean0 = aqi_weath_daily_comb_clean0.replace('NA', np.nan)

AQI_TS_Clean_DF_1 = aqi_weath_daily_comb_clean0[comb_cols]

# Checking the Missing Values
print("MVs After Missing Treatment (using n1, p1, n2 and p2)")
print(AQI_TS_Clean_DF_1.isnull().sum())
print(" ")    

# Now there are very few Missing Values left. We will use interpolate (linear method) function for imputation of those values
AQI_TS_Clean_DF = AQI_TS_Clean_DF_1.interpolate(method ='linear', limit_direction ='forward')

# Checking the Missing Values
print("Final MVs After Last Missing Treatment (using interpolate)")
print(AQI_TS_Clean_DF.isnull().sum())
print(" ")  

# Downloading CSV Missing Values are there.
AQI_TS_Clean_DF.to_csv("AQI_TS_Daily.csv")