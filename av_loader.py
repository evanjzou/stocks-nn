"""
This is a module for loading data from AlphaVantage

"""

import urllib.request
import json
import datetime
import enum

TIMESERIES_BASE_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="

URL_TAIL = "&outputsize=full&apikey=U8DGBF2PDMXR2FZT"

INTRADAY_BASE_URL = "https://www.alphavantage.co/query?" \
    "function=TIME_SERIES_INTRADAY&symbol=MSFT&interval="

class TimeoutException(Exception):
    """Used in conjunction with next_day_back in the case that data doesn't exist past 200 days"""
    pass

class StockData(object):
    """
    A wrapper object representing stock data

    Attributes:

        company: Stock ticker of the company

        mavg_50: 50 day simple moving average

        mavg_100: 100 day simple moving average

        mavg_200: 200 day simple moving average
    """

    def __init__(self, company):
        self.company = company
        self.mavg_50, self.mavg_100, self.mavg_200 = self.__moving_average(
            self.__get_daily_series())


    def __get_daily_series(self):
        return json.load(urllib.request.urlopen(TIMESERIES_BASE_URL + self.company + URL_TAIL))

    def __next_day_back(self, res, curr):
        now = curr - datetime.timedelta(1)
        counter = 0
        while not str(now) in res['Time Series (Daily)']:
            if counter > 200:
                raise TimeoutException("Timeout occured trying to fetch next day back")
            now = now - datetime.timedelta(1)
            counter = counter + 1
        return now

    def __moving_average(self, res):
        current_day = datetime.date.today()
        days_counted = 0
        total = 0
        mavg_50 = 0
        mavg_100 = 0
        mavg_200 = 0
        while days_counted < 200:
            # do something
            current_day = self.__next_day_back(res, current_day)
            total = total + float(res['Time Series (Daily)'][str(current_day)]['4. close'])
            days_counted = days_counted + 1
            if days_counted == 50:
                mavg_50 = total / 50
            elif days_counted == 100:
                mavg_100 = total / 100
            elif days_counted == 200:
                mavg_200 = total / 200
        return mavg_50, mavg_100, mavg_200

    def __str__(self):
        return ("(" + self.company + "," + str(self.mavg_50) + ", "
                + str(self.mavg_100) + ", " + str(self.mavg_200) + ")")


class AVFunction(enum.Enum):
    """Enumeration for the different functions available from the AlphaVantage API"""
    DAILY = 'TIME_SERIES_DAILY'
    INTRADAY = 'TIME_SERIES_INTRADAY'

class TimeDifferential(enum.Enum):
    """Enumeration of the different time differentials at which data can be pulled

    This object is currently not implemented
    """
    def __init__(self):
        raise NotImplementedError("Class not supported yet")


class AVLoader(object):
    """This class loads data from alphavantage based on specified parameters"""

    def __init__(self, company, function, interval=None):
        """function must be a valid AVFunction"""
        self.company = company
        self.function = function
        self.interval = interval

    def get_stock_data(self):
        """Makes and api call to alphavantage and returns a dictionary... [INCOMPLETE]"""
        if self.function == AVFunction.DAILY:
            return json.load(urllib.request.urlopen(TIMESERIES_BASE_URL + self.company + URL_TAIL))
        else:
            raise NotImplementedError("get_stock_data() is not implemented for other functions yet")


if __name__ == '__main__':
    print("\nGetting stock data for Google...")
    print(StockData("GOOG"))
