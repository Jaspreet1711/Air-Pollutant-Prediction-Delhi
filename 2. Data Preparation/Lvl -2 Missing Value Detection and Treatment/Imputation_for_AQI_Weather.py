# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 12:06:07 2021

@author: Jaspreet Singh
"""
import pandas as pd
import datetime as dt

# For continous variables
# -- This function will be taking average of previous and next variable(non null) of the missing variable.
# -- As we have hourly data, So taking average will become more logical.
# -- For Example if 3:00 Pm data is missing but we have 2:00pm and 4:00 pm. The average of both 2 and 4 pm will give the reliable value for 3:00 pm data 
# -- We have applied the condition if data is missing for large period (or Hours), then function will impute monthly average (which means that non none cells have large numbers of rows in between).

def imputate_mv(df, col, tim_col):
    col = str(col)
    df[col+'_isnull'] = df[col].isnull()
    ls = df[col+'_isnull'].tolist()
    ls1 = []
    c = -1
    for i in ls:
        c += 1
        if i == False:
            ls1.append(0)
        else:
            if len(ls1) == 0:
                ls1.append(1)
            else:
                if ls1[c-1] > 0:
                    ls1.append(ls1[c-1] + 1)
                else:
                    ls1.append(1)
        
    dataframe = df[[tim_col, col, col+'_isnull']]
    dataframe[tim_col] = pd.to_datetime(dataframe[tim_col], dayfirst=True) 
    dataframe['count_True'] = ls1
    n = -1
    dt1 = dataframe[tim_col]
    lst = dataframe[col].tolist()
    lst1 = dataframe[col+'_isnull'].tolist()
    lst2 = dataframe['count_True'].tolist()
    for i in lst:
        n += 1
        if n == 0:
            if lst2[n] == 1:
                lst.pop(n)
                lst.insert(n, 0)
            else:
                pass
        elif (n == len(lst2)-1 or n == len(lst2)):
            try:
                if lst2[n] > 0:
                    lst.pop(n)
                    lst.insert(n, 0)
                else:
                   pass
            except:
                pass
        else:
            if (lst2[n] > lst2[n-1] and lst2[n+1] == 0):
                val = (lst[n-1] + lst[n+1])/2
                lst.pop(n)
                lst.insert(n, val)
            elif (lst2[n] > lst2[n-1] and lst2[n+1] > lst2[n]):
                a = lst[n-1]
                l = lst2[n:]
                c = l.index(0)
                b = lst[n+c]
                if (c < 211 and lst2[n] < 211):
                    if (c < 13 and lst2[n] < 13):
                        val = (a + b)/2
                        lst.pop(n)
                        lst.insert(n, val)
                    else:
                        dataframe_monthly = dataframe.groupby(pd.PeriodIndex(dt1, freq="M"))[col].mean().reset_index()
                        dataframe_monthly[tim_col] = dataframe_monthly[tim_col].astype(str)
                        
                        # Takeout Month and year from dt1
                        # Match that with dataframe_monthly
                        try:
                            d = str(str(dt1[n].year)+'-'+dt1[n].strftime('%m'))
                            val = dataframe_monthly.loc[dataframe_monthly[tim_col] == d, col].iloc[0]
                            lst.pop(n)
                            lst.insert(n, val)
                        except:
                            pass
                else:
                    pass
            else:
                pass
    dataframe[col] = lst
    df[col] = lst
    df = df.drop(col+'_isnull', 1)

# Get number of hours out of a date
def hours(td):
    return int(td.seconds//3600)

# For Discrete Variables
# -- Average will not make sense here as data is discrete in nature.
# -- We will be imputing weather conditions (like Rainy, Clear, Thunder, etc.) so time will become crucial as weather condition changes quickly.
# -- This function will impute last condition (or Last Hour(s)) in the missing cell.
# -- If missing cell and last cell has more than 2 hours of gap then it will not impute.
# -- Also, if data is missing for large period (or Hours) it will leave all the missing cells (which means that non none cells have large numbers of rows in between)

def imputate_dummy(df, col, tim_col):
    df[tim_col] = pd.to_datetime(df[tim_col], dayfirst=True)
    df[col+'_isnull'] = df[col].isnull()
    ls = df[col+'_isnull'].tolist()
    ls1 = []
    c = -1
    for i in ls:
        c += 1
        if i == False:
            ls1.append(0)
        else:
            if len(ls1) == 0:
                ls1.append(1)
            else:
                if ls1[c-1] > 0:
                    ls1.append(ls1[c-1] + 1)
                else:
                    ls1.append(1)
    
    dataframe = df[[tim_col, col, col+'_isnull']]
    dataframe[tim_col] = pd.to_datetime(dataframe[tim_col], dayfirst=True) 
    dataframe['count_True'] = ls1
    n = -1
    dt1 = dataframe[tim_col].tolist()
    lst = dataframe[col].tolist()
    lst1 = dataframe[col+'_isnull'].tolist()
    lst2 = dataframe['count_True'].tolist()                
    for i in lst:
        n += 1
        if n == 0:
            if lst2[n] == 1:
                lst.pop(n)
                lst.insert(n, 0)
            else:
                pass
        elif (n == len(lst2)-1 or n == len(lst2)):
            try:
                if lst2[n] > 0:
                    lst.pop(n)
                    lst.insert(n, 0)
                else:
                   pass
            except:
                pass
        else:
            d = dt1[n] - dt1[n-1] 
            h = hours(d)
            # if data is missing for more than 2 hours then it will not impute as it will reduce our precision and will more rely on assumptions
            if (lst2[n] > lst2[n-1] and lst2[n+1] == 0 and h < 3):
                val = lst[n-1]
                lst.pop(n)
                lst.insert(n, val)
            elif (lst2[n] > lst2[n-1] and lst2[n+1] > lst2[n]):
                a = lst[n-1]
                l = lst2[n:]
                c = l.index(0)
                if (c < 8 and lst2[n] < 8 and h < 3):
                    val = a
                    lst.pop(n)
                    lst.insert(n, val)
                else:
                    pass
            else:
                pass
    dataframe[col] = lst
    df[col] = lst
    df = df.drop(col+'_isnull', 1)    
   
    