# Setting the Base Environment
import pandas as pd
import matplotlib.pyplot as plt

# loading the Data Set
aqi_ts_train = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/Time_Series/aqi_ts_train.csv", index_col = 'timestamp')
aqi_ts_test = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/Time_Series/aqi_ts_test.csv", index_col = 'timestamp')

# -- Converting the timestamp columns into datetime format
aqi_ts_train.index = pd.to_datetime(aqi_ts_train.index)
aqi_ts_test.index = pd.to_datetime(aqi_ts_test.index)

# -- Joining both the datasets
aqi_ts_comb = pd.concat([aqi_ts_train, aqi_ts_test], axis=0)

# -- Reseting the index 
aqi_ts_train.reset_index(inplace = True)
aqi_ts_test.reset_index(inplace = True)
aqi_ts_comb.reset_index(inplace = True)

# -- Removing Duplicates from Datasets
aqi_ts_train = aqi_ts_train.drop_duplicates(subset = 'timestamp', keep='last')
aqi_ts_test = aqi_ts_test.drop_duplicates(subset = 'timestamp', keep='last')
aqi_ts_comb = aqi_ts_comb.drop_duplicates(subset = 'timestamp', keep='last')

# Converting Data into Monthly for Better Accuracy
aqi_ts_train = aqi_ts_train.resample('M', on='timestamp').mean()
aqi_ts_test = aqi_ts_test.resample('M', on='timestamp').mean()
aqi_ts_comb = aqi_ts_comb.resample('M', on='timestamp').mean()

# -- Reseting the index
aqi_ts_train.reset_index(inplace = True)
aqi_ts_test.reset_index(inplace = True)
aqi_ts_comb.reset_index(inplace = True)

# -- Modifying the Datasets into Series for Modeling
from darts import TimeSeries

series_train = TimeSeries.from_dataframe(aqi_ts_train, 'timestamp', 'PM2.5')
series_test = TimeSeries.from_dataframe(aqi_ts_test, 'timestamp', 'PM2.5')
series_comb = TimeSeries.from_dataframe(aqi_ts_comb, 'timestamp', 'PM2.5')

# -- Using Darts Module for TimeSeries Forecasting
from darts.models import ARIMA

model = ARIMA()
model.fit(series_train)
prediction = model.predict(len(series_test), num_samples=1000)

series_comb.plot()
prediction.plot(label='forecast', low_quantile=0.05, high_quantile=0.95)
plt.legend()
plt.show()








































