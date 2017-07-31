import ParsedInfo
import av_loader
from datetime import timedelta
import datetime


class Collection:
    series = []

    def __init__(self, inCompanyName, inStartDate, inEndDate, inTimeDifferential):
        ''' inTimeDifferential should be in minutes '''
        self.companyName = inCompanyName
        self.startDate = inStartDate
        self.endDate = inEndDate
        self.timeDifferential = inTimeDifferential

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
                myTI = TimeInstance(self.companyName, myTIJSON, secToDate)
                self.addTimeInstance(myTI)

            i = i+1

        self.setFlags()

    def setFlags(self):
        for i in range(0, len(self.series)-1):
            if self.series[i].infoSeries.close < self.series[i+1].infoSeries.close:
                self.series[i].flag = True

    def addTimeInstance(self, timeInstance):

        self.series.append(timeInstance)


class TimeInstance:
    ''' has a companyName, a flag, and a timeToSearch '''

    def __init__(self, companyName, unparsedJSON, timeToSearch):
        self.companyName = companyName
        self.flag = False
        self.timeToSearch = timeToSearch

        self.infoSeries = ParsedInfo.ParsedInfo(unparsedJSON, timeToSearch)

        '''
        for x in infoSeries:
            if companyName in infoSeries:
                self.info = infoSeries[x]
        '''

    def __str__(self):
        print(self.timeToSearch, self.flag)



# def test():
#
#
#
#     # for the third parameter above (the interval) you may need to change it once the AVLoader class is
#     # expanded to actually implement/make use of the interval attribute
#
#
#     testDate1 = datetime.date(2017, 7, 24)
#     testDate2 = datetime.date(2017, 7, 27)
#     testTimeDelta = datetime.timedelta(3)
#     testDiff = 1440
#     testColl = Collection("MSFT", testDate1, testDate2, testDiff)
#
#     testDate = datetime.date(2017, 7, 26)
#     # testTimeInstance = TimeInstance("MSFT", asdf, testDate) # need an actual date object, not a string
#
#
#     # testTimeInstance.infoSeries.__str__()
#
#     for x in testColl.series:
#         x.__str__()
#         x.infoSeries.__str__()
#
#
#
#
#     print("Made it to the end of the test.")
#
# test()