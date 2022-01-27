# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 12:13:22 2021

@author: Jaspreet Singh
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
from time import localtime, strftime
import time
from datetime import datetime as dt

path = 'C:/Users/Jaspreet Singh/Desktop/DS_Projects/1a. AQI Prediction/1. Data Collection/Web Scrapers/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get("https://freemeteo.in/weather/new-delhi/history/daily-history/?gid=1261481&date=2018-12-01&station=9764&language=english&country=india")
time.sleep(2)
action = webdriver.ActionChains(driver)

# Inputs
d0 = dt(2018, 12, 1) # -- From Date -- In (YYYY, MM, DD) format -- Change Url according to this date.
d1 = dt(2019, 1, 1) # -- To Date -- In (YYYY, MM, DD) format
delta = d1 - d0
num_of_days = int(delta.days) + 1

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

###############################################################################

# Closing the Ad on page
Next_day_button = driver.find_element_by_css_selector("a[class='next']")
Next_day_button.click()
time.sleep(2)

action.move_by_offset(10, 20)    # 10px to the right, 20px to bottom
action.perform()
action.double_click()
action.perform()
time.sleep(2)  
    
Prev_day_button = driver.find_element_by_css_selector("a[class='prev']")
Prev_day_button.click()
time.sleep(2)

# Scraping Starts Day wise
n = -1
num = 0

for day in range(0,num_of_days):
    
    num += 1
    n += 1
    # It will not click next day on starting page
    if n > 0:
        try:
            Next_day_button = driver.find_element_by_css_selector("a[class='next']")
            Next_day_button.click()
            time.sleep(0.3)
        except:
            # Ad blocked the page
            print("Ad_Blocked_the_Page")
            action.move_by_offset(10, 20)    # 10px to the right, 20px to bottom
            action.perform()
            action.double_click()
            action.perform()
            time.sleep(2)
            
            Next_day_button = driver.find_element_by_css_selector("a[class='next']")
            Next_day_button.click()
            time.sleep(0.3)
            print("Ad_Removed_Successfully")
            print("Resuming_Scraping")
    else:
        pass
    
    try:
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
                            wind_dir = 'N/A'
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
    except:
        try:
            # Sometimes page crashes. It will refersh twice to ensure content comebacks again.
            print("Page_Crashed_Refreshing_it")
            driver.refresh()
            time.sleep(3)
            driver.refresh()
            time.sleep(5)
        
            try:
                Date_ele = driver.find_element_by_css_selector("a[class='cal']")
                Date = Date_ele.text
                Table = driver.find_element_by_css_selector("div[class='table hourly']")
                TRs = Table.find_elements_by_tag_name("tr")
            except:
                # Ad blocked the page
                print("Ad_Blocked_the_Page -")
                action.move_by_offset(10, 20)    # 10px to the right, 20px to bottom
                action.perform()
                action.double_click()
                action.perform()
                time.sleep(2)
            
                Date_ele = driver.find_element_by_css_selector("a[class='cal']")
                Date = Date_ele.text
                Table = driver.find_element_by_css_selector("div[class='table hourly']")
                TRs = Table.find_elements_by_tag_name("tr")
                print("Ad_Removed_Successfully")
            
            print("Page_has_loaded_successfully.")
            print("Resuming_Scraping")
        
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
                                wind_dir = 'N/A'
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
        
        except:
            print("This Page has no content")
            print("Going to next page")
            try:
                Date_ele = driver.find_element_by_css_selector("a[class='cal']")
                Date = Date_ele.text
            except:
                try:
                    # Ad blocked the page
                    print("Ad_Blocked_the_Page -")
                    action.move_by_offset(10, 20)    # 10px to the right, 20px to bottom
                    action.perform()
                    action.double_click()
                    action.perform()
                    time.sleep(2)
            
                    Date_ele = driver.find_element_by_css_selector("a[class='cal']")
                    Date = Date_ele.text
                except:
                    # Even Date is not available on page
                    Date = 'N/A'
                    
            det = 'N/A'
            Date_Time.append(Date)
            Temp.append(det)
            Relative_Temp.append(det)
            Wind_Speed.append(det)
            Wind_Direction.append(det)
            Wind_Gust.append(det)
            Rel_Humidity.append(det)
            Dew_Point.append(det)
            Atmos_Pressure.append(det)
            Description.append(det)
            
    print("Pages Scraped: " + str(num) + " / " + str(num_of_days))
    
###############################################################################    

Output_DF = pd.DataFrame(
    {'Date & Time': Date_Time,
     'Temperature': Temp,
     'Relative_Temp': Relative_Temp,
     'Wind_Speed': Wind_Speed,
     'Wind_Direction': Wind_Direction,
     'Wind_Gust': Wind_Gust,
     'Rel_Humidity': Rel_Humidity,
     'Dew_Point': Dew_Point,
     'Atmospheric_Pressure': Atmos_Pressure,
     'Description': Description
    })

datatoexcel = pd.ExcelWriter('Delhi__Weather_report_June2015-November2021.xlsx')

Output_DF.to_excel(datatoexcel)
datatoexcel.save()
print("File Saved in Excel Format in your system.")

time.sleep(5)
driver.close()    
    