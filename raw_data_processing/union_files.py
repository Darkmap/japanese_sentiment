import os
import xmltodict, json
from os import listdir
from os.path import isfile, join
fns=[os.path.join(root,fn) for root,dirs,files in os.walk("./") for fn in files]
import xml.etree.ElementTree
ons=[os.path.join(root,fn) for root,dirs,files in os.walk("../output/") for fn in files]
out_file_index = 1
ons = set(ons)
print ons
for fname in fns:
	if fname == "./union_files.py" or fname == "./.DS_Store":
		continue
	outpath = "../output/raw_" + str(out_file_index) + ".txt"
	if outpath in ons:
		continue
	print fname
	f = open(fname, "r")
	xml_str = f.read()
	f.close()
	d = xmltodict.parse(xml_str)
	j = json.dumps(d, ensure_ascii=False).encode("utf8")
	d = eval(j)
	reviews = d["root"]["review"]
	text = ""
	for review in reviews:
		if review.has_key("#text"):
			text += review["#text"] + "\n"

	out = open(outpath, "w")
	out.write(text)
	out.close()
	out_file_index += 1
# print fns

# o = xmltodict.parse('<e> <a>text</a> <a>text</a> </e>')
# print json.dumps(o) # '{"e": {"a": ["text", "text"]}}'
