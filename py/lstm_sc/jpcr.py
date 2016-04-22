"""
This python program is adapted by following the tutorial (http://deeplearning.net/tutorial/lstm.html).

This program is used for loading the Japanese customer reviews dataset which crawled by LGM team for the usage of research
about building language model base on LSTM (https://github.com/Darkmap/japanese_sentiment).
"""

from __future__ import print_function
import numpy
import theano
import random

def prepare_data(seqs, labels):
    """
    Create the matrices from the datasets.

    Firstly, each sequence is processed to be the same length:
        the length of the longuest sequence or maxlen.

    This swap the axises
    :param seqs is the list of sentences
    :param labels is the list of 0/1 labels
    """
    lens = [len(s) for s in seqs]

    size = len(seqs)
    max_len = numpy.max(lens)

    # For this part's algorithm analysis, you can check an article (http://www.cnblogs.com/neopenx/p/4806006.html)
    # if you can read Chinese :).
    sentences = numpy.zeros((max_len, size)).astype('int64')
    sentences_mask = numpy.zeros((max_len, size)).astype(theano.config.floatX)

    for idx, s in enumerate(seqs):
        sentences[:lens[idx], idx] = s
        sentences_mask[:lens[idx], idx] = 1.

    return sentences, sentences_mask, labels


def load_helper(train_set, path, label, vocab):
    """
    For loading different types of train and test data.
    :param train_set: the two-dimensional list for storing training set
    :param path: the data file path
    :param label: the label for this specific file, because we store the reviews with same label in the same file
    :param vocab: the vocabulary dict
    """
    file = open(path)

    for line in file:
        sample = []
        words = line.strip().split(" ")
        for word in words:
            if word in vocab:
                sample.append(vocab[word])
        if len(sample) == 0:
            continue
        else:
            train_set[0].append(sample)
            train_set[1].append(label)


def load_data(valid_portion=0.1):
    """
    Method for Loading the dataset
    :param path: The path to the dataset (here Japanese Customer Reviews)
    :param valid_portion: The proportion of the full train set used for
        the validation set.
    """

    # Get the Vocabulary  which is a dict contains (word:index) entries
    vocab_file = open("vocabulary")
    vocab = {}
    for line in vocab_file:
        tokens = line.strip().split("\t")
        vocab[tokens[1]] = int(tokens[0])

    # Load train_set and test_set
    # train/test_set[0] is the list of documents. The document is represented as [idx0, idx1, ... ,idxn].
    # train/test_set[1] is the list of labels. For the label, 0 is negative, 1 is positive.
    train_set = ([],[])
    load_helper(train_set, "positive_train.txt", 1, vocab)
    load_helper(train_set, "negative_train.txt", 0, vocab)
    test_set = ([], [])
    load_helper(test_set, "positive_test.txt", 1, vocab)
    load_helper(test_set, "negative_test.txt", 0, vocab)

    # Select some reviews from training to create validation set
    train_set_x, train_set_y = train_set
    size = len(train_set_x)

    train_x = []
    train_y = []
    valid_x = []
    valid_y = []

    thred = int(100 * valid_portion)
    for idx in range(0, size):
        gen = random.randint(1, 100)
        if gen <= thred:
            valid_x.append(train_set_x[idx])
            valid_y.append(train_set_y[idx])
        else:
            train_x.append(train_set_x[idx])
            train_y.append(train_set_y[idx])

    train_set = (train_x, train_y)
    valid_set = (valid_x, valid_y)

    return train_set, valid_set, test_set
