import os
import xmltodict, json
from os import listdir
from os.path import isfile, join
fns=[os.path.join(root,fn) for root,dirs,files in os.walk("./") for fn in files]
import xml.etree.ElementTree
out_file_index = 1
for fname in fns:
	if fname == "./union_files.py" or fname == "./.DS_Store" or fname == "gen_dev_data.py":
		continue
	outpath = "../dev_data/raw_" + str(out_file_index) + ".txt"
	if out_file_index <= 740:
		out_file_index += 1
		continue
	f = open(fname, "r")
	xml_str = f.read()
	f.close()
	d = xmltodict.parse(xml_str)
	j = json.dumps(d, ensure_ascii=False).encode("utf8")
	out = open(outpath, "w")
	out.write(j)
	out.close()
	out_file_index += 1
