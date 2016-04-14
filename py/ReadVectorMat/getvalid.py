__author__ = 'qixuanwang'

import sys
import random

origin_file = open(sys.argv[1])
train_file = open(sys.argv[2], "w")
valid_file = open(sys.argv[3], "w")

for line in origin_file:
    num = random.randint(1, 100)
    if num > 10:
        train_file.write(line)
    else:
        valid_file.write(line)

train_file.close()
valid_file.close()
