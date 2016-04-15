__author__ = 'qixuanwang'

neg_file = open("5000negative_vector.txt")
pos_file = open("5000positive_vector.txt")

out_file = open("rnn_train.txt", "w")
for line in pos_file:
    out_file.write("1 " + line)
for line in neg_file:
    out_file.write("-1 " + line)

out_file.close()