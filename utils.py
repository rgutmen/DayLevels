#!/usr/local/bin/python

from datetime import datetime, timedelta

dateTodayDate = datetime.now()

"""
Convert date object to string
"""
def date2Str(dateObject):
    return dateObject.strftime('%Y-%m-%d')


"""
Calculate today and yesterday date into string format
"""
def calculateDatesTomorrow(daysBack):
    dateTodayStr = date2Str(dateTodayDate + timedelta(days=1)) 
    timeDiffStr = date2Str(dateTodayDate + timedelta(days=-daysBack))
    return dateTodayStr, timeDiffStr

"""
Format the date with the following format: YYYYMMDD
"""
def getTodayDBFormat():
    return datetime.now().strftime("%Y%m%d")
