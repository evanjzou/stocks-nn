from datetime import timedelta
import datetime
import av_loader

class ParsedInfoWith_mavgFlags():
    def __init__(self, info, date, dateStr=None):
        self.date = date
        if dateStr is None:
            self.dateStr = str(date)
        else:
            self.dateStr = dateStr
        self.info = info
        self.volume = float(self.info["Time Series (Daily)"][self.dateStr]["5. volume"])
        self.open = float(self.info["Time Series (Daily)"][self.dateStr]["1. open"])
        self.close = float(self.info["Time Series (Daily)"][self.dateStr]["4. close"])
        self.percentChange = (self.close - self.open)/self.open
        self.currentPrice = 0


        mostRecentDate = datetime.date.today()

        while not dateStr in info['Time Series (Daily)']:
            mostRecentDate = mostRecentDate - datetime.timedelta(1)
            dateStr = str(mostRecentDate)

        mostRecentDate = info["Meta Data"]["3. Last Refreshed"]
        self.currentPrice = float(self.info["Time Series (Daily)"][mostRecentDate]["4. close"])
        #         self.currentPrice = float(self.info["Time Series (Daily)"][mostRecentDate]["4. close"])
        #         self.todaysVolume = float(self.info["Time Series (Daily)"][mostRecentDate]["5. volume"])
        #         self.todaysOpen = float(self.info["Time Series (Daily)"][mostRecentDate]["1. open"])
        #         self.todaysClose = float(self.info["Time Series (Daily)"][mostRecentDate]["4. close"])

        self.__moving_average(self.info)
        self.__find10Day3MonthVol(self.info)

        self.mavgCompare = self.set_mavgCompare()
        self.volCompare = self.set_volumeCompare()



    def set_mavgCompare(self):
        if self.mavg_50 > self.mavg_100 and self.mavg_100 > self.mavg_200 and self.mavg_50 > self.mavg_200:
            return True
        else:
            return False
    
    def set_volumeCompare(self):
        if self.vol10Day > self.vol3Month:
            return True
        else:
            return False

    def __find10Day3MonthVol(self, res):
        current_day = self.date
        days_counted = 0
        total = 0
        self.vol10Day = 0
        self.vol3Month = 0

        while days_counted < 90:
            # do something

            current_day = self.__next_day_back(res, current_day)
            # current_day = current_day - datetime.timedelta(1)

            total = total + float(res['Time Series (Daily)'][str(current_day)]['5. volume'])
            days_counted = days_counted + 1
            if days_counted == 10:
                self.vol10Day = total / 10
             
            elif days_counted == 90: #90 days = 3 months
                self.vol3Month = total / 90


    def __moving_average(self, res):
        current_day = self.date
        days_counted = 0
        total = 0
        self.mavg_50 = 0
        self.mavg_100 = 0
        self.mavg_200 = 0
        while days_counted < 200:
            # do something

            current_day = self.__next_day_back(res, current_day)
            # current_day = current_day - datetime.timedelta(1)

            total = total + float(res['Time Series (Daily)'][str(current_day)]['4. close'])
            days_counted = days_counted + 1
            if days_counted == 50:
                self.mavg_50 = total / 50
            elif days_counted == 100:
                self.mavg_100 = total / 100
            elif days_counted == 200:
                self.mavg_200 = total / 200
        # return mavg_50, mavg_100, mavg_200

    def __next_day_back(self, res, curr):
        now = curr - datetime.timedelta(1)
        counter = 0
        while not str(now) in res['Time Series (Daily)']:
            if counter > 200:
                raise av_loader.TimeoutException("Timeout occured trying to fetch next day back")
            now = now - datetime.timedelta(1)
            counter = counter + 1
        return now

    def __str__(self):
        print(self.close)
        # print(str(self.vol10Day), str(self.vol3Month), '\n'+str(self.volCompare))
