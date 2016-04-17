#!/usr/bin/env python
# -*- coding: utf-8 -*-

vectors = dict()

def load_vectors(filename):
	f = open(filename, "r")
	f.readline()
	for line in f:
		array = line.split(" ")
		vector = []
		word = array[0]
		for i in range(1, 201):
			vector.append(float(array[i]))
		vectors[word] = vector
	f.close()

def sentence2vec(sentence):
	words = sentence.strip().split(" ")
	sentence_vec = [0 for i in range(200)]
	word_count = 0
	for word in words:
		if vectors.has_key(word):
			word_count += 1
			vec_plus(sentence_vec, vectors[word])
	if word_count == 0:
		return None
	for i in range(200):
		sentence_vec[i] = sentence_vec[i] / word_count
	return sentence_vec

def vec_plus(vec1, vec2):
	res_vec = []
	for i in range(len(vec1)):
		vec1[i] = vec1[i] + vec2[i]

def process_one_file(infile, outfile, tag):
	out_str = ""
	input_file = open(infile, "r")
	for line in input_file:
		sentence_vec = sentence2vec(line)
		if sentence_vec == None:
			continue
		out_str += str(tag)
		for i in range(200):
			out_str += " " + str(sentence_vec[i])
		out_str += "\n"
	input_file.close()
	output_file = open(outfile, "a")
	output_file.write(out_str)
	output_file.close()

load_vectors("vectors.txt")
process_one_file("5000positive.txt", "sentence_vectors_with_tags.txt", 1)
process_one_file("5000negative.txt", "sentence_vectors_with_tags.txt", -1)
