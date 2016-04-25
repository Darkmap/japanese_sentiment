#!/bin/bash

awk '{print "1 " $0;}' pos_doc_vector.txt > p.txt
awk '{print "-1 " $0;}' neg_doc_vector.txt > n.txt
cat n.txt p.txt > train.txt

