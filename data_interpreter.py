from neon.data import ArrayIterator
import numpy as np
import math
import bitstring
from CollectionClass import Collection
from datetime import date, timedelta
from neon.initializers.initializer import Gaussian
from neon.layers import Affine
from neon.transforms import Rectlin, Softmax
from neon.models import Model
from neon.layers import GeneralizedCost
from neon.transforms import CrossEntropyMulti
from neon.optimizers import GradientDescentMomentum
from neon.callbacks.callbacks import Callbacks
from neon.transforms import Misclassification
from neon.util.argparser import NeonArgparser

TRAINING_DURATION_IN_DAYS = 500
TEST_DURATION_IN_DAYS = 500
TIME_DIFFERENTIAL = 1440
NUM_FEATURES = 393
COMPANY_NAME = 'GOOGL'
NUM_OUTPUTS = 2


#enables customization with flags
parser = NeonArgparser(__doc__)
args = parser.parse_args()

def timeInstanceToArray(timeInstance):
    inputArray = []
    # convert timeInstance output to array form and add to inputArray
    inputArray += floatArray(timeInstance.infoSeries.volume)
    inputArray += floatArray(timeInstance.infoSeries.currentPrice)
    inputArray += floatArray(timeInstance.infoSeries.mavg_50)
    inputArray += floatArray(timeInstance.infoSeries.mavg_100)
    inputArray += floatArray(timeInstance.infoSeries.mavg_200)
    inputArray += floatArray(timeInstance.infoSeries.vol10Day)
    inputArray += floatArray(timeInstance.infoSeries.vol3Month)
    if timeInstance.infoSeries.volCompare:
        inputArray += [1]
    else:
        inputArray += [0]
    if timeInstance.infoSeries.mavgCompare:
        inputArray += [1]
    else:
        inputArray+= [0]
    return inputArray

def timeInstanceToArray(timeInstance):
    """
    creates an array of bits given a specific time instance
    :param timeInstance: a timeInstance object
    :return: an array of bits representing the time instance
    """

    inputArray = []
    # convert timeInstance output to array form and add to inputArray
    inputArray += floatArray(timeInstance.infoSeries.volume)
    inputArray += floatArray(timeInstance.infoSeries.currentPrice)
    inputArray += floatArray(timeInstance.infoSeries.mavg_50)
    inputArray += floatArray(timeInstance.infoSeries.mavg_100)
    inputArray += floatArray(timeInstance.infoSeries.mavg_200)

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


def createArrayIterator(companyName, startDate, endDate, timeDifferential):
    """
    creates an array iterator for training/testing
    :param companyName: the company being evaluated
    :param startDate: the earliest date used by the iterator
    :param endDate: the latest date used by the iterator
    :param timeDifferential: the amount of time between time instances being
                             evaluated
    :return: an ArrayIterator usable by the neural network
    """

    # load an array of timeInstance objects
    company = Collection(companyName, startDate, endDate, timeDifferential)
    timeInstances = company.series

    # create a 2D array, each row representing a timeseries as an array
    XList = []
    for timeInstance in timeInstances:
        XList.append(timeInstanceToArray(timeInstance))
    X = np.array(XList)

    # create a 2D array of 1hot collumns for buy/sell
    yList = []
    for timeInstance in timeInstances:

        # flag needs to be set
        if timeInstance.flag:
            yList.append([0,1])
        else:
            yList.append([1,0])
    y = np.array(yList)


    return ArrayIterator(X=X, y=y, nclass=NUM_OUTPUTS)


# create timeDeltas of testDuration and trainingDuration
trainingDuration = timedelta(days = TRAINING_DURATION_IN_DAYS)
testDuration = timedelta(days = TEST_DURATION_IN_DAYS)

# find the start date and end date for the training and test
# data based on their durations
trainStartDate = date.today() - (trainingDuration + testDuration)
trainEndDate = date.today() - (testDuration + timedelta(days=1))
testStartDate = date.today() - testDuration
testEndDate = date.today() - timedelta(days=1)

# creates an array iterator for the training data and test data
train_set = createArrayIterator(COMPANY_NAME, trainStartDate,\
                            trainEndDate, TIME_DIFFERENTIAL)
test_set = createArrayIterator(COMPANY_NAME, testStartDate,\
                            testEndDate, TIME_DIFFERENTIAL)

#initializes the weights of the neurons
init_norm = Gaussian(loc=0.0, scale=0.01)

# creating initial layers
layers = []
layers.append(Affine(nout=100, init=init_norm, activation=Rectlin()))
layers.append(Affine(nout=NUM_OUTPUTS, init=init_norm,
                     activation=Softmax()))

# sets up a model with the provided layers
mlp = Model(layers=layers)

# specifies cost function to use with neural network
cost = GeneralizedCost(costfunc=CrossEntropyMulti())

# uses stochastic gradient descent with learning rate of 0.1 and momentum
# coefficient of 0.9
optimizer = GradientDescentMomentum(0.1, momentum_coef=0.9)

# sets up progress bars
callbacks = Callbacks(mlp, eval_set=test_set, **args.callback_args)

# puts the model together
mlp.fit(train_set, optimizer=optimizer, num_epochs=args.epochs, cost=cost,
        callbacks=callbacks)

# tests the model with a specific test set
results = mlp.get_outputs(test_set)


error = mlp.eval(test_set, metric=Misclassification())*100
print('Success Rate = %.1f%%' % (100 - error))

# # show today's prediction
# company = Collection(COMPANY_NAME, trainStartDate, date.today(), TIME_DIFFERENTIAL)
# today = np.array(timeInstanceToArray(company.today))
# todaysData = ArrayIterator(today, None, nclass=NUM_OUTPUTS)
# classes = ["sell", "buy"]
# out = mlp.get_outputs(todaysData)
# print(classes[out[0].argmax()] + " %.1f%%" % out[0].amax)
#



