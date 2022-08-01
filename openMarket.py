from utils import calculateDatesTomorrow, getTodayDBFormat, date2Str
from datetime import datetime, timedelta
from Market import Market
import yfinance as yf
import pandas as pd
import numpy as np
import sqlite3
import math
import json

"""
This file is executed using crontab at the time the CME is opening.
"""
DAYS_BACK = 14

""" 
Round to 0.25, 0.5, 0.75
"""
def roundToQuarter(x):
    if x != np.nan:
        return math.ceil(x*4)/4
    else:
        return 0

"""
Calculate 14 days back from the current date.
"""
def calculateDatesDaysBack():
    daysBack = DAYS_BACK
    currentDay = datetime.now()
    while daysBack > 0:
      currentDay = currentDay - timedelta(1)
      if currentDay.weekday() >= 0 and currentDay.weekday() <= 4:
        daysBack -= 1
    dateTodayStr = date2Str(dateTodayDate)
    timeDiffStr = date2Str(currentDay)
    return dateTodayStr, timeDiffStr

"""
Round the prices, according the market
"""
def roundTo(roundType, valueToRound):
    if roundType == "Zero":
        result = round(valueToRound, 0)
    elif roundType == "TwoPlaces":
        result = round(valueToRound, 2)
    elif roundType == "FourPlaces":
        result = round(valueToRound, 4)
    elif roundType == "Quarter":
        result = roundToQuarter(valueToRound)
    return result

"""
Fill the array with markets objects from the parameters in the json file
"""
def fillArray(markets):
    lista = []
    for market in markets:
        mark = Market()
        mark.setTicker(market.get('Ticker'))
        mark.setRoundTo(market.get('RoundTo'))
        mark.setTableName(market.get('tableName'))
        lista.append(mark)
    return lista

"""
Get the deviation from the range ETH (High-Low)
"""
def getDeviationAndOpening(ticker):
    data1d = pd.DataFrame()
    dateTodayStr, timeDiffStr = calculateDatesDaysBack()
    data1d = yf.download(ticker, start=timeDiffStr, end=dateTodayStr, interval='1m')
    data1d['Range'] = data1d['High'] - data1d['Low']
    data1d['std'] = data1d['Range'].rolling(DAYS_BACK).std()
    data1d['stdDiv2'] = data1d['std']/2

    data1m = pd.DataFrame()
    dateTodayStr, timeDiffStr = calculateDatesTomorrow(1)
    data1m = yf.download(ticker, start=timeDiffStr, end=dateTodayStr, interval='1m')
    data1m = data1m[(data1m.index.day == dateTodayDate.day) & (data1m.index.hour == 9) & (data1m.index.minute == 30)]
    opening = 0
    if len(data1m['Open'].values) == 1:
        opening = data1m['Open'].values[0]

    return data1d.stdDiv2[-1], opening

"""
Get the opening price of the market, and then the deviations are calculated on top and below the price opening
"""
def openingReport(markets):
    listaMsg = []
    for market in markets:
        deviation, openToday = getDeviationAndOpening(market.getTicker())
        todayDB = int(getTodayDBFormat())
        msg = ""
        msg = "{}\n{}\n\n".format((dateTodayDate).strftime('%d-%m-%Y'), market.getMarketName())
        if deviation != 0 and openToday != 0:
            market.setStdP3(roundTo(market.getRoundTo(), openToday + (+3 * deviation)))
            market.setStdP2(roundTo(market.getRoundTo(), openToday + (+2 * deviation)))
            market.setStdP1(roundTo(market.getRoundTo(), openToday + (+1 * deviation)))
          
            market.setOpen(roundTo(market.getRoundTo(), openToday))

            market.setStdN1(roundTo(market.getRoundTo(), openToday + (-1 * deviation)))
            market.setStdN2(roundTo(market.getRoundTo(), openToday + (-2 * deviation)))
            market.setStdN3(roundTo(market.getRoundTo(), openToday + (-3 * deviation)))
            # TODO implementar logs, para registrar los posibles mensajes usar libreria logging
            msg = msg + "stdP3: {}\nstdP2: {}\nstdP1: {}\n\nOpen: {}\n\nstdN1: {}\nstdN2: {}\nstdN3: {}".format(market.getStdP3(), market.getStdP2(), market.getStdP1(), market.getOpen(), \
                                                                                                                market.getStdN1(), market.getStdN2(), market.getStdN3())

            connection_obj = sqlite3.connect('db.sqlite3')            
            cursor_obj = connection_obj.cursor()
            table = '''CREATE TABLE IF NOT EXISTS '''+ market.getTableName() +'''("Id" INTEGER NOT NULL, "Date" INTEGER NOT NULL, "stdP3" REAL, "stdP2" REAL, \
	                "stdP1"	REAL, "Open" REAL, "stdN1" REAL, "stdN2" REAL, "stdN3" REAL, "PosX" INTEGER, "NegX" INTEGER, PRIMARY KEY("Id" AUTOINCREMENT));'''
            cursor_obj.execute(table)
            connection_obj.commit()
            cursor_obj.execute('insert into ' + market.getTableName() + ' (Date, stdP3, stdP2, stdP1, Open, stdN1, stdN2, stdN3) values (?, ?, ?, ?, ?, ?, ?, ?)', 
            (todayDB, market.getStdP3(), market.getStdP2(), market.getStdP1(), market.getOpen(), market.getStdN1(), market.getStdN2(), market.getStdN3()))
            connection_obj.commit()
            
          
            listaMsg.append(msg)
        
            
        elif deviation == 0 and openToday != 0:
            msg = msg + "Error getting/calculating the deviation."
        elif deviation != 0 and openToday == 0:
            msg = msg + "Error getting/calculating the open price."

    connection_obj.close()

"""
Load the json file into an array
"""
def initialization():
    global markets
    with open('markets.json') as f:
        data = json.load(f)
    markets = fillArray(data)


dateTodayDate = datetime.now()
initialization()
openingReport(markets)

