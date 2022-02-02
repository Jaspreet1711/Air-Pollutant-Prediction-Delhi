# -*- coding: utf-8 -*-
"""
Created on Mon Jan 31 16:22:08 2022

@author: Jaspreet Singh
"""
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import pyrebase

# Loading Scaler Pickle
pickle_scaler = open("Scaler.pkl", "rb")
scaler = pickle.load(pickle_scaler)

# Set the configuration for your app
config = {
    "apiKey": "AIzaSyCJj5yJgV2QdpkBxZN8QNvaZQiWh-TjntA",
    "authDomain": "aqi-prediction-338709.firebaseapp.com",
    "databaseURL": "https://aqi-prediction-338709-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "aqi-prediction-338709",
    "storageBucket": "aqi-prediction-338709.appspot.com",
    "messagingSenderId": "1068395558929",
    "appId": "1:1068395558929:web:089594c34c4f8f523119b0",
    "measurementId": "G-B1PN8WHJMG"
}
firebase = pyrebase.initialize_app(config)

# Get a reference to the database service
db = firebase.database()

# Retrieving data from Firebase DB
AQI_Daily_TS_pyre = db.get()
AQI_Daily_TS_Dict = AQI_Daily_TS_pyre.val()

# Transforming the Data from OrderedDict to DataFrame
Columns = ['timestamp', 'PM2-5', 'PM10', 'NO2', 'SO2', 'CO', 'Temperature_in_cel', 'Wind_Speed_in_Kmph', 'Rel_Humidity',
           'Dew_Point_in_cel', 'Atmospheric_Pressure_in_mb']
AQI_Daily_TS_DF = pd.DataFrame(AQI_Daily_TS_Dict, columns=AQI_Daily_TS_Dict.keys()).transpose()[Columns]
AQI_Daily_TS_DF.reset_index(inplace=True, drop=True)

# Data Formating and Managing Missing Values (Which will be very less)
AQI_Daily_TS_DF['timestamp'] = pd.to_datetime(AQI_Daily_TS_DF['timestamp'])

# -- 1 year minus data for imputation
# -- Plus 1 Year (p1)  # for example values in year 2018 is actually of 2017.
AQI_Daily_TS_DF_p1 = pd.DataFrame()

for col in Columns:
    if col != 'timestamp':
        col_name = str(col + '_p1')
        AQI_Daily_TS_DF_p1[col_name] = AQI_Daily_TS_DF[col]
    else:
        AQI_Daily_TS_DF_p1[col] = AQI_Daily_TS_DF[col]

AQI_Daily_TS_DF_p1['timestamp'] = AQI_Daily_TS_DF_p1['timestamp'] + pd.offsets.DateOffset(years=1)

# -- 2 year minus data for imputation
# -- Plus 2 Year (p2)  # for example values in year 2018 is actually of 2016.
AQI_Daily_TS_DF_p2 = pd.DataFrame()

for col in Columns:
    if col != 'timestamp':
        col_name = str(col + '_p2')
        AQI_Daily_TS_DF_p2[col_name] = AQI_Daily_TS_DF[col]
    else:
        AQI_Daily_TS_DF_p2[col] = AQI_Daily_TS_DF[col]

AQI_Daily_TS_DF_p2['timestamp'] = AQI_Daily_TS_DF_p2['timestamp'] + pd.offsets.DateOffset(years=2)

# -- We will left inner join the new tables to aqi_weath_daily_comb (I will rename this Merged df as 'aqi_weath_daily_comb_clean0')
AQI_Daily_TS_DF_clean = AQI_Daily_TS_DF.merge(AQI_Daily_TS_DF_p1, how='left', left_on='timestamp', right_on='timestamp')
AQI_Daily_TS_DF_clean = AQI_Daily_TS_DF_clean.merge(AQI_Daily_TS_DF_p2, how='left', left_on='timestamp', right_on='timestamp')


# -- Making the functions for imputation using n1 and n2 Data.
def impute_p1(r, col):
    if r[col] == 'nan':
        col_name = str(col + '_p1')
        return r[col_name]
    else:
        return r[col]


def impute_p2(r, col):
    if r[col] == 'nan':
        col_name = str(col + '_p2')
        return r[col_name]
    else:
        return r[col]


for col in Columns:
    if col != 'timestamp':
        # -- We are replace 'nan' values with previous year values.
        AQI_Daily_TS_DF_clean[col] = AQI_Daily_TS_DF_clean.apply(lambda x: impute_p1(x, col), axis=1)
        AQI_Daily_TS_DF_clean[col] = AQI_Daily_TS_DF_clean.apply(lambda x: impute_p2(x, col), axis=1)
        # -- After MVs Treatment. We are formating the data.
        AQI_Daily_TS_DF_clean[col] = pd.to_numeric(AQI_Daily_TS_DF_clean[col])
        AQI_Daily_TS_DF_clean[col] = AQI_Daily_TS_DF_clean[col].interpolate(method='linear', limit_direction='forward')
    else:
        AQI_Daily_TS_DF_clean[col] = pd.to_datetime(AQI_Daily_TS_DF_clean[col])

AQI_Daily_TS = AQI_Daily_TS_DF_clean[Columns]
AQI_Daily_TS = AQI_Daily_TS.drop_duplicates(subset='timestamp', keep='last')
print(AQI_Daily_TS.isnull().sum())

def month_year(r):
    year = r.year
    mon = r.month
    if mon < 10:
        mon = str(0) + str(r.month)
    else:
        pass
    mon_yr = str(mon) + '/' + str(year)
    return mon_yr


AQI_Daily_TS['month_year'] = AQI_Daily_TS['timestamp'].apply(lambda x: month_year(x))

# I am making a dataframe that will give number of days we have for a particular month and year
total_days_in_month = pd.pivot_table(AQI_Daily_TS,
                                     values='timestamp',
                                     index='month_year',
                                     aggfunc={'month_year': ['count']})

AQI_Daily_TS = AQI_Daily_TS.merge(total_days_in_month, how='left', left_on='month_year', right_on='month_year')

# It will consider current month for training after 25th of that month
AQI_Daily_TS = AQI_Daily_TS[AQI_Daily_TS['count'] > 24]
AQI_Daily_TS = AQI_Daily_TS.drop(['month_year', 'count'], 1)

# Converting Data into Monthly for Better Accuracy
AQI_Daily_TS = AQI_Daily_TS.resample('M', on='timestamp').mean()

# -- Renaming the columns
AQI_Daily_TS = AQI_Daily_TS.rename({'PM2-5':'PM2.5', 'Dew_Point_in_cel':'Dew_Point_in_°C', 'Temperature_in_cel':'Temperature_in_°C'}, axis=1)

# Scaling the Data.
AQI_Daily_TS_1 = scaler.transform(AQI_Daily_TS)

AQI_Daily_TS = pd.DataFrame(data = AQI_Daily_TS_1, columns = AQI_Daily_TS.columns, index = AQI_Daily_TS.index)

# -- Reseting the index
AQI_Daily_TS.reset_index(inplace = True)

# -- Modifying the Datasets into Series for Modeling
from darts import TimeSeries

series_train_pm25 = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'PM2.5')

series_train_pm10 = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'PM10')

series_train_ws = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'Wind_Speed_in_Kmph')

series_train_tmp = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'Temperature_in_°C')

series_train_hum = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'Rel_Humidity')

series_train_ap = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'Atmospheric_Pressure_in_mb')

series_train_co = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'CO')

series_train_no2 = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'NO2')

series_train_so2 = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'SO2')

series_train_dp = TimeSeries.from_dataframe(AQI_Daily_TS, 'timestamp', 'Dew_Point_in_°C')

# -- Using Darts Module for TimeSeries Forecasting
from darts.models import TransformerModel

model_transformer_mon = TransformerModel(input_chunk_length = 12, output_chunk_length = 6, n_epochs = 100, random_state = 10)

Input_Ls = [series_train_pm25, series_train_pm10, series_train_ws, series_train_tmp, series_train_hum, series_train_ap, series_train_co, series_train_no2, series_train_dp]

model_transformer_mon.fit(Input_Ls, verbose = True)
prediction_pm25 = model_transformer_mon.predict(n = 24, series = series_train_pm25)

# converting the model into pickle
import pickle
file = open('TransformerModel_AQI_TS_Monthly.pkl', 'wb')
pickle.dump(model_transformer_mon, file)

file = open('Prediction_Transformer_AQI_Monthly.pkl', 'wb')
pickle.dump(prediction_pm25, file)

# Visualizing Predicted values on Graph
series_train_pm25.plot()
prediction_pm25.plot(label='forecast for PM2.5', low_quantile=0.05, high_quantile=0.95)
plt.legend()
plt.show()