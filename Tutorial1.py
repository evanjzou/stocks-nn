from neon.util.argparser import NeonArgparser
from neon.data import MNIST, ArrayIterator
from neon.initializers import Gaussian
from neon.layers import Affine, GeneralizedCost
from neon.transforms import Rectlin, Softmax, CrossEntropyMulti, Misclassification
from neon.models import Model
from neon.optimizers import GradientDescentMomentum
from neon.callbacks.callbacks import Callbacks

parser = NeonArgparser(__doc__)
args = parser.parse_args()

mnist = MNIST()
(X_train, y_train), (X_test, y_test), nclass = mnist.load_data()

train_set = ArrayIterator(X_train, y_train, nclass=nclass)
test_set = ArrayIterator(X_test, y_test, nclass=nclass)
print(nclass)
#print('x_test = ' + X_test)

init_norm = Gaussian(loc=0.0, scale=0.01)

layers = []
layers.append(Affine(nout=100, init=init_norm, activation=Rectlin()))
layers.append(Affine(nout=10, init=init_norm,
                     activation=Softmax()))
mlp = Model(layers = layers)
cost = GeneralizedCost(costfunc=CrossEntropyMulti())
optimizer = GradientDescentMomentum(0.1, momentum_coef=0.9)
callbacks = Callbacks(mlp, eval_set=test_set, **args.callback_args)

mlp.fit(train_set, optimizer=optimizer, num_epochs=args.epochs, cost=cost,
        callbacks=callbacks)


results = mlp.get_outputs(test_set)
# evaluate the model on test_set using the misclassification metric
error = mlp.eval(test_set, metric=Misclassification())*100
print('Misclassification error = %.1f%%' % error)