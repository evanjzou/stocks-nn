from neon.data import ArrayIterator
import numpy as np
import math
import bitstring
from CollectionClass import CollectionForTimeInstanceWithNormalizedData
from datetime import date, timedelta
from neon.initializers.initializer import Gaussian
from neon.layers import Affine
from neon.transforms import Rectlin, Explin, Normalizer, Tanh, Logistic, Softmax
from neon.models import Model
from neon.layers import GeneralizedCost
from neon.transforms import CrossEntropyMulti
from neon.optimizers import GradientDescentMomentum
from neon.callbacks.callbacks import Callbacks
from neon.transforms import Misclassification
from avloading.StockDataCollection import StockTimeSeries
from neon.util.argparser import NeonArgparser

TRAINING_DURATION_IN_DAYS = 1500
TEST_DURATION_IN_DAYS = 500
TIME_DIFFERENTIAL = 1440
NUM_FEATURES = 393
COMPANY_NAME = 'PYPL'
NUM_OUTPUTS = 2

#enables customization with flags
parser = NeonArgparser(__doc__)
args = parser.parse_args()

def boolToInt(bool):
    if bool:
        return 1
    else:
        return -1


def floatToFractionalBinary(float):
    """
    convert the left and right side of the decimal point each
    to binary, and write them into a set of 64 inputs
    :param float: the float being converted to fractional binary
    format
    :return: a 64 item array of 1s and 0s representing the bits
    of the fractional binary representation
    """
    fracBin = []
    left = int(float)
    right = float - left
    while left > 0:
        fracBin.append(left - (2*(left//2)))
        left = left//2
    while len(fracBin) < 32:
        fracBin = [0] + fracBin
    while len(fracBin) < 64:
        rightInt = right*2
        fracBin.append(rightInt)
        right = right - rightInt
    return fracBin


def timeInstanceToArray(timeInstance):
    """
    convert a time instance object to an array of input values
    :param timeInstance: the timeInstance object being converted
    :return: array of input values, consisting of low valued floats
    """
    inputArray = []
    inputArray += tiToArrayFloat(timeInstance)
    inputArray += tiToArrayFloat(timeInstance.prev)
    inputArray.append(boolToInt(timeInstance.vol_compare))
    inputArray.append(boolToInt(timeInstance.mavg_compare))
    dayOfWeek = [0,0,0,0,0]
    dayOfWeek[timeInstance.dayOfWeek-1] = 1
    inputArray += dayOfWeek
    return inputArray

def tiToArray(ti):
    """
    converts numeric values of a time instance into an input array using their
    standard deviation
    :param ti: time instance being used
    :return: array representation of the numeric values within the time instance
    """
    inputArray = []
    inputArray.append(ti.std_diff_mavg50)
    inputArray.append(ti.std_diff_mavg100)
    inputArray.append(ti.std_diff_mavg200)
    inputArray.append(ti.std_diff_vol)
    inputArray.append(ti.std_diff_price)
    return inputArray

def tiToArrayFracBin(ti):
    """
    converts numeric values of a time instance into an input array using their
    fractional binary representations
    :param ti: time instance being used
    :return: array representation of the numeric values within the time instance
    """
    inputArray = []
    inputArray += floatToFractionalBinary(ti.mavg_50)
    inputArray += floatToFractionalBinary(ti.mavg_100)
    inputArray += floatToFractionalBinary(ti.mavg_200)
    inputArray += floatToFractionalBinary(ti.info.volume_10day)
    inputArray += floatToFractionalBinary(ti.info.volume_3month)
    return inputArray

def tiToArrayFloat(ti):
    """
    converts numeric values of a time instance into an input array using their
    ieee float representations
    :param ti: time instance being used
    :return: array representation of the numeric values within the time instance
    """
    inputArray = []
    inputArray += floatArray(ti.mavg_50)
    inputArray += floatArray(ti.mavg_100)
    inputArray += floatArray(ti.mavg_200)
    inputArray += floatArray(ti.info.volume_10day)
    inputArray += floatArray(ti.info.volume_3month)

    return inputArray

def floatArray(float):
    """
    covert a float to an array of bits with length 32
    :param float: the input float value
    :return: 32 length array representation of bits in float
    """

    bitarray = []
    f1 = bitstring.BitStream(float=float, length=32)
    result = f1.read('bin')
    return list(result)


def createArrayIterator(company, start, end, test=False):
    """
    creates an array iterator for training/testing
    :param company: a collection object representing the company being evaluated
    :param start: the starting point index
    :param endDate: the ending point index
    :return: an ArrayIterator usable by the neural network
    """

    # load an array of timeInstance objects
    timeInstances = company.series[start:end]

    # create a 2D array, each row representing a timeseries as an array
    # create a 2D array of 1hot collumns for buy/sell
    XList = []
    yList = []
    for timeInstance in timeInstances:
        XList.append(timeInstanceToArray(timeInstance))
        if timeInstance.will_increase:
            yList.append([0,1])
        else:
            yList.append([1,0])
    if test:
        print("X length")
        print(len(XList))
        print("Y length")
        print(len(yList))
    X = np.array(XList)


    # flag needs to be set
    y = np.array(yList)
    return ArrayIterator(X=X, y=y, nclass=NUM_OUTPUTS)

def run():


    companyName = input('Enter Stock Ticker:')
    # create timeDeltas of testDuration and trainingDuration
    trainingDuration = timedelta(days = TRAINING_DURATION_IN_DAYS)
    testDuration = timedelta(days = TEST_DURATION_IN_DAYS)

    # find the start date and end date for the training and test
    # data based on their durations
    trainStartDate = date.today() - (trainingDuration + testDuration)
    trainEndDate = date.today() - (testDuration + timedelta(days=1))
    testStartDate = date.today() - testDuration
    testEndDate = date.today() - timedelta(days=1)

    # creates a new stock time series object
    company = StockTimeSeries(companyName)

    # creates an array iterator for the training data and test data
    train_set = createArrayIterator(company, -(TRAINING_DURATION_IN_DAYS + \
                                TEST_DURATION_IN_DAYS), -TEST_DURATION_IN_DAYS)

    test_set = createArrayIterator(company, -TEST_DURATION_IN_DAYS, len(company.series))

    #initializes the weights of the neurons
    init_norm = Gaussian(loc=0.0, scale=0.01)

    # creating initial layers
    layers = []
    layers.append(Affine(nout=88, init=init_norm, activation=Logistic()))
    layers.append(Affine(nout=NUM_OUTPUTS, init=init_norm,
                     activation=Softmax()))

    # sets up a model with the provided layers
    mlp = Model(layers=layers)

    # specifies cost function to use with neural network
    cost = GeneralizedCost(costfunc=CrossEntropyMulti())

    # uses stochastic gradient descent with learning rate of 0.1 and momentum
    # coefficient of 0.9
    optimizer = GradientDescentMomentum(.1, momentum_coef=0.9)

    print("Evaluating " + companyName)
    # sets up progress bars
    callbacks = Callbacks(mlp, eval_set=test_set, **args.callback_args)

    # puts the model together
    mlp.fit(train_set, optimizer=optimizer, num_epochs=args.epochs, cost=cost,
            callbacks=callbacks)

    # tests the model with a specific test set
    results = mlp.get_outputs(test_set)


    error = mlp.eval(test_set, metric=Misclassification())*100
    print('Success Rate = %.1f%%' % (100 - error))

    # show today's prediction
    today = timeInstanceToArray(company.today)
    x_new = np.zeros((TEST_DURATION_IN_DAYS, len(today)), dtype=np.int)
    x_new[0] = np.array(today)
    todaysData = ArrayIterator(x_new, None, nclass=NUM_OUTPUTS)
    classes = ["sell", "buy"]
    out = mlp.get_outputs(todaysData)
    print(classes[out[0].argmax()] + " %.1f%%" % (100 * np.amax(out[0])))


if __name__ == '__main__':
    run()

