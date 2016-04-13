__author__ = 'qixuanwang'


def read_mat(mfile, vocabfile, matfile):

    layer1_size = 0
    V = 0

    while 1:
        line = mfile.readline().strip()

        if line.startswith("hidden layer size:"):
            layer1_size = int(line.split(":")[1].strip())
        elif line.startswith("vocabulary size:"):
            V = int(line.split(":")[1].strip())
        elif line == "Vocabulary:":
            break

    for i in range(0, V):
        tokens = mfile.readline().strip().split("\t")
        vocabfile.write(tokens[0]+"\t"+tokens[2]+"\n")

    while 1:
        line = mfile.readline().strip()
        if line == "Weights 0->1:":
            break

    for i in range(0, layer1_size):
        for j in range(0, V):
            token = mfile.readline().strip()
            matfile.write(token+"\t")
        for k in range(0, layer1_size):
            mfile.readline()
        matfile.write("\n")


model_file = open("model")
vocabulary_file = open("vocabulary", "w")
out_file = open("word_vector_model", "w")

read_mat(model_file, vocabulary_file, out_file)

model_file.close()
out_file.close()
