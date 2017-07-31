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


TRAINING_DURATION_IN_DAYS = 1500
TEST_DURATION_IN_DAYS = 500
TIME_DIFFERENTIAL = 1440
NUM_FEATURES = 393
COMPANY_NAME = 'GOOG'
NUM_OUTPUTS = 2


def timeInstanceToArray(timeInstance):
    """
    converts a timeInstance to an Array
    :param timeInstance: timeInstance containing relevant stock information
    :return: timeInstance in Array form.
    """
    inputArray = []
# convert timeInstance output to array form and add to inputArray
    inputArray += floatArray(timeInstance.volume)
    inputArray += floatArray(timeInstance.currentPrice)
    inputArray += floatArray(timeInstance.mavg_50)
    inputArray += floatArray(timeInstance.mavg_100)
    inputArray += floatArray(timeInstance.mavg_200)

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
    return list(f1.read('bin'))


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
    print(type(companyName))
    company = Collection(companyName, startDate, endDate, timeDifferential)
    timeInstances = company.series

    # create a 2D array, each row representing a timeseries as an array
    X = np.array(timeInstanceToArray(timeInstance) for timeInstance in timeInstances)

    # create a 2D array of 1hot collumns for buy/sell
    yList = []
    for timeInstance in company:

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

# does something, look a t the api
callbacks = Callbacks(mlp, eval_set=test_set, **args.callback_args)


mlp.fit(train_set, optimizer=optimizer, num_epochs=args.epochs, cost=cost,
        callbacks=callbacks)

results = mlp.get_outputs(test_set)


error = mlp.eval(test_set, metric=Misclassification())*100
print('Misclassification error = %.1f%%' % error)