import random

# title = "positive"
title = "negative"

origin = open("5000" + title + ".txt")
train = open(title+"_train.txt", "w")
test = open(title+"_test.txt", "w")

for line in origin:
    gen = random.randint(1,100)
    if gen <= 20:
        test.write(line)
    else:
        train.write(line)

test.close()
train.close()