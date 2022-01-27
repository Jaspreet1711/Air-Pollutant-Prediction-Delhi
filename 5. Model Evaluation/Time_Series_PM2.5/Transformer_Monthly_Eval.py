import pandas as pd
import numpy as np
import pickle

pickle_transformer_mon = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/4. Modeling/Time_Series/TransformerModel_AQI_TS_Monthly.pkl", "rb")
model_transformer_mon = pickle.load(pickle_transformer_mon)

# loading the Data Set
aqi_ts_train_scaled = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/Time_Series/aqi_ts_train.csv", index_col = 'timestamp')
aqi_ts_test = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/Time_Series/aqi_ts_test_before_scaling.csv", index_col = 'timestamp')

# -- Converting the timestamp columns into datetime format
aqi_ts_train_scaled.index = pd.to_datetime(aqi_ts_train_scaled.index)
aqi_ts_test.index = pd.to_datetime(aqi_ts_test.index)

# -- Reseting the index
aqi_ts_train_scaled.reset_index(inplace = True)
aqi_ts_test.reset_index(inplace = True)

# -- Removing Duplicates from Datasets
aqi_ts_train_scaled = aqi_ts_train_scaled.drop_duplicates(subset = 'timestamp', keep='last')
aqi_ts_test = aqi_ts_test.drop_duplicates(subset = 'timestamp', keep='last')

# Converting Data into Monthly for Better Accuracy
aqi_ts_train_scaled = aqi_ts_train_scaled.resample('M', on='timestamp').mean()
aqi_ts_test = aqi_ts_test.resample('M', on='timestamp').mean()

# -- Reseting the index
aqi_ts_train_scaled.reset_index(inplace = True)
aqi_ts_test.reset_index(inplace = True)

# -- Modifying the Datasets into Series for Modeling
from darts import TimeSeries

series_train_pm25 = TimeSeries.from_dataframe(aqi_ts_train_scaled, 'timestamp', 'PM2.5')

# Predicting Values using the Model (Converting Darts.TimeSeries Type to Pandas Dataframe)
prediction_pm25 = model_transformer_mon.predict(n = 36, series = series_train_pm25)
prediction_pm25_df = prediction_pm25.pd_dataframe()
prediction_pm25_df.reset_index(inplace = True)

# Merging Forecasted Values with Orginal to do a backtest.
aqi_ts_test['PM2.5_og'] = aqi_ts_test['PM2.5']
aqi_ts_test = aqi_ts_test[['timestamp', 'PM2.5_og']]
prediction_test_df = aqi_ts_test.merge(prediction_pm25_df, how = 'left', left_on = 'timestamp', right_on = 'time')
prediction_test_df['PM2.5_pred_scaled'] = prediction_test_df['PM2.5']
prediction_test_df = prediction_test_df[['timestamp', 'PM2.5_og', 'PM2.5_pred_scaled']]
prediction_test_df = prediction_test_df.dropna()

# Converting PM2.5 Pred scaled values into orignal values
scaler_ts_pm25 = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/Time_Series/Scaler_TS_pm25.pkl", "rb")
scaler_ts_pm10 = open("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -3 Train_Test_Split and Data Scaling/Time_Series/Scaler_TS_pm10.pkl", "rb")
scaler_pm25 = pickle.load(scaler_ts_pm25)
scaler_pm10 = pickle.load(scaler_ts_pm10)

pred_pm25_scaled = prediction_test_df['PM2.5_pred_scaled'].to_frame()
pred_pm25_og = scaler_pm25.inverse_transform(pred_pm25_scaled).tolist()
ls = []
for ls_item in pred_pm25_og:
    for item in ls_item:
        ls.append(item)
        
pred_pm25_og = ls

prediction_test_df['PM2.5_pred'] = pred_pm25_og
prediction_test_df['Error_in_%'] = prediction_test_df.apply(lambda x: np.round(((x['PM2.5_og'] - x['PM2.5_pred'])/x['PM2.5_og'])*100, 1), axis = 1) 

# -- Rearranging Columns for better view
prediction_test_df = prediction_test_df[['timestamp', 'PM2.5_og', 'PM2.5_pred', 'Error_in_%', 'PM2.5_pred_scaled']]

prediction_test_df.to_csv("TransformerModel_Backtest_Results_Monthly.csv")