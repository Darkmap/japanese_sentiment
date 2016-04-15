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
    for token in word_v_np:
        tmp_str += str(token)+" "
    return tmp_str

if len(sys.argv) != 2:
    print("Please add \"raw data file\" as arg[1]!")
    sys.exit()

vocab = {}
vocab_file = open("vocabulary")

for line in vocab_file:
    tokens = line.strip().split("\t")
    # print(tokens)
    vocab[tokens[1]] = int(tokens[0])

V = len(vocab)

print("Vocabulary was read!")

mat_file = open("word_vector_model")
u_tmp = []
for i in range(0, V):
    u_tmp.append([])

for line in mat_file:
    tokens = line.strip().split("\t")
    v = 0
    for token in tokens:
        u_tmp[v].append(float(token))
        v += 1

vLen = len(u_tmp[0])

print("U matrix was read!")

raw_file = open(sys.argv[1])

doc_vector_file = open("doc_vector.txt", "w")

lIdx = 0
for line in raw_file:
    print("Start dealing with line: " + str(lIdx))
    tokens = line.strip().split(" ")
    vector = []
    for i in range(0, vLen):
        vector.append(0.0)
    word_v_np = np.array(vector)
    count = 0
    for token in tokens:
        idx = getIdx(vocab, token)
        if idx != -1:
            tmp = np.array(u_tmp[idx])
            word_v_np += tmp
            count += 1
    word_v_np /= count
    doc_vector_file.write(getStr(word_v_np) + "\n")
    lIdx += 1
    print(str(lIdx) + " line completed")


doc_vector_file.close()
