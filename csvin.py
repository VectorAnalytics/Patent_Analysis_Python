#!/usr/bin/env python

import csv
with open('pats_all_power.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	corpus = {}
	for row in reader:
		corpus[row[-1]] = corpus.get(row[-1],[]) + [row[21]]
		print row[21]
             
