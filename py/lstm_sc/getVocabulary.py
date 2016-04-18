"""
For getting the vocabulary from origin files
"""
def add_to_dict(word, dict):
    word = word.strip()
    if len(word) >= 1:
        if word in dict:
            dict[word] += 1
        else:
            dict[word] = 1


origin_file = open("10000.txt")

dict ={}

for line in origin_file:
    words = line.strip().split(" ")
    for word in words:
        add_to_dict(word, dict)

dict["</s>"] = 100000

idx = 0

outfile = open("vocabulary", "w")

for w in sorted(dict, key=dict.get, reverse=True):
    outfile.write(str(idx) + "\t" + w + "\n")
    idx += 1

outfile.close()
