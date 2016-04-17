positive = ""
negative = ""

for i in range(1, 400):
	fraw = open("raw_" + str(i) + ".txt", "r")
	ffinal = open("final_" + str(i) + ".txt", "r")
	rjson = fraw.read()
	d = eval(rjson)
	flines = ffinal.readlines()
	reviews = d["root"]["review"]
	for k in range(len(flines)):
		if reviews[k]["@rating"] == "5.0":
			positive += flines[k]
		elif reviews[k]["@rating"] == "1.0" or reviews[k]["@rating"] == "2.0":
			negative += flines[k]
	fraw.close()
	ffinal.close()


outp = open("positive.txt", 'w')
outn = open("negative.txt", 'w')
outp.write(positive)
outn.write(negative)
outp.close()
outn.close()
