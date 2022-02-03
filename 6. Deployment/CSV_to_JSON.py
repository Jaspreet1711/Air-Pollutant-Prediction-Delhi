import pandas as pd
aqi_ts = pd.read_csv('C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/2. Data Preparation/Lvl -2 Missing Value Detection and Treatment/AQI_TS_Daily.csv')
aqi_ts_2 = pd.read_csv('AQI_TS_Daily_2.csv')
aqi_df = pd.concat([aqi_ts, aqi_ts_2], axis=0)

aqi_df = aqi_df.rename({'PM2.5': 'PM2-5', 'Temperature_in_°C': 'Temperature_in_cel', 'Dew_Point_in_°C': 'Dew_Point_in_cel'}, axis=1)

# -- Removing Duplicates from Datasets
aqi_df = aqi_df.drop_duplicates(subset = 'timestamp', keep='last')

# -- This file in CSV with no duplicates
aqi_df.to_csv("AQI_Daily_TS.csv", index = False)

# --------------------------------------------------------------------------------------------------------- #
# I have taken the following code from GeeksforGeeks (https://www.geeksforgeeks.org/convert-csv-to-json-using-python/)

import csv
import json


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['timestamp']
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='UTF-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))


# Driver Code

# Decide the two file paths according to your
# computer system
csvFilePath = r'AQI_Daily_TS.csv'
jsonFilePath = r'AQI_TS_Daily.json'

# Call the make_json function
make_json(csvFilePath, jsonFilePath)

