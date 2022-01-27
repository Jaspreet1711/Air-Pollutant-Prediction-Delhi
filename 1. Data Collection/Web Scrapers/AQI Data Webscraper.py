# -*- coding: utf-8 -*-
"""
Created on Wed Nov 10 14:46:11 2021

@author: Jaspreet Singh
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 31 12:33:44 2021

@author: Jaspreet Singh
Day wise AQI Level for every hour at different DPCC Stations of Delhi.   
Technique: Web Scraping (Using Selenium in Python)
Source: https://app.cpcbccr.com/AQI_India/
"""
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
from datetime import datetime as dt

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)

path = 'C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/1. Data Collection/Web Scrapers/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get("https://app.cpcbccr.com/AQI_India/")

time.sleep(5)

# Inputs
state = 'Delhi'
city = 'Delhi'
station = 'Anand'
date_from =  '01/10/2021'
times = '23:30' # -- Time Option on Web Page. I have written times instead of time because it will conflict with library 'time'
mon = 2 # -- Number of Months to be scraped
File_Name = 'AQI_Anand_Vihar_Oct-Nov2021'
tim = 2 # -- Number of seconds to load page (Depends upon your Internet Speed)

# Outputs
timestamp = [] # -- date and time at which station sent the data
PM25 = []
PM10 = []
NO2 = []
NH3 = []
SO2 = []
CO = []
OZONE = []

# Selecting State
State = driver.find_element_by_id("states")
State.click()
state_select = "option[value='"+state+"']"
Select_State = driver.find_element_by_css_selector(state_select)
Select_State.click()

time.sleep(0.25)

# Selecting City
City = driver.find_element_by_id("cities")
City.click()
city_select = "option[value='"+city+"']"    
Select_City = driver.find_element_by_css_selector(city_select)
Select_City.click()

time.sleep(0.25)
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

# Inserting Time
Time_In = driver.find_element_by_id("time")

Time_In.send_keys(Keys.CONTROL, 'a')
Time_In.send_keys(Keys.BACKSPACE)
Time_In.send_keys(times)

# Inserting Date
Date_ele = driver.find_element_by_id("date")
Date_In = Date_ele.find_element_by_css_selector("input[type='text']")

Date_In.send_keys(Keys.CONTROL, 'a')
Date_In.send_keys(Keys.BACKSPACE)
Date_In.send_keys(date_from)
Date_In.click()
Date_In.send_keys(Keys.RETURN)
time.sleep(2)
Date_In.send_keys(Keys.RETURN) # -- Sending return twice because sometimes it stays on current date despite loading
time.sleep(5)

##########################################################################################

# Extract Data from 1st Page
Data_Container = WebDriverWait(driver, 12, ignored_exceptions=ignored_exceptions).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tbody[class='metrics-container']"))
    )
try:
    Data_Rows = Data_Container.find_elements_by_css_selector("tr[class='metrics-row']")
    
    Pollutant = []
    for row in Data_Rows:
        Pollutant.append(row.text.split()[0])  # -- Spliting through backlash (\) can be done using empty .split() function
    
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
                                for i in range(0,iteration):
                                    PM10.append('NA')
                                    c = c + 1
                                PM10.append(data_pm10[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_pm10[0])
                                iteration = index - c
                                for i in range(0,iteration):
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
                                for i in range(0,iteration):
                                    NO2.append('NA')
                                    c = c + 1
                                NO2.append(data_no2[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_no2[0])
                                iteration = index - c
                                for i in range(0,iteration):
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
                                for i in range(0,iteration):
                                    NH3.append('NA')
                                    c = c + 1
                                NH3.append(data_nh3[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_nh3[0])
                                iteration = index - c
                                for i in range(0,iteration):
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
                                for i in range(0,iteration):
                                    SO2.append('NA')
                                    c = c + 1
                                SO2.append(data_so2[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_so2[0])
                                iteration = index - c
                                for i in range(0,iteration):
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
                                for i in range(0,iteration):
                                    CO.append('NA')
                                    c = c + 1
                                CO.append(data_co[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_co[0])
                                iteration = index - c
                                for i in range(0,iteration):
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
                                for i in range(0,iteration):
                                    OZONE.append('NA')
                                    c = c + 1
                                OZONE.append(data_ozone[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_ozone[0])
                                iteration = index - c
                                for i in range(0,iteration):
                                    OZONE.append('NA')
                                    c = c + 1
                                OZONE.append(data_ozone[1])
                            except:
                                pass 
            
            else:
                pass
    
        if pm_10 == False:
            for i in range(0,len(time_alignment)):
                PM10.append("NA")
        else:
            pass
        
        if no_2 == False:
            for i in range(0,len(time_alignment)):
                NO2.append("NA")
        else:
            pass
        
        if nh_3 == False:
            for i in range(0,len(time_alignment)):
                NH3.append("NA") 
        else:
            pass
        
        if so_2 == False:
            for i in range(0,len(time_alignment)):
                SO2.append("NA")
        else:
            pass
        
        if co == False:
            for i in range(0,len(time_alignment)):
                CO.append("NA")
        else:
            pass
        
        if ozone == False:
            for i in range(0,len(time_alignment)):
                OZONE.append("NA")
        else:
            pass
        
        ####
                
        if len(timestamp) > len(PM10):
            n = len(timestamp) - len(PM10)
            for i in range(0,n):
                PM10.append('NA')
        else:
            pass
                
        if len(timestamp) > len(NO2):
            n = len(timestamp) - len(NO2)
            for i in range(0,n):
                NO2.append('NA')
        else:
            pass
                
        if len(timestamp) > len(NH3):
            n = len(timestamp) - len(NH3)
            for i in range(0,n):
                NH3.append('NA')
        else:
            pass
                
        if len(timestamp) > len(SO2):
            n = len(timestamp) - len(SO2)
            for i in range(0,n):
                SO2.append('NA')
        else:
            pass
                
        if len(timestamp) > len(CO):
            n = len(timestamp) - len(CO)
            for i in range(0,n):
                CO.append('NA')
        else:
            pass
                
        if len(timestamp) > len(OZONE):
            n = len(timestamp) - len(OZONE)
            for i in range(0,n):
                OZONE.append('NA')
        else:
            pass
                
        ####
        
    else:
        Date_ele = driver.find_element_by_id("date")
        Date_In = Date_ele.find_element_by_css_selector("input[type='text']")
        missing_date = str(Date_In.get_attribute('value'))
    
        timestamp.append(missing_date)
        PM25.append("No data for a day")
        PM10.append("No data for a day")
        NO2.append("No data for a day")
        NH3.append("No data for a day")
        SO2.append("No data for a day")
        CO.append("No data for a day")
        OZONE.append("No data for a day")

except:
    Date_ele = driver.find_element_by_id("date")
    Date_In = Date_ele.find_element_by_css_selector("input[type='text']")
    missing_date = str(Date_In.get_attribute('value'))
    
    timestamp.append(missing_date)
    PM25.append("No data for a day")
    PM10.append("No data for a day")
    NO2.append("No data for a day")
    NH3.append("No data for a day")
    SO2.append("No data for a day")
    CO.append("No data for a day")
    OZONE.append("No data for a day")

########################################################################################    
# Extracting Data from 1st Month     
Calender_button = Date_ele.find_element_by_css_selector("span[class='input-group-addon']")
Calender_button.click()

Calender_Box = driver.find_element_by_css_selector("div[class='datepicker-days']")
Month_Next = Calender_Box.find_element_by_css_selector("th[class='next']")

Days_Body = Calender_Box.find_element_by_tag_name("tbody")
Days_ele = Days_Body.find_elements_by_css_selector("td[class='day']")
Num_of_Days = len(Days_ele) 
Click_Days = -1

for day in range(0,Num_of_Days):
    Click_Days += 1
    Calender_button = Date_ele.find_element_by_css_selector("span[class='input-group-addon']")
    Calender_button.click()
    Calender_Box = driver.find_element_by_css_selector("div[class='datepicker-days']")
    Days_Body = Calender_Box.find_element_by_tag_name("tbody")
    Days_ele = Days_Body.find_elements_by_css_selector("td[class='day']")
    if Click_Days == 0:
        Days_ele[0].click() 
    else:
        Days_ele[Click_Days].click()
    time.sleep(tim)
    
    ###---To Align data in exception part below---###
    data_pm25 = []
    data_pm10 = []
    data_no2 = []
    data_nh3 = []
    data_so2 = []
    data_co = []
    data_ozone = []
    ###---###
    
    # Extract Data from 2nd day till end from 1st Month
    try:
        data_check = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='panel panel-default aqi-panel']"))
            )
    except:
        #Sometimes page does not load to make it load again it will go back to previous date and comeback to current date
        try:
            Calender_button.click()
            Calender_Box = driver.find_element_by_css_selector("div[class='datepicker-days']")
            Days_Body = Calender_Box.find_element_by_tag_name("tbody")
            Days_ele = Days_Body.find_elements_by_css_selector("td[class='day']")
            Days_ele[Click_Days].click()
        
            time.sleep(1)
        
            Calender_button.click()
            Calender_Box = driver.find_element_by_css_selector("div[class='datepicker-days']")
            Days_Body = Calender_Box.find_element_by_tag_name("tbody")
            Days_ele = Days_Body.find_elements_by_css_selector("td[class='day']")
            Days_ele[Click_Days].click()
            time.sleep(tim)
        except:    
            pass
        try:
            data_check = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='panel panel-default aqi-panel']"))
                )
        except:
            pass
        
    Data_Container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tbody[class='metrics-container']"))
        )
    try:
        #driver.find_element_by_css_selector("tbody[class='metrics-container']")
        Data_Rows = Data_Container.find_elements_by_css_selector("tr[class='metrics-row']")
        
        Pollutant = []
        for row in Data_Rows:
            Pollutant.append(row.text.split()[0])  # -- Spliting through backlash (\) can be done using empty .split() function
        
        pm_25 = "PM2.5" in Pollutant
        pm_10 = "PM10" in Pollutant
        no_2 = "NO2" in Pollutant
        nh_3 = "NH3" in Pollutant
        so_2 = "SO2" in Pollutant
        co = "CO" in Pollutant
        ozone = "OZONE" in Pollutant
        
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
                    time_in_pm10 = []
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
                                iteration = index - c
                                for i in range(0,iteration):
                                    PM10.append('NA')
                                    c = c + 1
                                PM10.append(data_pm10[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_pm10[0])
                                iteration = index - c
                                for i in range(0,iteration):
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
                                for i in range(0,iteration):
                                    NO2.append('NA')
                                    c = c + 1
                                NO2.append(data_no2[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_no2[0])
                                iteration = index - c
                                for i in range(0,iteration):
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
                                for i in range(0,iteration):
                                    NH3.append('NA')
                                    c = c + 1
                                NH3.append(data_nh3[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_co[0])
                                iteration = index - c
                                for i in range(0,iteration):
                                    NH3.append('NA')
                                    c = c + 1
                                NH3.append(data_co[1])
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
                                for i in range(0,iteration):
                                    SO2.append('NA')
                                    c = c + 1
                                SO2.append(data_so2[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_co[0])
                                iteration = index - c
                                for i in range(0,iteration):
                                    SO2.append('NA')
                                    c = c + 1
                                SO2.append(data_co[1])
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
                                for i in range(0,iteration):
                                    CO.append('NA')
                                    c = c + 1
                                CO.append(data_co[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_co[0])
                                iteration = index - c
                                for i in range(0,iteration):
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
                                for i in range(0,iteration):
                                    OZONE.append('NA')
                                    c = c + 1
                                OZONE.append(data_ozone[1])
                            except:
                                pass
                        else:
                            try:
                                index = time_alignment.index(data_co[0])
                                iteration = index - c
                                for i in range(0,iteration):
                                    OZONE.append('NA')
                                    c = c + 1
                                OZONE.append(data_co[1])
                            except:
                                pass 
                            
                else:
                    pass
        
            if pm_10 == False:
                for i in range(0,len(time_alignment)):
                    PM10.append("NA")
            else:
                pass
        
            if no_2 == False:
                for i in range(0,len(time_alignment)):
                    NO2.append("NA")
            else:
                pass
        
            if nh_3 == False:
                for i in range(0,len(time_alignment)):
                    NH3.append("NA") 
            else:
                pass
        
            if so_2 == False:
                for i in range(0,len(time_alignment)):
                    SO2.append("NA")
            else:
                pass
        
            if co == False:
                for i in range(0,len(time_alignment)):
                    CO.append("NA")
            else:
                pass
        
            if ozone == False:
                for i in range(0,len(time_alignment)):
                    OZONE.append("NA")
            else:
                pass
            
            ####
                
            if len(timestamp) > len(PM10):
                n = len(timestamp) - len(PM10)
                for i in range(0,n):
                    PM10.append('NA')
            else:
                pass
                
            if len(timestamp) > len(NO2):
                n = len(timestamp) - len(NO2)
                for i in range(0,n):
                    NO2.append('NA')
            else:
                pass
                
            if len(timestamp) > len(NH3):
                n = len(timestamp) - len(NH3)
                for i in range(0,n):
                    NH3.append('NA')
            else:
                pass
                
            if len(timestamp) > len(SO2):
                n = len(timestamp) - len(SO2)
                for i in range(0,n):
                    SO2.append('NA')
            else:
                pass
                
            if len(timestamp) > len(CO):
                n = len(timestamp) - len(CO)
                for i in range(0,n):
                    CO.append('NA')
            else:
                pass
                
            if len(timestamp) > len(OZONE):
                n = len(timestamp) - len(OZONE)
                for i in range(0,n):
                    OZONE.append('NA')
            else:
                pass
                
            ####
        
        else:
            Date_ele = driver.find_element_by_id("date")
            Date_In = Date_ele.find_element_by_css_selector("input[type='text']")
            missing_date = str(Date_In.get_attribute('value'))

            timestamp.append(missing_date)
            PM25.append("No data for a day")
            PM10.append("No data for a day")
            NO2.append("No data for a day")
            NH3.append("No data for a day")
            SO2.append("No data for a day")
            CO.append("No data for a day")
            OZONE.append("No data for a day")

    except:
        Date_ele = driver.find_element_by_id("date")
        Date_In = Date_ele.find_element_by_css_selector("input[type='text']")
        missing_date = str(Date_In.get_attribute('value'))
        
        if len(data_pm25) == 0:
            timestamp.append(missing_date)   
            PM25.append("No data for a day_1")
            PM10.append("No data for a day_1")
            NO2.append("No data for a day_1")
            NH3.append("No data for a day_1")
            SO2.append("No data for a day_1")
            CO.append("No data for a day_1")
            OZONE.append("No data for a day_1")
            time_alignment = []
        else:
            pass
            
        if len(data_pm10) > 0:
            pass
        else:
            for i in range(0,len(time_alignment)):
                PM10.append("No data for a day_1")
            
        if len(data_no2) > 0:
            pass
        else:
            for i in range(0,len(time_alignment)):
                NO2.append("No data for a day_1")
        
        if len(data_nh3) > 0:
            pass
        else:
            for i in range(0,len(time_alignment)):
                NH3.append("No data for a day_1")
            
        if len(data_so2) > 0:
            pass
        else:
            for i in range(0,len(time_alignment)):
                SO2.append("No data for a day_1")
            
        if len(data_co) > 0:
            pass
        else:
            for i in range(0,len(time_alignment)):
                CO.append("No data for a day_1")
        
        if len(data_ozone) > 0:
            pass
        else:
            for i in range(0,len(time_alignment)):
                OZONE.append("No data for a day_1")

###############################################################################

# Adjusting Date format to crawl till last month
date_from = date_from.replace('/', ' ')
Date = dt.strptime(date_from, '%d %m %Y')
Today = dt.today().strftime('%d %m %Y')
Today = dt.strptime(Today, '%d %m %Y')

def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

#Num_of_Months = int(diff_month(Today, Date)) + 1
Num_of_Months = mon 

for month in range(1,Num_of_Months):
    Calender_button = Date_ele.find_element_by_css_selector("span[class='input-group-addon']")
    Calender_button.click()
    Month_Next = Calender_Box.find_element_by_css_selector("th[class='next']")    
    Month_Next.click()
    
    Days_ele = Days_Body.find_elements_by_css_selector("td[class='day']")
    Num_of_Days = len(Days_ele) 
    Click_Days = -1
    
    for day in range(0,Num_of_Days):
        Click_Days += 1
        Calender_button = Date_ele.find_element_by_css_selector("span[class='input-group-addon']")
        Calender_button.click()
        Calender_Box = driver.find_element_by_css_selector("div[class='datepicker-days']")
        Days_Body = Calender_Box.find_element_by_tag_name("tbody")
        Days_ele = Days_Body.find_elements_by_css_selector("td[class='day']")     
        if Click_Days == 0:
            Days_ele[0].click() 
        else:
            Days_ele[Click_Days-1].click()
        time.sleep(tim)
        
        ###---To Align data in exception part below---###
        data_pm25 = []
        data_pm10 = []
        data_no2 = []
        data_nh3 = []
        data_so2 = []
        data_co = []
        data_ozone = []
        ###---###
        
        # Extract Data of every day from 2nd Month till end
        try:
            data_check = WebDriverWait(driver, 4).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='panel panel-default aqi-panel']"))
                )
        except:
            #Sometimes page does not load to make it load again it will go to next date and comeback to current date.
            try:
                Calender_button.click()
                Calender_Box = driver.find_element_by_css_selector("div[class='datepicker-days']")
                Days_Body = Calender_Box.find_element_by_tag_name("tbody")
                Days_ele = Days_Body.find_elements_by_css_selector("td[class='day']")
                Days_ele[Click_Days].click()
                time.sleep(tim)
        
                Calender_button.click()
                Calender_Box = driver.find_element_by_css_selector("div[class='datepicker-days']")
                Days_Body = Calender_Box.find_element_by_tag_name("tbody")
                Days_ele = Days_Body.find_elements_by_css_selector("td[class='day']")
                Days_ele[Click_Days].click()
                time.sleep(tim)
            except:
                pass
            try:
                data_check = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='panel panel-default aqi-panel']"))
                    )
            except:
                pass
            
        try:
            Data_Container = driver.find_element_by_css_selector("tbody[class='metrics-container']")
            Data_Rows = Data_Container.find_elements_by_css_selector("tr[class='metrics-row']")
        
            Pollutant = []
            for row in Data_Rows:
                Pollutant.append(row.text.split()[0])  # -- Spliting through backlash (\) can be done using empty .split() function
        
            pm_25 = "PM2.5" in Pollutant
            pm_10 = "PM10" in Pollutant
            no_2 = "NO2" in Pollutant
            nh_3 = "NH3" in Pollutant
            so_2 = "SO2" in Pollutant
            co = "CO" in Pollutant
            ozone = "OZONE" in Pollutant
            
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
                        time_in_pm10 = []
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
                                    iteration = index - c
                                    for i in range(0,iteration):
                                        PM10.append('NA')
                                        c = c + 1
                                    PM10.append(data_pm10[1])
                                except:
                                    pass
                            else:
                                try:
                                    index = time_alignment.index(data_pm10[0])
                                    iteration = index - c
                                    for i in range(0,iteration):
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
                                    for i in range(0,iteration):
                                        NO2.append('NA')
                                        c = c + 1
                                    NO2.append(data_no2[1])
                                except:
                                    pass
                            else:
                                try:
                                    index = time_alignment.index(data_no2[0])
                                    iteration = index - c 
                                    for i in range(0,iteration):
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
                                    for i in range(0,iteration):
                                        NH3.append('NA')
                                        c = c + 1
                                    NH3.append(data_nh3[1])
                                except:
                                    pass
                            else:
                                try:
                                    index = time_alignment.index(data_co[0])
                                    iteration = index - c
                                    for i in range(0,iteration):
                                        NH3.append('NA')
                                        c = c + 1
                                    NH3.append(data_co[1])
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
                                    for i in range(0,iteration):
                                        SO2.append('NA')
                                        c = c + 1
                                    SO2.append(data_so2[1])
                                except:
                                    pass
                            else:
                                try:
                                    index = time_alignment.index(data_co[0])
                                    iteration = index - c
                                    for i in range(0,iteration):
                                        SO2.append('NA')
                                        c = c + 1
                                    SO2.append(data_co[1])
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
                                    for i in range(0,iteration):
                                        CO.append('NA')
                                        c = c + 1
                                    CO.append(data_co[1])
                                except:
                                    pass
                            else:
                                try:
                                    index = time_alignment.index(data_co[0])
                                    iteration = index - c
                                    for i in range(0,iteration):
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
                                    for i in range(0,iteration):
                                        OZONE.append('NA')
                                        c = c + 1
                                    OZONE.append(data_ozone[1])
                                except:
                                    pass
                            else:
                                try:
                                    index = time_alignment.index(data_co[0])
                                    iteration = index - c
                                    for i in range(0,iteration):
                                        OZONE.append('NA')
                                        c = c + 1
                                    OZONE.append(data_co[1])
                                except:
                                    pass    
                    
                    else:
                        pass
                
                if pm_10 == False:
                    for i in range(0,len(time_alignment)):
                        PM10.append("NA")
                else:
                    pass
        
                if no_2 == False:
                    for i in range(0,len(time_alignment)):
                        NO2.append("NA")
                else:
                    pass
        
                if nh_3 == False:
                    for i in range(0,len(time_alignment)):
                        NH3.append("NA") 
                else:
                    pass
        
                if so_2 == False:
                    for i in range(0,len(time_alignment)):
                        SO2.append("NA")
                else:
                    pass
        
                if co == False:
                    for i in range(0,len(time_alignment)):
                        CO.append("NA")
                else:
                    pass
        
                if ozone == False:
                    for i in range(0,len(time_alignment)):
                        OZONE.append("NA")
                else:
                    pass
                
                ####
                
                if len(timestamp) > len(PM10):
                    n = len(timestamp) - len(PM10)
                    for i in range(0,n):
                        PM10.append('NA')
                else:
                    pass
                
                if len(timestamp) > len(NO2):
                    n = len(timestamp) - len(NO2)
                    for i in range(0,n):
                        NO2.append('NA')
                else:
                    pass
                
                if len(timestamp) > len(NH3):
                    n = len(timestamp) - len(NH3)
                    for i in range(0,n):
                        NH3.append('NA')
                else:
                    pass
                
                if len(timestamp) > len(SO2):
                    n = len(timestamp) - len(SO2)
                    for i in range(0,n):
                        SO2.append('NA')
                else:
                    pass
                
                if len(timestamp) > len(CO):
                    n = len(timestamp) - len(CO)
                    for i in range(0,n):
                        CO.append('NA')
                else:
                    pass
                
                if len(timestamp) > len(OZONE):
                    n = len(timestamp) - len(OZONE)
                    for i in range(0,n):
                        OZONE.append('NA')
                else:
                    pass
                
                ####
                
            else:
                Date_ele = driver.find_element_by_id("date")
                Date_In = Date_ele.find_element_by_css_selector("input[type='text']")
                missing_date = str(Date_In.get_attribute('value'))
        
                timestamp.append(missing_date)
                PM25.append("No data for a day")
                PM10.append("No data for a day")
                NO2.append("No data for a day")
                NH3.append("No data for a day")
                SO2.append("No data for a day")
                CO.append("No data for a day")
                OZONE.append("No data for a day")
        
        except:
            
            Date_ele = driver.find_element_by_id("date")
            Date_In = Date_ele.find_element_by_css_selector("input[type='text']")
            missing_date = str(Date_In.get_attribute('value'))
            
            if len(data_pm25) == 0:
                timestamp.append(missing_date)   
                PM25.append("No data for a day_1")
                PM10.append("No data for a day_1")
                NO2.append("No data for a day_1")
                NH3.append("No data for a day_1")
                SO2.append("No data for a day_1")
                CO.append("No data for a day_1")
                OZONE.append("No data for a day_1")
                time_alignment = []
            else:
                pass
            
            if len(data_pm10) > 0:
                pass
            else:
                for i in range(0,len(time_alignment)):
                    PM10.append("No data for a day_1")
            
            if len(data_no2) > 0:
                pass
            else:
                for i in range(0,len(time_alignment)):
                    NO2.append("No data for a day_1")
            
            if len(data_nh3 ) > 0:
                pass
            else:
                for i in range(0,len(time_alignment)):
                    NH3.append("No data for a day_1")
            
            if len(data_so2) > 0:
                pass
            else:
                for i in range(0,len(time_alignment)):
                    SO2.append("No data for a day_1")
            
            if len(data_co) > 0:
                pass
            else:
                for i in range(0,len(time_alignment)):
                    CO.append("No data for a day_1")
            
            if len(data_ozone) > 0:
                pass
            else:
                for i in range(0,len(time_alignment)):
                    OZONE.append("No data for a day_1")

##################################################################################

Output_DF = pd.DataFrame(
    {'timestamp': timestamp,
     'PM2.5': PM25,
     'PM10': PM10,
     'NO2': NO2,
     'NH3': NH3,
     'SO2': SO2,
     'CO': CO,
     'OZONE': OZONE
    })

datatoexcel = pd.ExcelWriter(File_Name+'.xlsx')

Output_DF.to_excel(datatoexcel)
datatoexcel.save()
print("File Saved in Excel Format in your system.")

time.sleep(8)
driver.close()