__author__ = 'qixuanwang'

import numpy as np
import sys


def getIdx(vocab, word):
    if word in vocab:
        return vocab[word]
    else:
        return -1


def getOneHot(idx, V):
    one_hot_vector = []
    for i in range(0, V):
        one_hot_vector.append([0.0])
    one_hot_vector[idx] = [1.0]
    return one_hot_vector


def getDistributed(idx, U):
    one_hot_np = np.array(getOneHot(idx, V))
    return np.dot(U, one_hot_np)


def getStr(word_v_np):
    tmp_str = ""
    for row in word_v_np:
        tmp_str += str(row[0])+" "
    return tmp_str

if len(sys.argv) != 2:
    print("Please add \"raw data file\" as arg[1]!")
    sys.exit()

vocab = {}
vocab_file = open("vocabulary")

for line in vocab_file:
    tokens = line.strip().split("\t")
    vocab[tokens[1]] = int(tokens[0])

V = len(vocab)

mat_file = open("word_vector_model")
u_tmp = []
for line in mat_file:
    tokens = line.strip().split("\t")
    row = []
    for token in tokens:
        row.append(float(token))
    u_tmp.append(row)
U = np.array(u_tmp)

vLen = len(U)

raw_file = open(sys.argv[1])

doc_vector_file = open("docvector", "w")

lIdx = 0
for line in raw_file:
    tokens = line.strip().split(" ")
    vector = []
    for i in range(0, vLen):
        vector.append([0.0])
    word_v_np = np.array(vector)
    count = 0
    for token in tokens:
        idx = getIdx(vocab, token)
        if idx != -1:
            tmp = getDistributed(idx, U)
            word_v_np += tmp
            count += 1
    word_v_np /= count
    doc_vector_file.write(getStr(word_v_np) + "\n")
    lIdx += 1
    print(str(lIdx) + " line completed")


doc_vector_file.close()
