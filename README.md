# Air-Pollutant-Prediction-Delhi
Brief: Time Series Forecasting and Cross Section Prediction of PM2.5 and PM10 in Delhi

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

A. Air Quality Index (AQI) Data
       Day wise AQI Level for every hour at different DPCC Stations of Delhi.   
       Technique: Web Scraping (Using Selenium in Python)
       Source: https://app.cpcbccr.com/AQI_India/
       
       Features: -> Diff Pollutants - (Like PM 10, 2.5, CO, 
                                                      NO2, NNH3, Ozone, 
                                                      SO2)
                      -> Every Hour (From 12:30 AM to 11:30 PM), 
                      -> Avg, Min, Max, 
                      -> Prominent Pollutant
                       
       Stations:                                      From
       1. Punjabi Bagh, Delhi - DPCC -  1st June 2015
       2. Anand Vihar, Delhi - DPCC  -  1st Nov  2017
       3. R.K. Puram, Delhi    - DPCC  -  1st Nov  2017
       4. J.N. Stadium, Delhi  - DPCC -   1st  Feb  2018
       5. Ohkla Ph-2, Delhi    - DPCC -   2nd  Feb  2018
       6. Patparganj, Delhi     - DPCC -   2nd  Feb  2018
       7. Wazirpur, Delhi       - DPCC -   2nd  Feb  2018
       8. Rohini, Delhi           - DPCC -   2nd  Feb  2018
       9. Ashok Vihar, Delhi  - DPCC -   2nd  Feb  2018
     10. KSSR, Delhi             - DPCC -   2nd  Feb  2018
     11. Dwarka, Sec-8, Delhi - DPCC- 2nd  Feb  2018
  
B. Weather Data
       Day Wise Every Hour Weather Report for particular location (In Sync with DPCC Stations)     
       Technique: Web Scraping (Using Selenium in Python)       
       Source: https://freemeteo.in/weather/new-delhi/history/daily-history/?gid=1261481&date=2015-06-01&station=9764&language=english&country=india
       
       Features: -> Temperature in celsius captured at that Hour (In Sync with AQI data)
                      -> Wind Speed
                      -> Wind Direction 
                      -> Atmospheric Pressure
                      -> Humidity
                      -> Desc (Like Thunder, Cloudy, etc)
         Location -> Palam, Delhi


