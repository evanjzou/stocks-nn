import ParsedInfo
import av_loader
from datetime import timedelta
import datetime
from ParsedInfoClassPlusFields import ParsedInfoWith_mavgFlags
import statistics
from TimeInstanceClasses import TimeInstance
from CollectionClass import CollectionForTimeInstanceWithNormalizedData

# def test():
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
#     # testTimeInstance.infoSeries.__str__()
#
#     for x in testColl.series:
#         x.__str__()
#         x.infoSeries.__str__()
#
#     testColl.todaysTI.__str__()
#     testColl.todaysTI.infoSeries.__str__()
#
#     print("Made it to the end of the test.")
#
#
# def test():
#     # for the third parameter above (the interval) you may need to change it once the AVLoader class is
#     # expanded to actually implement/make use of the interval attribute
#
#
#     testDate1 = datetime.date(2017, 7, 24)
#     testDate2 = datetime.date(2017, 7, 27)
#     testTimeDelta = datetime.timedelta(3)
#     testDiff = 1440
#     testColl = CollectionForTimeInstanceWithNormalizedData("MSFT", testDate1, testDate2, testDiff)
#
#     testDate = datetime.date(2017, 7, 26)
#     # testTimeInstance = TimeInstance("MSFT", asdf, testDate) # need an actual date object, not a string
#
#     testColl.__str__()
#     # testTimeInstance.infoSeries.__str__()
#     #
#     for x in testColl.series:
#        x.__str__()
#         # x.infoSeries.__str__()
#
#     print("Made it to the end of the test.")
#
# test()