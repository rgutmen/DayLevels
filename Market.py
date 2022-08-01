#!/usr/local/bin/python
class Market:

    def __init__(self, date="null", ticker = "null", marketName = "null", roundTo = "cero", tableName = "", stdP3 = 0.0, \
                stdP2 = 0.0, stdP1 = 0.0, open = 0.0, stdN1 = 0.0, stdN2 = 0.0, stdN3 = 0.0,  stdvMaxP = 0, stdvMaxN = 0):
        self.date = date
        self.ticker = ticker
        self.marketName = marketName
        self.roundTo = roundTo
        self.tableName = tableName
        self.stdP3 = stdP3
        self.stdP2 = stdP2
        self.stdP1 = stdP1
        self.open = open
        self.stdN1 = stdN1
        self.stdN2 = stdN2
        self.stdN3 = stdN3
        self.stdvMaxP = stdvMaxP
        self.stdvMaxN = stdvMaxN
    
    def clear(self):
        self.setDate("")
        self.setTicker("")
        self.setMarketName("")
        self.setRoundTo("")
        self.setTableName("")
        self.setStdP3(0.0)
        self.setStdP2(0.0)
        self.setStdP1(0.0)
        self.setOpen(0.0)
        self.setStdN1(0.0)
        self.setStdN2(0.0)
        self.setStdN3(0.0)
        self.setStdvMaxP(0)
        self.setStdvMaxN(0)
        
    def getDate(self):
        return self.date
    
    def getTicker(self):
        return self.ticker
    
    def getMarketName(self):
        return self.marketName

    def getRoundTo(self):
        return self.roundTo
    
    def getTableName(self):
        return self.tableName

    def getStdP3(self):
        return self.stdP3

    def getStdP2(self):
        return self.stdP2

    def getStdP1(self):
        return self.stdP1

    def getOpen(self):
        return self.open

    def getStdN1(self):
        return self.stdN1

    def getStdN2(self):
        return self.stdN2

    def getStdN3(self):
        return self.stdN3
  
    def getStdvMaxP(self):
        return self.stdvMaxP

    def getStdvMaxN(self):
        return self.stdvMaxN

    def setDate(self, date):
        self.date = date

    def setTicker(self, ticker):
        self.ticker = ticker

    def setMarketName(self, marketName):
        self.marketName = marketName

    def setRoundTo(self, roundTo):
        self.roundTo = roundTo
    
    def setTableName(self, tableName):
        self.tableName = tableName

    def setStdP3(self, stdP3):
        self.stdP3 = stdP3

    def setStdP2(self, stdP2):
        self.stdP2 = stdP2

    def setStdP1(self, stdP1):
        self.stdP1 = stdP1

    def setOpen(self, open):
        self.open = open

    def setStdN1(self, stdN1):
        self.stdN1 = stdN1

    def setStdN2(self, stdN2):
        self.stdN2 = stdN2

    def setStdN3(self, stdN3):
        self.stdN3 = stdN3

    def setStdvMaxP(self, stdvMaxP):
        self.stdvMaxP = stdvMaxP

    def setStdvMaxN(self, stdvMaxN):
        self.stdvMaxN = stdvMaxN


    def to_dict(self):
        return {
           'Date': self.getDate(),
            'stdP3': self.getStdP3(), 
            'stdP2': self.getStdP2(), 
            'stdP1': self.getStdP1(),
            'Open': self.getOpen(),
            'stdN1': self.getStdN1(),
            'stdN2': self.getStdN2(),
            'stdN3': self.getStdN3(),
            'NegX': self.getStdvMaxN(), 
            'PosX': self.getStdvMaxP()
        }
