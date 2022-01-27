# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 16:37:11 2021

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
driver.get("https://www.tomtom.com/en_gb/traffic-index/new-delhi-traffic/")
driver.maximize_window()

time.sleep(2)
cookie_decline = driver.find_element_by_css_selector("button[class='CookieBar__button']")
cookie_decline.click()

time.sleep(10)
# -- Quickly scroll down to circles tray on the browser that is open.

# Output
Date = []
Congestion = []

# Selecting previous year comparison tab
tab = driver.find_element_by_css_selector("div[class='CityAggregated']")
py_sec = tab.find_element_by_css_selector("li[class='Tabs__tab']")
py_tab = py_sec.find_element_by_tag_name("div")
py_tab.click() 
time.sleep(3)

# Finding Circles in webpage
data_tray = driver.find_element_by_css_selector("svg[class='DailyCongestionChart__svg']")
circles = data_tray.find_elements_by_tag_name("circle") 
n = len(circles)
c = 0

print("We have congestion data for "+str(n)+" days of current year. Each day is represented by indivdual circle on the webpage.")
print(" ")
print("Size of the circle represent traffic congestion size(refer webpage for more details).")
print(" ")

for circle in circles:
    hover = ActionChains(driver).move_to_element(circle)
    hover.perform()
    time.sleep(1)
    try:
        data = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='CityAggregated__tooltip']"))
            )
    except:
        print("Y")
        hover.perform()
        time.sleep(2)
        data = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='CityAggregated__tooltip']"))
            )
    c += 1
    l = data.text.split()
    date = str(l[1]+' '+l[2]+' '+l[3])
    congestion = l[10]
    Date.append(date)
    Congestion.append(congestion)
    print("Circle(s) Scraped: "+str(c)+" / "+str(n))
    print(" ")
    
Output_DF = pd.DataFrame(
    {'Date': Date, 
     '2020 Difference from 2019 in congestion': Congestion
     })

datatoexcel = pd.ExcelWriter('Delhi_Traffic_Congestion_Data_2019.xlsx')
Output_DF.to_excel(datatoexcel)
datatoexcel.save()

time.sleep(5)
driver.close()