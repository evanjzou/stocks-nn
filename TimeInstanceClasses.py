import ParsedInfo
import av_loader
from datetime import timedelta
import datetime
from ParsedInfoClassPlusFields import ParsedInfoWith_mavgFlags
import statistics


class TimeInstanceWithNormalizedData():
    def __init__(self, companyName, unparsedJSON, timeToSearch, stdPrice, stdVol, todaysTI, dateStr=None, previousTimeDiffTI=None):
        self.companyName = companyName
        self.flag = False
        self.timeToSearch = timeToSearch
        self.previousTimeDiffTI = previousTimeDiffTI

        self.saveTodaysTI = todaysTI
        self.saveSTDVol = stdVol
        self.saveSTDPrice = stdPrice

        self.previousTimeDiffPrice = 0

        if dateStr != None:
            dateStr = str(dateStr)

        self.infoSeries = ParsedInfoWith_mavgFlags(unparsedJSON, timeToSearch, dateStr)

        if todaysTI != None:
            self.normalizedVolume = (self.infoSeries.volume - self.infoSeries.vol10Day) / stdVol
            self.normalizedOpen = (self.infoSeries.open - todaysTI.infoSeries.open) / stdPrice
            self.normalizedClose = (self.infoSeries.close - todaysTI.infoSeries.close) / stdPrice
            self.normalizedCurrentPrice = (self.infoSeries.currentPrice - todaysTI.infoSeries.currentPrice)/ stdPrice

    def updateSTD(self, stdVol, stdPrice):
        if self.saveTodaysTI != None:
            self.stdPrice = stdPrice
            self.normalizedVolume = (self.infoSeries.volume - self.infoSeries.vol10Day) / stdVol
            self.normalizedOpen = (self.infoSeries.open - self.saveTodaysTI.infoSeries.open) / stdPrice
            self.normalizedClose = (self.infoSeries.close - self.saveTodaysTI.infoSeries.close) / stdPrice
            self.normalizedCurrentPrice = (self.infoSeries.currentPrice - self.saveTodaysTI.infoSeries.currentPrice) / stdPrice



    def __str__(self):
        # print(self.normalizedCurrentPrice)
        # print(self.normalizedVolume)
        # print(self.normalizedClose)

        print(self.timeToSearch)
        print(self.infoSeries.close)
        print(self.saveTodaysTI.infoSeries.close)
        print(self.stdPrice)

        print(self.normalizedClose)
        print("-------------------------------------")

class TimeInstance:
    ''' has a companyName, a flag, and a timeToSearch '''

    def __init__(self, companyName, unparsedJSON, timeToSearch, dateStr=None, previousTimeDiffTI=None):
        self.companyName = companyName
        self.flag = False
        self.timeToSearch = timeToSearch
        self.previousTimeDiffTI = previousTimeDiffTI

        self.previousTimeDiffPrice = 0

        if dateStr != None:
            dateStr = str(dateStr)
        self.infoSeries = ParsedInfoWith_mavgFlags(unparsedJSON, timeToSearch, dateStr)


        '''
        for x in infoSeries:
            if companyName in infoSeries:
                self.info = infoSeries[x]
        '''

    def __str__(self):
        print(self.normalizedCurrentPrice)
        print(self.normalizedVolume)
        print(self.normalizedClose)
        print("-------------------------------------")

