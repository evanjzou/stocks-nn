from datetime import timedelta
import datetime
import av_loader

class ParsedInfo:
    def __init__(self, info, date, dateString=None):
        self.date = date
        if dateString is None:
            self.dateStr = str(date)

        self.info = info
        self.volume = float(self.info["Time Series (Daily)"][self.dateStr]["5. volume"])
        self.open = float(self.info["Time Series (Daily)"][self.dateStr]["1. open"])
        self.close = float(self.info["Time Series (Daily)"][self.dateStr]["4. close"])
        self.percentChange = (self.close - self.open)/self.open

        mostRecentDate = info["Meta Data"]["3. Last Refreshed"]
        self.currentPrice = float(info["Time Series (Daily)"][mostRecentDate]["4. close"])

        self.__moving_average(self.info)

    def __moving_average(self, res):
        current_day = self.date
        days_counted = 0
        total = 0
        self.mavg_50 = 0
        self.mavg_100 = 0
        self.mavg_200 = 0
        while days_counted < 200:
            # do something

            try:
                current_day = self.__next_day_back(res, current_day)
            except:
                print("Checked past 200 days. Incorrect Moving Averages.")
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
        print(self.mavg_50, self.mavg_100, self.mavg_200)
