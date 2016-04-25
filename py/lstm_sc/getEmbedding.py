"""
This file is used to get word embedding parameters from the trained LSTM model (model.npz)
"""

from __future__ import print_function
import six.moves.cPickle as pickle

from collections import OrderedDict
import sys
import time

import numpy
import theano
from theano import config
import theano.tensor as tensor
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams

# import dataset loading module
import jpcr


def load_params(path, params):
    pp = numpy.load(path)
    for kk, vv in params.items():
        if kk not in pp:
            raise Warning('%s is not in the archive' % kk)
        params[kk] = pp[kk]

    return params


def init_params(options):
    """
    Global (not LSTM) parameter. For the embedding and the classifier.
    """
    params = OrderedDict()

    # embedding
    randn = numpy.random.rand(options['n_words'], options['dim_proj'])
    params['Wemb'] = (0.01 * randn).astype(config.floatX)

    # Init the LSTM parameter:
    # Such concatenate is designed for the parallel computing
    W = numpy.concatenate([ortho_weight(options['dim_proj']),
                           ortho_weight(options['dim_proj']),
                           ortho_weight(options['dim_proj']),
                           ortho_weight(options['dim_proj'])], axis=1)
    params['lstm_W'] = W

    # Such concatenate is designed for the parallel computing
    U = numpy.concatenate([ortho_weight(options['dim_proj']),
                           ortho_weight(options['dim_proj']),
                           ortho_weight(options['dim_proj']),
                           ortho_weight(options['dim_proj'])], axis=1)
    params['lstm_U'] = U

    b = numpy.zeros((4 * options['dim_proj']))
    params['lstm_b'] = b.astype(config.floatX)

    # Logistic regression classifier
    params['U'] = 0.01 * numpy.random.randn(options['dim_proj'], options['ydim']).astype(config.floatX)
    params['b'] = numpy.zeros((options['ydim'],)).astype(config.floatX)

    return params

def ortho_weight(ndim):
    W = numpy.random.randn(ndim, ndim)
    u, s, v = numpy.linalg.svd(W)
    return u.astype(config.floatX)

def getWordEmbedding(
    dim_proj=128,  # word embeding dimension and LSTM number of hidden units.
    dispFreq=100,  # Display to stdout the training progress every N updates
    lrate=0.0001,  # Learning rate for sgd (not used for adadelta and rmsprop)
    n_words=16000,  # Vocabulary size
    saveto='model.npz',  # The best model will be saved there
    batch_size=16,  # The batch size during training.
    valid_batch_size=64,  # The batch size used for validation/test set.
):

    # Model options
    model_options = locals().copy()

    load_data = jpcr.load_data
    prepare_data = jpcr.prepare_data

    # Loading train, valid, and test data
    train, valid, test = load_data(valid_portion=0.05)

    # Label range (for this problem, only {0,1})
    model_options['ydim'] = 2

    # This create the initial parameters as numpy ndarrays.
    # Dict name (string) -> numpy ndarray
    params = init_params(model_options)

    load_params('model_save/model.npz', params)

    wemb = params['Wemb']

    wemb_file = open("word_embedding.txt", "w")

    for row in wemb:
        for col in row:
            wemb_file.write(str(col)+"\t")
        wemb_file.write("\n")

    wemb_file.close()


if __name__ == '__main__':
    getWordEmbedding()