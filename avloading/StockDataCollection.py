"""Module handles the construction of time series objects
for stock data
"""
import datetime
import statistics
import av_loader

class StockTimeSeries:
    """A Collection of stock time instances
    for all time points where data is available
    """
    def __init__(self, company_name, time_diff=None):
        if time_diff != None:
            raise NotImplementedError("Only daily time differential implemented")
        self.data_loader = av_loader.AVLoader(company_name, function=av_loader.AVFunction.DAILY)
        stock_data = self.data_loader.get_stock_data()
        self.time_diff = time_diff
        self.today = TimeInstance(stock_data, str(datetime.date.today()), is_today=True)
        self.series = []
        self.std_vol = 0
        self.std_price = 0
        self.__set_series(stock_data)
        #self.std_vol = statistics.stdev(volumes)
        #self.std_price = statistics.stdev(prices)

    def __set_series(self, stock_data):
        """Populate series with time instances and sets std_vol and std_prices"""
        if self.time_diff != None:
            raise NotImplementedError("Only daily time differential implemented")
        current_day = None

        try:
            current_day = next_day_back(stock_data, datetime.date.today())
        except av_loader.TimeoutException:
            raise IndexError("Stock data is not valid")

        volumes = []
        prices = []
        while True:
            self.series.append(TimeInstance(stock_data, str(current_day)))
            volumes.append(self.series[len(self.series) - 1].info.volume)
            prices.append(self.series[len(self.series) - 1].info.close)
            try:
                current_day = next_day_back(stock_data, current_day)
            except av_loader.TimeoutException:
                break
        self.std_vol = statistics.stdev(volumes)
        self.std_price = statistics.stdev(prices)
        # Configure meta-fields
        for i in range(len(self.series)):
            if i != len(self.series) - 1:
                elt = self.series[i]
                elt.prev = self.series[i + 1]
                elt.prev.will_increase = \
                    elt.info.close > elt.prev.info.close
                elt.std_diff_vol = (elt.info.volume - elt.prev.info.volume) / self.std_vol
                elt.std_diff_price = (elt.info.close - elt.prev.info.close) / self.std_price
        self.today.prev = self.series[0]
        self.series[0].will_increase = \
            self.today.info.close > self.series[0].info.close
        self.today.std_diff_vol = (
            self.today.info.volume - self.today.prev.info.volume) / self.std_vol
        self.today.std_diff_price = (
            self.today.info.close - self.today.prev.info.close) / self.std_price
        self.series.reverse()

    def set_std(self):
        """Set the standard deviation of volumes and prices"""
        pass

    def __str__(self):
        return "Series of " + str(len(self.series)) + " trading days"

class TimeInstance:
    """Represents a single instance of time"""

    def __init__(self, stock_data, time, interval=None, is_today=False):
        self.info = StockInfo(time, stock_data, is_today)
        self.interval = interval
        self.prev = None # Will be updated in collection
        self.will_increase = False # Will be updated in collection
        self.vol_compare = self.info.volume_10day > self.info.volume_3month
        self.mavg_compare = self.info.mavg_50 > self.info.mavg_100 > self.info.mavg_200
        self.std_diff_price = 0 # Will be updated in collection
        self.std_diff_vol = 0 # Will be updated in collection

    def __str__(self):
        return str(self.info)

class StockInfo:
    """Represents information about this stock at a given instance of time"""

    def __init__(self, time, stock_data, is_today=False):

        most_recent = time
        if is_today:
            most_recent = stock_data["Meta Data"]["3. Last Refreshed"]
        date = date_from_time(most_recent)
        now_info = stock_data['Time Series (Daily)'][most_recent]
        self.open = float(now_info["1. open"])
        self.high = float(now_info["2. high"])
        self.low = float(now_info["3. low"])
        self.close = float(now_info["4. close"])
        self.volume = float(now_info["5. volume"])

        mavg_50, mavg_100, mavg_200 = moving_average(
            stock_data, datetime.date(int(date[:4]), int(date[5:7]), int(date[8:])))
        self.mavg_50 = mavg_50
        self.mavg_100 = mavg_100
        self.mavg_200 = mavg_200

        day10vol, day90vol = volume_avg(
            stock_data, datetime.date(int(date[:4]), int(date[5:7]), int(date[8:])))
        self.volume_10day = day10vol
        self.volume_3month = day90vol

    def __str__(self):
        return str((self.open, self.high, self.low, self.close,
                    self.volume, self.mavg_50, self.mavg_100, self.mavg_200,
                    self.volume_10day, self.volume_3month))

def date_from_time(time):
    """Returns the date of a time string that begins with format
    YYYY-MM-DD
    """
    return time[0:10]

def next_day_back(res, curr):
    """Returns the latest day before curr with stock trading data
    """
    now = curr - datetime.timedelta(1)
    counter = 0
    while not str(now) in res['Time Series (Daily)']:
        if counter > 200:
            raise av_loader.TimeoutException("Timeout occured trying to fetch next day back")
        now = now - datetime.timedelta(1)
        counter = counter + 1
    return now

def moving_average(res, today, is_today=False):
    """return the 50, 100, and 200 day moving averages"""
    current_day = today
    days_counted = 0
    total = 0
    if is_today:
        total = total + float(
            res['Time Series (Daily)'][res["Meta Data"]["3. Last Refreshed"]]['4. close'])
        days_counted = days_counted + 1
    elif str(today) in res['Time Series (Daily)']:
        total = total + float(res['Time Series (Daily)'][str(today)]['4. close'])
        days_counted = days_counted + 1
    mavg_50 = 0
    mavg_100 = 0
    mavg_200 = 0
    while days_counted < 200:
        try:
            current_day = next_day_back(res, current_day)
        except av_loader.TimeoutException:
            break
        total = total + float(res['Time Series (Daily)'][str(current_day)]['4. close'])
        days_counted = days_counted + 1
        if days_counted == 50:
            mavg_50 = total / 50
        elif days_counted == 100:
            mavg_100 = total / 100
        elif days_counted == 200:
            mavg_200 = total / 200
    return mavg_50, mavg_100, mavg_200

def volume_avg(res, today):
    """return the 10 day and 90 day volume averages"""
    current_day = today
    days_counted = 0
    total = 0
    day10vol = 0
    day90vol = 0
    while days_counted < 90:
        try:
            current_day = next_day_back(res, current_day)
        except av_loader.TimeoutException:
            break
        total = total + float(res['Time Series (Daily)'][str(current_day)]["5. volume"])
        days_counted = days_counted + 1
        if days_counted == 10:
            day10vol = total / 10
        elif days_counted == 90:
            day90vol = total / 90
    return day10vol, day90vol
