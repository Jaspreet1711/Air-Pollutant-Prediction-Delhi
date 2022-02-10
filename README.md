# Air-Pollutants-Forecasting-&-Prediction-Delhi
Brief: Time Series Forecasting and Cross Section Prediction of PM2.5 and PM10 in Delhi

![This Image Represents time series forecating backtesting using a deep learning model](https://github.com/Jaspreet1711/Air-Pollutant-Prediction-Delhi/blob/main/5.%20Model%20Evaluation/Time_Series_PM2.5/TransdormerModel_Results_Monthly_Viz.png)


## Index:-

I. Problem Statement

II. Data Science Problem

III. Data Collection

IV. Data Preparation

V. Exploratory Data Analysis

VI. Modeling

VII. Model Evaluation

VIII. Deployment

IX. Maintenance and Improvements


## I. Problem Statement
Delhi is struggling with pollution and bad air quality from past many years. People with respiratory issues face many health problems. If we are able to forecast and predict pollution level government and patients can take precautionary measures early. PM2.5 and PM10 are major pollutants present that are hazardous to health.

## II. Data Science Problem
Data science can help in Forecasting of PM2.5 but no structured time series data is available for Delhi. Weather condition play crucial role in pollution level but again no structured data is available. To Forecast with accuracy we need good quality data in regular time series and need to understand multiple factors (features) impacting PM2.5 (Lable-1) and PM10 (lable-2). To understand label independency on features we can do a cross section analysis by using statistical techniques and machine learning.   

## III. Data Collection

### A. Air Quality Index (AQI) Data collection
   
The Central Pollution Control Board (CPCB), statutory organisation, was constituted in September, 1974 under the Water (Prevention and Control of Pollution) Act, 1974. Further, CPCB was entrusted with the powers and functions under the Air (Prevention and Control of Pollution) Act, 1981. CPCB Monitors hourly AQI data and also collects data from state owned stations like DPCC (Delhi Pollution Control Committee). 

CPCB's Web app shows hourly pollutant level data day wise for every station present in India in the form of bar charts. Web Scraping with Selenium can help in extracting data as we need to crawl through various pages and Pollutant numbers are covered under heavy HTML Tags. Selenium can easily parse HTML and crawl on different pages. We will extract data in rectangle format.
   
   Day wise AQI Level for every hour at different DPCC Stations of Delhi.   
   Technique: Web Scraping (Using Selenium in Python)
   Source: https://app.cpcbccr.com/AQI_India/
       
       Features: -> Diff Pollutants - (Like PM 10, 2.5, CO, 
                                                      NO2, NNH3, Ozone, 
                                                      SO2)
                      -> Every Hour (From 12:30 AM to 11:30 PM), 
                      -> Avg, Min, Max, 
                      -> Prominent Pollutant
                       
       Stations for collection:                                     
       1. Punjabi Bagh, Delhi - DPCC -  1st June 2015
       2. Anand Vihar, Delhi - DPCC  -  1st Nov  2017
       
       Output Dataframe Format: .xlsx
      
  
### B. Weather Data collection

Delhi's historical weather data for every half and hour was available at freemeteo website. Website's HTML was comparatively simple than later web app as data was presented in Table Format on Web Page but Ads were the problem which were popping randomly while crawling. Again I used Selenium to extract data from the web page. "If-else" and "try-except" conditions were used at every step to tackle the ad issue. If ad came selenium's cursor will find close button, click it and resume the collection and crawling. 

   Day Wise Every half and hour Weather Report for particular location (In Sync with DPCC Stations)     
   Technique: Web Scraping (Using Selenium in Python)       
   Source: https://freemeteo.in/weather/new-delhi/history/daily-history/?gid=1261481&date=2015-06-01&station=9764&language=english&country=india
       
       Features: -> Temperature in celsius captured at that Hour (In Sync with AQI data)
                      -> Wind Speed
                      -> Wind Direction 
                      -> Atmospheric Pressure
                      -> Humidity
                      -> Desc (Like Thunder, Cloudy, etc)
         Location -> Palam, Delhi
         
         Output Dataframe Format: .xlsx

## IV. Data Preprocessing

I have done Data Preprocessing at different and level and done EDA after every level to improve data preprocessing.

### DP Level - 1 

#### Text Present in Data was removed
-> Missing Values were present in text form
While Web Scraping if Value at time was not availble it was returning "NA", "NaN", "'No data for a day'". All of these were replaced by null values.
It was done for both AQI and Weather Data Set.

-> Weather Data was full of text
Features like teamperature were having "Degree Celsius", Wind Speed had "KmPH" written after the number, Atmospheric pressure had "mb" etc. 

#### Dummy Variables 
Categorical data was converted into Dummies. In Weather Data Weather Description were of 6 Types (like Thunder, Cloudy, Sunny, etc.) and 5 dummies were created. 

#### features Data Type Formatting
-> Timestamp in both the AQI and Weather Datasets were set to Datetime format using pandas.
-> In Weather features like Description was dropped as dummies were created.
-> Rest of the data was converted to numeric type.

### DP Level - 2





