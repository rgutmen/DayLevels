#!/usr/local/bin/python
from utils import calculateDatesTomorrow, getTodayDBFormat
from config import openingMarketTime, nightReportTime
from datetime import datetime
from Market import Market
import yfinance as yf
import sqlite3
import json

"""
This file is executed using crontab at the end of the sesion, to find out which levels were crossed by the price and store it in the sqlite database.
"""


"""
It fills the array with the values and levels calculated at the opening for each market in the json file.
"""
def fillArray(dataMarkets):
    lista = []
    todayDB = getTodayDBFormat()
    connection_obj = sqlite3.connect('db.sqlite3')
    cursor_obj = connection_obj.cursor()

    for market in dataMarkets:
        mark = Market()
        rowList = cursor_obj.execute('''SELECT * FROM '''+ market.get('tableName') +''' WHERE date = '''+ todayDB +''';''').fetchone()
        rowDict = dict(zip([c[0] for c in cursor_obj.description], rowList))
        
        mark.setDate(todayDB)
        mark.setTicker(market.get('Ticker'))
        mark.setTableName(market.get('tableName'))
        mark.setStdP3(rowDict.get('stdP3'))
        mark.setStdP2(rowDict.get('stdP2'))
        mark.setStdP1(rowDict.get('stdP1'))
        mark.setOpen(rowDict.get('Open'))
        mark.setStdN1(rowDict.get('stdN1'))
        mark.setStdN2(rowDict.get('stdN2'))
        mark.setStdN3(rowDict.get('stdN3'))
        lista.append(mark)
    connection_obj.close()
    return lista

"""
Verify which levels were crossed and store the information in the database.
"""
def checker(markets):
    for market in markets:
        dateTodayStr, timeDiffStr = calculateDatesTomorrow(1)
        df = yf.download(market.getTicker(), start=timeDiffStr, end=dateTodayStr, interval='1m')
        dfRth = df.between_time(openingMarketTime, nightReportTime)
        hi = dfRth['High'].max()
        lo = dfRth['Low'].min()
        if hi > market.getStdP3():
            market.setStdvMaxP(3)
        elif (hi >= market.getStdP2() and hi <= market.getStdP3()):
            market.setStdvMaxP(2)
        elif (hi >= market.getStdP1() and hi <= market.getStdP2()):
            market.setStdvMaxP(1)
        else:
            market.setStdvMaxP(0)

        if lo < market.getStdN3():
            market.setStdvMaxN(3)
        elif (lo <= market.getStdN2() and lo >= market.getStdN3()):
            market.setStdvMaxN(2)
        elif (lo <= market.getStdN1() and lo >= market.getStdN2()):
            market.setStdvMaxN(1)
        else:
            market.setStdvMaxN(0)

        connection_obj = sqlite3.connect('db.sqlite3')
        cursor_obj = connection_obj.cursor()
        cursor_obj.execute('''UPDATE ''' + market.getTableName() +  ''' SET PosX = '''+ str(market.getStdvMaxP()) + \
                                                                    ''', NegX = '''+ str(market.getStdvMaxN()) + \
                                                                    ''' WHERE Date = ''' + str(market.getDate()) +''';''')
        connection_obj.commit()
        connection_obj.close()

"""
Load the json file into an array
"""
def initialization():
    global markets
    with open('markets.json') as f:
        dataMarkets = json.load(f)
    markets = fillArray(dataMarkets)


dateTodayDate = datetime.now()

if __name__ == '__main__':
    initialization()
    checker(markets)


