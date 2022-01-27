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

series_train_pm25 = TimeSeries.from_dataframe(aqi_ts_train, 'timestamp', 'PM2.5')
series_test_pm25 = TimeSeries.from_dataframe(aqi_ts_test, 'timestamp', 'PM2.5')
series_comb_pm25 = TimeSeries.from_dataframe(aqi_ts_comb, 'timestamp', 'PM2.5')

series_train_pm10 = TimeSeries.from_dataframe(aqi_ts_train, 'timestamp', 'PM10')
series_test_pm10 = TimeSeries.from_dataframe(aqi_ts_test, 'timestamp', 'PM10')
series_comb_pm10 = TimeSeries.from_dataframe(aqi_ts_comb, 'timestamp', 'PM10')

series_train_ws = TimeSeries.from_dataframe(aqi_ts_train, 'timestamp', 'Wind_Speed_in_Kmph')
series_test_ws = TimeSeries.from_dataframe(aqi_ts_test, 'timestamp', 'Wind_Speed_in_Kmph')
series_comb_ws = TimeSeries.from_dataframe(aqi_ts_comb, 'timestamp', 'Wind_Speed_in_Kmph')

series_train_tmp = TimeSeries.from_dataframe(aqi_ts_train, 'timestamp', 'Temperature_in_°C')
series_test_tmp = TimeSeries.from_dataframe(aqi_ts_test, 'timestamp', 'Temperature_in_°C')
series_comb_tmp = TimeSeries.from_dataframe(aqi_ts_comb, 'timestamp', 'Temperature_in_°C')

series_train_hum = TimeSeries.from_dataframe(aqi_ts_train, 'timestamp', 'Rel_Humidity')
series_test_hum = TimeSeries.from_dataframe(aqi_ts_test, 'timestamp', 'Rel_Humidity')
series_comb_hum = TimeSeries.from_dataframe(aqi_ts_comb, 'timestamp', 'Rel_Humidity')

series_train_ap = TimeSeries.from_dataframe(aqi_ts_train, 'timestamp', 'Atmospheric_Pressure_in_mb')
series_test_ap = TimeSeries.from_dataframe(aqi_ts_test, 'timestamp', 'Atmospheric_Pressure_in_mb')
series_comb_ap = TimeSeries.from_dataframe(aqi_ts_comb, 'timestamp', 'Atmospheric_Pressure_in_mb')

# -- Using Darts Module for TimeSeries Forecasting
from darts.models import NBEATSModel

model = NBEATSModel(input_chunk_length = 12, output_chunk_length = 6, n_epochs = 100, random_state = 10)
model.fit([series_comb_pm25, series_comb_pm10, series_comb_ws, series_comb_tmp, series_comb_hum, series_comb_ap], verbose = True)
prediction_pm25 = model.predict(n = 24, series = series_train_pm25)

series_comb_pm25.plot()
prediction_pm25.plot(label='forecast for PM2.5', low_quantile=0.05, high_quantile=0.95)
plt.legend()
plt.show()