"""
This is a module for loading data from AlphaVantage

"""

import urllib.request
import json
import datetime

TIMESERIES_BASE_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="

URL_TAIL = "&outputsize=full&apikey=U8DGBF2PDMXR2FZT"

class TimeoutException(Exception):
    """Used in conjunction with next_day_back in the case that data doesn't exist past 200 days"""
    pass

def __get_daily_series(company):
    """Obtain daily series for [company] from AlphaVantage"""
    return json.load(urllib.request.urlopen(TIMESERIES_BASE_URL + company + URL_TAIL))


def process_ds_json(res):
    """Returns a python dictionary with relevant fields of the daily series json"""
    pass

def __moving_average(res):
    """Returns the simple moving average of closing price over 50, 100, and 200 days"""
    current_day = datetime.date.today()
    days_counted = 0
    total = 0
    mavg_50 = 0
    mavg_100 = 0
    mavg_200 = 0
    while days_counted < 200:
        # do something
        current_day = __next_day_back(res, current_day)
        total = total + float(res['Time Series (Daily)'][str(current_day)]['4. close'])
        days_counted = days_counted + 1
        if days_counted == 50:
            mavg_50 = total / 50
        elif days_counted == 100:
            mavg_100 = total / 100
        elif days_counted == 200:
            mavg_200 = total / 200
    return mavg_50, mavg_100, mavg_200

def __next_day_back(res, curr):
    """Returns the next date timestamp with data"""
    now = curr - datetime.timedelta(1)
    counter = 0
    while not str(now) in res['Time Series (Daily)']:
        if counter > 200:
            raise TimeoutException("Timeout occured trying to fetch next day back")
        now = now - datetime.timedelta(1)
        counter = counter + 1
    return now

if __name__ == "__main__":
    print(__moving_average(__get_daily_series("GOOG")))
