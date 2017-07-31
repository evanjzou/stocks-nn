# assume "info" is an object of a class with relevant stock data over a certain time instance

class TimeInstance:
    def __init__(self, companyName, infoSeries):
        self.flag = False

        for x in infoSeries:
            if companyName in infoSeries:
                info = infoSeries[companyName]



class Collection:
    self._series = []

    def __init__(self, companyName):
        self.companyName = companyName
        
    def addTimeInstance(self, timeInstance):
        self.series.append(timeInstance)

    def _init_(self, inCompanyName, inStartDate, inEndDate, inTimeDifference):
        self.companyName = inCompanyName
        self.startDate = inStartDate
        self.endDate = inEndDate
        self.timeDifference = inTimeDifference
        
        totalSeconds = (self.endDate).total_seconds() - (self.startDate).total_seconds()
        timeDiffSeconds = (self.timeDifference).total_seconds()
        interval = (totalSeconds/ timeDiffSeconds)
        decimalIntervals = interval- int(interval)
        intInterval = int(interval)
        

        i = 0
        while i <= intInterval
                secsToAdd = ((self.startDate).total_seconds() + (i*timeDiffSeconds))
                secToDate = datetime.datetime.fromtimestamp(secsToAdd)
                addTimeInstance(secToDate)



        


def main():
    print("This code works!")
    
main()


class ParsedInfo:
    
    """takes a JSON named 'info' which is 'info' from the time instance class
    and gets stock attribures from it using the 'date' parameter 
    
    Attributes:
        volume
        open
        close
        percent change (during one day)
        currentPrice: as of now this uses the closing price
    """

    def _init_(self, info, date):
    
    #constructor that sets the given fields from the "imput" parameter
        dateStr = str(date)
        info = info
        self.volume = info['Time Series (Daily)'][dateStr]['5. volume']
        self.open = info['Time Series (Daily)'][dateStr]['1. open']
        self.close = info['Time Series (Daily)'][dateStr]['4. close']
        self.percentChange = (self.close - self.open)/ self.open
        
        ##current price currently uses the "last refreshed" field from "Meta Data" on alpha vantage
        mostRecentDate = info['Meta Data']['3. Last Refreshed']
        self.currentPrice = info['Time Series (Daily)'][mostRecentDate]['4. close']

    def __str__ (self) :
        print  self.volume


