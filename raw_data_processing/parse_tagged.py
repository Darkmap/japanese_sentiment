
def parse(filename):
	f = open(filename, "r")
	lines = f.readlines()
	res = ""
	parsed_line = ""
	for line in lines:
		if line == "EOS\n":
			res += parsed_line + "\n"
			parsed_line = ""
			continue
		else:
			words = line.split(" ")
			if words[0] == '@' and words[1] != '@':
				continue
			parsed_line += words[0] + " "
	f.close()
	return res

for i in range(1, 770):
	final_str = parse(str(i) + ".txt")
	out = open("res/final_" + str(i) + ".txt", "w")
	print "res/final_" + str(i) + ".txt"
	out.write(final_str)
	out.close()