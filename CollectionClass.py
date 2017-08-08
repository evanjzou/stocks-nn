import ParsedInfo
import av_loader
from datetime import timedelta
import datetime
from ParsedInfoClassPlusFields import ParsedInfoWith_mavgFlags
import statistics
from TimeInstanceClasses import TimeInstanceWithNormalizedData
from TimeInstanceClasses import TimeInstance

#add a std function
#timeout excpetion

class Collection:
    series = []
    avgArray = []
    volArray = []

    def __init__(self, inCompanyName, inStartDate, inEndDate, inTimeDifferential):
        ''' inTimeDifferential should be in minutes '''
        self.companyName = inCompanyName
        self.startDate = inStartDate
        self.endDate = inEndDate
        self.timeDifferential = inTimeDifferential

        self.stdPrice = 0
        self.stdVol = 0

        myTimeDelta = datetime.timedelta()
        myTimeDelta = inEndDate-inStartDate
        totalSeconds = myTimeDelta.total_seconds()

        timeDiffSeconds = inTimeDifferential*60
        # timeDiffSeconds = (datetime.timedelta(self.endDate, self.startDate)).total_seconds()
        # totalSeconds = (self.endDate).total_seconds() - (self.startDate).total_seconds()
        # timeDiffSeconds = (self.timeDifference).total_seconds()
        interval = (totalSeconds / timeDiffSeconds)
        decimalIntervals = interval - int(interval)
        intInterval = int(interval)

        thisTimeDelta = datetime.timedelta()
        yearStartDate = datetime.date(self.startDate.year, 1, 1)
        thisTimeDelta = self.startDate - yearStartDate

        myTIJSON = av_loader.AVLoader(self.companyName, av_loader.AVFunction.DAILY).get_stock_data()
        i = 0
        while i <= intInterval:
            # secsToAdd = (thisTimeDelta.total_seconds() + (i * timeDiffSeconds))
            secsToAdd = i * timeDiffSeconds
            # secToDate = datetime.datetime.fromtimestamp(secsToAdd) # if doesn't work, might be wrong timezone
            secToDate = self.startDate + datetime.timedelta(0, secsToAdd)

            if str(secToDate) in myTIJSON['Time Series (Daily)']:
                previousTimeDiffTI = None
                if i > 0:
                    secsToAdd2 = (i - 1) * timeDiffSeconds
                    secToDate2 = self.startDate + datetime.timedelta(0, secsToAdd2)
                    if str(secToDate2) in myTIJSON['Time Series (Daily)']:
                        previousTimeDiffTI = TimeInstance(self.companyName, myTIJSON, secToDate2)

                myTI = TimeInstance(self.companyName, myTIJSON, secToDate, previousTimeDiffTI=previousTimeDiffTI)
                self.addTimeInstance(myTI)



            i = i + 1

        todaysDate = datetime.date.today()
        yearStart = datetime.date(todaysDate.year, 1, 1)
        secToToday = (todaysDate-yearStart).total_seconds()
        thisDate = yearStart + datetime.timedelta(0, secToToday)

        # thisTime = str(datetime.date.today()) + str(datetime.time.hour) + str(datetime.time.minute)
        # mostRecentDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00")
        mostRecentDateTime = myTIJSON["Meta Data"]["3. Last Refreshed"]
        if mostRecentDateTime in myTIJSON['Time Series (Daily)']:
            self.todaysTI = TimeInstance(self.companyName, myTIJSON, datetime.date.today(), mostRecentDateTime)
        else:
            while not mostRecentDateTime in myTIJSON['Time Series (Daily)']:
                todaysDate = todaysDate - datetime.timedelta(1)


        self.setFlags()
        self.setPriceDiff()
        self.setSTDFields()

    def setFlags(self):
        for i in range(0, len(self.series)-1):
            if self.series[i].infoSeries.close < self.series[i+1].infoSeries.close:
                self.series[i].flag = True
    
    def setPriceDiff(self):
        for i in range(0, len(self.series)-1):
            diff = self.series[i].infoSeries.close - self.series[i+1].infoSeries.close
            self.series[i+1].previousTimeDiffPrice = diff

    def addTimeInstance(self, timeInstance):
        self.series.append(timeInstance)

    def setSTDFields(self):
        for i in self.series:
            self.avgArray.append(i.infoSeries.close)
            self.volArray.append(i.infoSeries.volume)

        self.stdPrice = statistics.stdev(self.avgArray)
        self.stdVol = statistics.stdev(self.volArray)

    def __str__(self):
        print(self.stdPrice)
        print(self.stdVol)


class CollectionForTimeInstanceWithNormalizedData:
    series = []
    avgArray = []
    volArray = []

    def __init__(self, inCompanyName, inStartDate, inEndDate, inTimeDifferential):
        ''' inTimeDifferential should be in minutes '''
        self.companyName = inCompanyName
        self.startDate = inStartDate
        self.endDate = inEndDate
        self.timeDifferential = inTimeDifferential

        self.stdPrice = 1
        self.stdVol = 1

        self.todaysTI = None

        myTimeDelta = datetime.timedelta()
        myTimeDelta = inEndDate - inStartDate
        totalSeconds = myTimeDelta.total_seconds()

        timeDiffSeconds = inTimeDifferential * 60
        # timeDiffSeconds = (datetime.timedelta(self.endDate, self.startDate)).total_seconds()
        # totalSeconds = (self.endDate).total_seconds() - (self.startDate).total_seconds()
        # timeDiffSeconds = (self.timeDifference).total_seconds()
        interval = (totalSeconds / timeDiffSeconds)
        decimalIntervals = interval - int(interval)
        intInterval = int(interval)

        thisTimeDelta = datetime.timedelta()
        yearStartDate = datetime.date(self.startDate.year, 1, 1)
        thisTimeDelta = self.startDate - yearStartDate

        myTIJSON = av_loader.AVLoader(self.companyName, av_loader.AVFunction.DAILY).get_stock_data()


        mostRecentDateTime = myTIJSON["Meta Data"]["3. Last Refreshed"]
        if mostRecentDateTime in myTIJSON['Time Series (Daily)']:
            self.todaysTI = TimeInstanceWithNormalizedData(self.companyName, myTIJSON, datetime.date.today(), self.stdPrice, self.stdVol, None, dateStr=mostRecentDateTime)
        else:
            while not mostRecentDateTime in myTIJSON['Time Series (Daily)']:
                todaysDate = todaysDate - datetime.timedelta(1)

        i = 0
        while i <= intInterval:
            # secsToAdd = (thisTimeDelta.total_seconds() + (i * timeDiffSeconds))
            secsToAdd = i * timeDiffSeconds
            # secToDate = datetime.datetime.fromtimestamp(secsToAdd) # if doesn't work, might be wrong timezone
            secToDate = self.startDate + datetime.timedelta(0, secsToAdd)

            if str(secToDate) in myTIJSON['Time Series (Daily)']:
                previousTimeDiffTI = None
                if i > 0:
                    secsToAdd2 = (i - 1) * timeDiffSeconds
                    secToDate2 = self.startDate + datetime.timedelta(0, secsToAdd2)
                    if str(secToDate2) in myTIJSON['Time Series (Daily)']:
                        previousTimeDiffTI = TimeInstanceWithNormalizedData(self.companyName, myTIJSON, secToDate2,self.stdPrice, self.stdVol, self.todaysTI)

                myTI = TimeInstanceWithNormalizedData(self.companyName, myTIJSON, secToDate,self.stdPrice, self.stdVol, self.todaysTI, previousTimeDiffTI=previousTimeDiffTI)
                self.addTimeInstance(myTI)

            i = i + 1

        todaysDate = datetime.date.today()
        yearStart = datetime.date(todaysDate.year, 1, 1)
        secToToday = (todaysDate - yearStart).total_seconds()
        thisDate = yearStart + datetime.timedelta(0, secToToday)

        # thisTime = str(datetime.date.today()) + str(datetime.time.hour) + str(datetime.time.minute)
        # mostRecentDateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:00")


        self.setFlags()
        self.setPriceDiff()
        self.setSTDFields()
        print("------------")
        print(self.stdPrice)
        print(self.stdVol)
        for i in self.series:
            i.updateSTD(self.stdVol, self.stdPrice)

    def setFlags(self):
        for i in range(0, len(self.series) - 1):
            if self.series[i].infoSeries.close < self.series[i + 1].infoSeries.close:
                self.series[i].flag = True

    def setPriceDiff(self):
        for i in range(0, len(self.series) - 1):
            diff = self.series[i].infoSeries.close - self.series[i + 1].infoSeries.close
            self.series[i + 1].previousTimeDiffPrice = diff

    def addTimeInstance(self, timeInstance):
        self.series.append(timeInstance)

    def setSTDFields(self):
        for i in self.series:
            self.avgArray.append(i.infoSeries.close)
            self.volArray.append(i.infoSeries.volume)

        self.stdPrice = statistics.stdev(self.avgArray)
        self.stdVol = statistics.stdev(self.volArray)



    def __str__(self):
        print("----------------------------")

