# assume "info" is an object of a class with relevant stock data over a certain time instance

class TimeInstance:
    def __init__(self, companyName, infoSeries):
        flag = False

        for x in infoSeries:
            if companyName in infoSeries:
                info = infoSeries[companyName]



class Collection:
    series = []

    def __init__(self, companyName):
        companyName = companyName
        
    def addTimeInstance(self, timeInstance):
        series.append(timeInstance)

def main():
    print("This code works!")
    
main()
