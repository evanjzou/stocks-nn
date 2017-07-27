from neon.data import ArrayIterator
import numpy as np
import math
import bitstring


NUM_EXAMPLES = 100
NUM_FEATURES = 393
NUM_OUTPUTS = 2

#load an array of timeInstance objects
company = collection('GOOG')

#create a 2D array, each row representing a timeseries as an array
X = np.array(timeInstanceToArray(timeInstance) for timeInstance in company)

#create a 2D array of 1hot collumns for buy/sell
yList = []
for timeInstance in company:
    if timeInstance.flag:
        yList.append([0,1])
    else:
        yList.append([1,0])
y = np.array(yList)
y = np.transpose(y)

train = ArrayIterator(X=X, y=y, nclass=2)




def timeInstanceToArray(timeInstance):
    """
    converts a timeInstance to an Array
    :param timeInstance: timeInstance containing relevant stock information
    :return: timeInstance in Array form.
    """
    inputArray = []
# convert timeInstance output to array form and add to inputArray


def floatArray(float):
    """
    covert a float to an array of bits with length 32
    :param float: the input float value
    :return: 32 length array representation of bits in float
    """

    bitarray = []
    f1 = bitstring.BitStream(float=float, length=32)
    result = f1.read('bin')
    return list(f1.read('bin'))
