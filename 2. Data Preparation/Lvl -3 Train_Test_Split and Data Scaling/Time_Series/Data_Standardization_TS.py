import pandas as pd

aqi_ts_daily = pd.read_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -2 Missing Value Detection and Treatment/AQI_TS_Daily.csv", index_col = 'timestamp')

# Formating 'timestamp' to Datetime format
aqi_ts_daily.index = pd.to_datetime(aqi_ts_daily.index)

# Splitting Data into Train and Test then performing scaling
# Import the modules
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # --- Z Score Method
# -- Zscore Standardization Dataset
scaler = StandardScaler()

# ------------------------------------------------------------------------------- #

aqi_ts_train, aqi_ts_test = train_test_split(aqi_ts_daily, test_size = 0.2, shuffle = False)

# Downloading before Scaling Datasets
aqi_ts_train.to_csv("aqi_ts_train_before_scaling.csv")
aqi_ts_test.to_csv("aqi_ts_test_before_scaling.csv")

### Feature Scaling ###

# Fit the model for X
scaler.fit(aqi_ts_train)

# Transforming the both train and test based on train dataset fit.
aqi_ts_train_1 = scaler.transform(aqi_ts_train)
aqi_ts_test_1 = scaler.transform(aqi_ts_test)

aqi_ts_train = pd.DataFrame(data = aqi_ts_train_1, columns = aqi_ts_train.columns, index = aqi_ts_train.index)
aqi_ts_test = pd.DataFrame(data = aqi_ts_test_1, columns = aqi_ts_test.columns, index = aqi_ts_test.index)

# Downloading Scaled Datasets
aqi_ts_train.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/Time_Series/aqi_ts_train.csv")
aqi_ts_test.to_csv("C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -5 Final Data/Time_Series/aqi_ts_test.csv")

# Making Separate scaler for PM2.5 and PM10
aqi_train_og = pd.read_csv("aqi_ts_train_before_scaling.csv")

import pickle
aqi_pm25_1, aqi_pm10_1 = aqi_train_og['PM2.5'].to_frame(), aqi_train_og['PM10'].to_frame() 

# -- converting the scaler into pickle -- for PM2.5
scaler.fit(aqi_pm25_1)
aqi_pm25 = scaler.transform(aqi_pm25_1)
file = open('Scaler_TS_pm25.pkl', 'wb')
pickle.dump(scaler, file)


# -- converting the scaler into pickle -- for PM10
scaler.fit(aqi_pm10_1)
aqi_pm10 = scaler.transform(aqi_pm10_1)
file = open('Scaler_TS_pm10.pkl', 'wb')
pickle.dump(scaler, file)


