import data_interpreter as di
from neon.util.argparser import NeonArgparser

def testTimeInstanceToArray():
    ts = di.StockTimeSeries('GOOG')
    ti = ts.series[200]
    print(di.timeInstanceToArray(ti))
    print(ti.dayOfWeek)


def testCreateArrayIterator():

    company = di.StockTimeSeries('GOOG')
    print("Training Data")
    di.createArrayIterator(company, (di.TRAINING_DURATION_IN_DAYS + \
                                di.TEST_DURATION_IN_DAYS), di.TEST_DURATION_IN_DAYS, True)
    print("Test Data")
    di.createArrayIterator(company, di.TEST_DURATION_IN_DAYS, -len(company.series), True)

testCreateArrayIterator()
