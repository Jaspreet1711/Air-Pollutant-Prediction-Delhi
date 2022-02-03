import numpy as np
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time
from datetime import datetime

# Inputs
state = 'Delhi'
city = 'Delhi'
station = 'Punjabi'
tim = 20 # -- Number of seconds to load page (Depends upon your Internet Speed)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)

path = 'C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/1. Data Collection/Web Scrapers/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get("https://app.cpcbccr.com/AQI_India/")

time.sleep(tim)

# Outputs
timestamp = [] # -- date and time at which station sent the data
PM25 = []
PM10 = []
NO2 = []
NH3 = []
SO2 = []
CO = []
OZONE = []

# ------------ If page will not upload it will try mulitple times --------- #
try:
    State = driver.find_element_by_id("states")
    State.click()
    state_select = "option[value='" + state + "']"
    Select_State = driver.find_element_by_css_selector(state_select)
    Select_State.click()
except:
    # Page Crashed Refreshing it
    driver.refresh()
    time.sleep(3)
    driver.refresh()
    time.sleep(tim)
    try:
        State = driver.find_element_by_id("states")
        State.click()
        state_select = "option[value='" + state + "']"
        Select_State = driver.find_element_by_css_selector(state_select)
        Select_State.click()
    except:
        # Page Crashed Refreshing it
        driver.refresh()
        time.sleep(3)
        driver.refresh()
        time.sleep(tim)
        try:
            State = driver.find_element_by_id("states")
            State.click()
            state_select = "option[value='" + state + "']"
            Select_State = driver.find_element_by_css_selector(state_select)
            Select_State.click()
        except:
            # Page Crashed Refreshing it
            driver.refresh()
            time.sleep(3)
            driver.refresh()
            time.sleep(tim/2)
            try:
                State = driver.find_element_by_id("states")
                State.click()
                state_select = "option[value='" + state + "']"
                Select_State = driver.find_element_by_css_selector(state_select)
                Select_State.click()
            except:
                # Page Crashed Refreshing it
                driver.refresh()
                time.sleep(3)
                driver.refresh()
                time.sleep(tim/2)
                State = driver.find_element_by_id("states")
                State.click()
                state_select = "option[value='" + state + "']"
                Select_State = driver.find_element_by_css_selector(state_select)
                Select_State.click()
# ------------------------------------------------------------------------------------ #

# Selecting State
# State = driver.find_element_by_id("states")
# State.click()
# state_select = "option[value='"+state+"']"
# Select_State = driver.find_element_by_css_selector(state_select)
# Select_State.click()

time.sleep(0.25)

# Selecting City
City = driver.find_element_by_id("cities")
City.click()
city_select = "option[value='" + city + "']"
Select_City = driver.find_element_by_css_selector(city_select)
Select_City.click()

time.sleep(tim/5)
station_words = station.split(' ')

# Selecting Station
Station = driver.find_element_by_id("stations")
Station.click()
Options_Stations_ele = Station.find_elements_by_tag_name("Option")
Options_Stations = []
opt_num = -1
for opt in Options_Stations_ele:
    opt_num = opt_num + 1
    if len(station_words) == 1:
        if station_words[0] in opt.text:
            select_opt_num = opt_num
        else:
            pass
    elif len(station_words) > 1:
        if station_words[0] and station_words[1] in opt.text:
            select_opt_num = opt_num
        else:
            pass

Options_Stations_ele[select_opt_num].click()

time.sleep(tim)

# -- Extracting Date
date_table = driver.find_element_by_css_selector("table[class='table table-condensed']")
date_ele = date_table.find_element_by_css_selector("span[class='date-on label label-info']")
date_ls = date_ele.text.split(' ')
date = str(date_ls[1] + ' ' + date_ls[2] + ' ' + date_ls[3])
date = pd.to_datetime(date, dayfirst=True).strftime('%Y-%m-%d')
timestamp.append(date)

# -- Extracting Avg Pollutant level
Data_Container = WebDriverWait(driver, 40, ignored_exceptions=ignored_exceptions).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody[class='metrics-container']"))
)
try:
    Data_Rows = Data_Container.find_elements_by_css_selector("tr[class='metrics-row']")

    Pollutant = []
    for row in Data_Rows:
        Pollutant.append(
            row.text.split()[0])  # -- Spliting through backlash (\) can be done using empty .split() function

    pm_25 = "PM2.5" in Pollutant
    pm_10 = "PM10" in Pollutant
    no_2 = "NO2" in Pollutant
    nh_3 = "NH3" in Pollutant
    so_2 = "SO2" in Pollutant
    co = "CO" in Pollutant
    ozone = "OZONE" in Pollutant

    ###---To Align data in exception part below---###
    data_pm25 = []
    data_pm10 = []
    data_no2 = []
    data_nh3 = []
    data_so2 = []
    data_co = []
    data_ozone = []
    ###---###

    if pm_25 == True and Pollutant.index("PM2.5") == 0:
        time_alignment = []
        count = -1
        for pol in Pollutant:
            count += 1

            if pol == 'PM2.5':
                tbody = Data_Rows[count].find_element_by_tag_name("tbody")
                pm25_trs = tbody.find_elements_by_tag_name("tr")
                for i in pm25_trs:
                    td = i.find_elements_by_tag_name("td")
                    data_pm25 = []
                    for i in td:
                        data_pm25.append((i.get_attribute('textContent')))
                    time_alignment.append(data_pm25[0])
                    timestamp.append(data_pm25[0])
                    PM25.append(data_pm25[1])

            elif pol == 'PM10':
                tbody = Data_Rows[count].find_element_by_tag_name("tbody")
                trs = tbody.find_elements_by_tag_name("tr")
                c = -1
                for i in trs:
                    c += 1
                    td = i.find_elements_by_tag_name("td")
                    data_pm10 = []
                    for i in td:
                        data_pm10.append((i.get_attribute('textContent')))

                    if len(time_alignment) >= len(trs):
                        try:
                            index = time_alignment.index(data_pm10[0])
                            iteration = index - c  # -- align data with common time stamp (Taken as per pm2.5)
                            for i in range(0, iteration):
                                PM10.append('NA')
                                c = c + 1
                            PM10.append(data_pm10[1])
                        except:
                            pass
                    else:
                        try:
                            index = time_alignment.index(data_pm10[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                PM10.append('NA')
                                c = c + 1
                            PM10.append(data_pm10[1])
                        except:
                            pass

            elif pol == 'NO2':
                tbody = Data_Rows[count].find_element_by_tag_name("tbody")
                trs = tbody.find_elements_by_tag_name("tr")
                c = -1
                for i in trs:
                    c += 1
                    td = i.find_elements_by_tag_name("td")
                    data_no2 = []
                    for i in td:
                        data_no2.append((i.get_attribute('textContent')))

                    if len(time_alignment) >= len(trs):
                        try:
                            index = time_alignment.index(data_no2[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                NO2.append('NA')
                                c = c + 1
                            NO2.append(data_no2[1])
                        except:
                            pass
                    else:
                        try:
                            index = time_alignment.index(data_no2[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                NO2.append('NA')
                                c = c + 1
                            NO2.append(data_no2[1])
                        except:
                            pass

            elif pol == 'NH3':
                tbody = Data_Rows[count].find_element_by_tag_name("tbody")
                trs = tbody.find_elements_by_tag_name("tr")
                c = -1
                for i in trs:
                    c += 1
                    td = i.find_elements_by_tag_name("td")
                    data_nh3 = []
                    for i in td:
                        data_nh3.append((i.get_attribute('textContent')))

                    if len(time_alignment) >= len(trs):
                        try:
                            index = time_alignment.index(data_nh3[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                NH3.append('NA')
                                c = c + 1
                            NH3.append(data_nh3[1])
                        except:
                            pass
                    else:
                        try:
                            index = time_alignment.index(data_nh3[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                NH3.append('NA')
                                c = c + 1
                            NH3.append(data_nh3[1])
                        except:
                            pass

            elif pol == 'SO2':
                tbody = Data_Rows[count].find_element_by_tag_name("tbody")
                trs = tbody.find_elements_by_tag_name("tr")
                c = -1
                for i in trs:
                    c += 1
                    td = i.find_elements_by_tag_name("td")
                    data_so2 = []
                    for i in td:
                        data_so2.append((i.get_attribute('textContent')))

                    if len(time_alignment) >= len(trs):
                        try:
                            index = time_alignment.index(data_so2[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                SO2.append('NA')
                                c = c + 1
                            SO2.append(data_so2[1])
                        except:
                            pass
                    else:
                        try:
                            index = time_alignment.index(data_so2[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                SO2.append('NA')
                                c = c + 1
                            SO2.append(data_so2[1])
                        except:
                            pass

            elif pol == 'CO':
                tbody = Data_Rows[count].find_element_by_tag_name("tbody")
                trs = tbody.find_elements_by_tag_name("tr")
                c = -1
                for i in trs:
                    c += 1
                    td = i.find_elements_by_tag_name("td")
                    data_co = []
                    for i in td:
                        data_co.append((i.get_attribute('textContent')))

                    if len(time_alignment) >= len(trs):
                        try:
                            index = time_alignment.index(data_co[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                CO.append('NA')
                                c = c + 1
                            CO.append(data_co[1])
                        except:
                            pass
                    else:
                        try:
                            index = time_alignment.index(data_co[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                CO.append('NA')
                                c = c + 1
                            CO.append(data_co[1])
                        except:
                            pass

            elif pol == 'OZONE':
                tbody = Data_Rows[count].find_element_by_tag_name("tbody")
                trs = tbody.find_elements_by_tag_name("tr")
                c = -1
                for i in trs:
                    c += 1
                    td = i.find_elements_by_tag_name("td")
                    data_ozone = []
                    for i in td:
                        data_ozone.append((i.get_attribute('textContent')))

                    if len(time_alignment) >= len(trs):
                        try:
                            index = time_alignment.index(data_ozone[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                OZONE.append('NA')
                                c = c + 1
                            OZONE.append(data_ozone[1])
                        except:
                            pass
                    else:
                        try:
                            index = time_alignment.index(data_ozone[0])
                            iteration = index - c
                            for i in range(0, iteration):
                                OZONE.append('NA')
                                c = c + 1
                            OZONE.append(data_ozone[1])
                        except:
                            pass

            else:
                pass

        if pm_10 == False:
            for i in range(0, len(time_alignment)):
                PM10.append("NA")
        else:
            pass

        if no_2 == False:
            for i in range(0, len(time_alignment)):
                NO2.append("NA")
        else:
            pass

        if nh_3 == False:
            for i in range(0, len(time_alignment)):
                NH3.append("NA")
        else:
            pass

        if so_2 == False:
            for i in range(0, len(time_alignment)):
                SO2.append("NA")
        else:
            pass

        if co == False:
            for i in range(0, len(time_alignment)):
                CO.append("NA")
        else:
            pass

        if ozone == False:
            for i in range(0, len(time_alignment)):
                OZONE.append("NA")
        else:
            pass

        ####

        if len(timestamp) > len(PM10):
            n = len(timestamp) - len(PM10)
            for i in range(0, n):
                PM10.append('NA')
        else:
            pass

        if len(timestamp) > len(NO2):
            n = len(timestamp) - len(NO2)
            for i in range(0, n):
                NO2.append('NA')
        else:
            pass

        if len(timestamp) > len(NH3):
            n = len(timestamp) - len(NH3)
            for i in range(0, n):
                NH3.append('NA')
        else:
            pass

        if len(timestamp) > len(SO2):
            n = len(timestamp) - len(SO2)
            for i in range(0, n):
                SO2.append('NA')
        else:
            pass

        if len(timestamp) > len(CO):
            n = len(timestamp) - len(CO)
            for i in range(0, n):
                CO.append('NA')
        else:
            pass

        if len(timestamp) > len(OZONE):
            n = len(timestamp) - len(OZONE)
            for i in range(0, n):
                OZONE.append('NA')
        else:
            pass

        ####

    else:
        Date_ele = driver.find_element_by_id("date")
        Date_In = Date_ele.find_element_by_css_selector("input[type='text']")
        missing_date = str(Date_In.get_attribute('value'))

        timestamp.append(missing_date)
        PM25.append("NA")
        PM10.append("NA")
        NO2.append("NA")
        NH3.append("NA")
        SO2.append("NA")
        CO.append("NA")
        OZONE.append("NA")

except:
    Date_ele = driver.find_element_by_id("date")
    Date_In = Date_ele.find_element_by_css_selector("input[type='text']")
    missing_date = str(Date_In.get_attribute('value'))

    timestamp.append(missing_date)
    PM25.append("NA")
    PM10.append("NA")
    NO2.append("NA")
    NH3.append("NA")
    SO2.append("NA")
    CO.append("NA")
    OZONE.append("NA")

#######################################

def Average_list(lst):
  new_list = []
  for i in lst:
    if i == 'NaN':
      pass
    elif i != 'NA':
      new_list.append(int(i))
    else:
      pass
  if len(new_list) > 7:
    try:
      result = sum(new_list) / len(new_list)
    except:
      result = np.nan
  else:
    result = np.nan
  return result

#######################

try:
    timestamp = timestamp[12]
    print("Yes")
except:
    timestamp = datetime.now()
    print("No")
timestamp = pd.to_datetime(timestamp).strftime('%Y-%m-%d')
PM25 = Average_list(PM25)
PM10 = Average_list(PM10)
NO2 = Average_list(NO2)
NH3 = Average_list(NH3)
SO2 = Average_list(SO2)
CO = Average_list(CO)
OZONE = Average_list(OZONE)
#############

# ------------------------------------------------------------------------------- #
###################################################################################
###################################################################################
#####-------------###############################################-------------#####
###################################################################################
###################################################################################
#### ------ ########################################################## ------ #####
#### ------- ######################################################### ------- ####
### --------- ####################################################### --------- ###
### --------- ####################################################### --------- ###
#### ------- ######################################################### ------- ####
#### ------ ##########################------########################## ------ #####
#####################################--------######################################
###################################################################################
###################################################################################
#########################---------------------------------#########################
#########################---------------------------------#########################
###################################################################################

# Now going to freemeteo website for Delhi's weather data.
driver.get("https://freemeteo.in/weather/new-delhi/current-weather/location/?gid=1261481&language=english&country=india")
time.sleep(tim/2)

# Clicking on History Tab
history_tab = driver.find_element_by_css_selector("li[class='h ']")
history_tab.click()

# Closing the Ad on page
time.sleep(tim/4)
action = webdriver.ActionChains(driver)
action.move_by_offset(10, 20)  # 10px to the right, 20px to bottom
action.perform()
action.double_click()
action.perform()
time.sleep(2)

# Clicking on Today's Date.
time.sleep(tim/5)
today_weather = driver.find_element_by_css_selector("li[class='a active']")
today_weather.click()

# Outputs
Date_Time = []
Temp = []
Relative_Temp = []
Wind_Speed = []
Wind_Direction = []
Wind_Gust = []
Rel_Humidity = []
Dew_Point = []
Atmos_Pressure = []
Description = []

# Collecting Weather Data
Date_ele = driver.find_element_by_css_selector("a[class='cal']")
Date = Date_ele.text
Table = driver.find_element_by_css_selector("div[class='table hourly']")
TRs = Table.find_elements_by_tag_name("tr")

for row in TRs:
    TDs = row.find_elements_by_tag_name("td")
    if len(TDs) == 10:
        c = -1
        for detail in TDs:
            det = detail.text
            c += 1
            if c == 0:
                dt = str(Date) + det
                Date_Time.append(dt)
            elif c == 1:
                Temp.append(det)
            elif c == 2:
                Relative_Temp.append(det)
            elif c == 3:
                Wind_Speed.append(det)
                try:
                    wind_dir_ele = detail.find_element_by_css_selector("div[class='wind-popinfo']")
                    wind_dir = wind_dir_ele.get_attribute('textContent')
                except:
                    wind_dir = np.nan
                Wind_Direction.append(wind_dir)
            elif c == 4:
                Wind_Gust.append(det)
            elif c == 5:
                Rel_Humidity.append(det)
            elif c == 6:
                Dew_Point.append(det)
            elif c == 7:
                Atmos_Pressure.append(det)
            elif c == 8:
                pass
            elif c == 9:
                Description.append(det)
            else:
                pass
    else:
        pass


dw = pd.DataFrame(
    {'Date & Time': Date_Time,
     'Temperature_in_°C': Temp,
     'Relative_Temp_in_°C': Relative_Temp,
     'Wind_Speed_in_Kmph': Wind_Speed,
     'Wind_Direction': Wind_Direction,
     'Wind_Gust': Wind_Gust,
     'Rel_Humidity': Rel_Humidity,
     'Dew_Point_in_°C': Dew_Point,
     'Atmospheric_Pressure_in_mb': Atmos_Pressure,
     'Description': Description
    })

# Cleaning Temperature
dw['Temperature_in_°C'] = dw['Temperature_in_°C'].apply(lambda x: x.replace('°C', ''))
dw['Temperature_in_°C'] = dw['Temperature_in_°C'].apply(lambda x: int(x))

# Cleaning Wind_Speed
# -- We will removing 'km/h', 'calm', 'variable at' and 'Wind Gust'.
# -- We have handled Calm and Variability above already by creating new columns.
dw['Wind_Speed_in_Kmph'] = dw['Wind_Speed_in_Kmph'].apply(lambda x: x.replace(' Km/h', '').replace('Variable at ', '').replace(' Wind Gust', ''))
dw['Wind_Speed_in_Kmph'] = dw['Wind_Speed_in_Kmph'].apply(lambda x: x.replace(',', ''))
def wind_calm_val(r):
    r = r
    if r['Wind_Speed_in_Kmph'] == 'Calm':
        return 3
    else:
        return r['Wind_Speed_in_Kmph']
dw['Wind_Speed_in_Kmph'] = dw.apply(lambda x: wind_calm_val(x), axis=1)
dw['Wind_Speed_in_Kmph'] = dw['Wind_Speed_in_Kmph'].apply(lambda x: int(x))

# Cleaning Rel_Humidity
dw['Rel_Humidity'] = dw['Rel_Humidity'].apply(lambda x: x.replace('%', ''))
dw['Rel_Humidity'] = dw['Rel_Humidity'].apply(lambda x: int(x))
dw['Rel_Humidity'] = dw['Rel_Humidity']/100

# Cleaning Dew_Point
dw['Dew_Point_in_°C'] = dw['Dew_Point_in_°C'].apply(lambda x: x.replace('°C', ''))
dw['Dew_Point_in_°C'] = dw['Dew_Point_in_°C'].apply(lambda x: int(x))

# Cleaning Atmospheric_Pressure
dw['Atmospheric_Pressure_in_mb'] = dw['Atmospheric_Pressure_in_mb'].apply(lambda x: x.replace('mb', ''))
dw['Atmospheric_Pressure_in_mb'] = pd.to_numeric(dw['Atmospheric_Pressure_in_mb'])

Temperature = dw['Temperature_in_°C'].mean()
Wind_Speed_in_Kmph = dw['Wind_Speed_in_Kmph'].mean()
Rel_Humidity = dw['Rel_Humidity'].mean()
Dew_Point = dw['Dew_Point_in_°C'].mean()
Atmospheric_Pressure_in_mb = dw['Atmospheric_Pressure_in_mb'].mean()

#print(" ")
#print("Start1")
#print(Temperature)
#print(Wind_Speed_in_Kmph)
#print(Rel_Humidity)
#print(Dew_Point)
#print(Atmospheric_Pressure_in_mb)
#print("End1")

output_dict = {
        "timestamp": timestamp,
        "PM2-5": str(PM25),
        "PM10": str(PM10),
        "NO2": str(NO2),
        "SO2": str(SO2),
        "CO": str(CO),
        "Temperature_in_cel": str(Temperature),
        "Wind_Speed_in_Kmph": str(Wind_Speed_in_Kmph),
        "Rel_Humidity": str(Rel_Humidity),
        "Dew_Point_in_cel": str(Dew_Point),
        "Atmospheric_Pressure_in_mb": str(Atmospheric_Pressure_in_mb)
}

print(output_dict)

import pyrebase

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

# Pushing data
db.child(timestamp).set(output_dict)

driver.close()