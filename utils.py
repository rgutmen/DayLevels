#!/usr/local/bin/python

from datetime import datetime, timedelta

dateTodayDate = datetime.now()

def date2Str(dateObject):
    """Convert date object to string

    Args:
        dateObject (_type_): _description_

    Returns:
        _type_: _description_
    """    
    return dateObject.strftime('%Y-%m-%d')

def calculateDatesTomorrow(daysBack):
    """Calculate today and yesterday date into string format

    Args:
        daysBack (_type_): _description_

    Returns:
        _type_: _description_
    """    """"""
    dateTodayStr = date2Str(dateTodayDate + timedelta(days=1)) 
    timeDiffStr = date2Str(dateTodayDate + timedelta(days=-daysBack))
    return dateTodayStr, timeDiffStr

def getTodayDBFormat():
    """Format the date with the following format: YYYYMMDD

    Returns:
        _type_: _description_
    """
    return datetime.now().strftime("%Y%m%d")
