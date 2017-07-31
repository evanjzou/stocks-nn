__author__ = 'johnphilmurray'
from neon.data import ArrayIterator
from neon.backends import gen_backend
from neon.data import NervanaDataIterator
import numpy as np

NUM_FEATURES = 201
NUM_EXAMPLES = 1000
NUM_OUTPUTS = 2

#initialize a numpy array
X_train = np.random.rand(NUM_EXAMPLES, NUM_FEATURES)
y_train = np.random.rand(NUM_EXAMPLES, NUM_OUTPUTS)


class StockData(NervanaDataIterator):

    def __init__(self, X, Y, lshape):

        self.X = X / 255
        self.Y = Y
        self.shape = lshape
        self.start = 0
        self.ndata = X.shape[0]
        self.nfeatures = X.shape[1]

        self.nbatches = self.ndata / self.be.bsz