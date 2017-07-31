class ParsedInfo:
    
    """takes a JSON named 'info' which is 'info' from the time instance class
    and gets stock attribures from it using the 'date' parameter """

    def _init_(self, info, date):
        dateStr = str(date)
        self.info = info
        self.volume = info['Time Series (Daily)'][dateStr]['5. volume']
        self.open = info['Time Series (Daily)'][dateStr]['1. open']
        self.close = info['Time Series (Daily)'][dateStr]['4. close']
        self.percentChange = (self.close - self.open)/ self.open
        
        ##current price is currently equal to the closing price
        self.currentPrice = info['Time Series (Daily)'][dateStr]['4. close']