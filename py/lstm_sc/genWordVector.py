"""
This file is used to generate the training and testing set in the LSTM-based word embedding
"""
import numpy as np

def getStr(word_v_np):
    tmp_str = ""
    for token in word_v_np:
        tmp_str += str(token)+" "
    return tmp_str

def getIdx(vocab, word):
    if word in vocab:
        return vocab[word]
    else:
        return -1

vocab = {}
vocab_file = open("vocabulary")

for line in vocab_file:
    tokens = line.strip().split("\t")
    # print(tokens)
    vocab[tokens[1]] = int(tokens[0])

V = len(vocab)

embeddings = []
embed_file = open("word_embedding.txt")

for line in embed_file:
    tokens = line.strip().split("\t")
    list = []
    for token in tokens:
        list.append(float(token))
    embeddings.append(list)

# raw_file = open("5000positive.txt")
# doc_vector_file = open("pos_doc_vector.txt", "w")

raw_file = open("5000negative.txt")
doc_vector_file = open("neg_doc_vector.txt", "w")

lIdx = 0
for line in raw_file:
    print("Start dealing with line: " + str(lIdx))
    tokens = line.strip().split(" ")
    vector = []
    for i in range(0, len(embeddings[0])):
        vector.append(0.0)
    word_v_np = np.array(vector)
    count = 0
    for token in tokens:
        idx = getIdx(vocab, token)
        if idx != -1:
            tmp = np.array(embeddings[idx])
            word_v_np += tmp
            count += 1
    word_v_np /= count
    if count > 0:
        doc_vector_file.write(getStr(word_v_np) + "\n")
    lIdx += 1
    print(str(lIdx) + " line completed")


doc_vector_file.close()














print("completed")
