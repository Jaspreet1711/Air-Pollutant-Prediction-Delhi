# -*- coding: utf-8 -*-
"""
Created on Tue Dec  7 13:09:21 2021

@author: Jaspreet Singh
"""

import pandas as pd
import datetime


dt = datetime.datetime(2015, 6, 1)
end = datetime.datetime(2021, 12, 1, 00, 00, 00)
step = datetime.timedelta(minutes=30)

Date_Time = []

while dt < end:
    Date_Time.append(dt.strftime('%Y-%m-%d %H:%M:%S'))
    dt += step
    
Output_DF = pd.DataFrame(
    {'Date & Time': Date_Time
     })

datatoexcel = pd.ExcelWriter('Calender_Jun2015-Nov2021.xlsx')

Output_DF.to_excel(datatoexcel)
datatoexcel.save()