#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import sys
import re
from collections import Counter
#from nltk.stem import WordNetLemmatizer
from nltk import cluster
from nltk.corpus import stopwords
 
#Read 2011 Abstracts from CSV file    
#f = open('PowerAbstracts_csv_2011.csv')
#csv_f=csv.reader(f)
 

        
f=open('C:/Users/mprice79/claims_2015.csv', newline='', encoding='utf8')
reader=csv.reader(f, delimiter=",")
next(reader, None) #skip the headers
for row in reader:
    pat_num=row[0]
    claims=row[1]
#data=list(reader)
#row_count=len(data)
#print(row_count)
#csv_f=csv.reader(f)
#Abstracts_2011=[]
#for row in csv_f:
#    Abstracts_2011.append(row[0])    	
#Abstracts_str_2011=' '.join(Abstracts_2011)

#Clean and return stopwords from 2011 abstracts          
#alpha_only_2011 = re.sub("[^a-zA-Z]", " ", Abstracts_str_2011)  
#words_2011 = alpha_only_2011.lower().split()
#Was testing stopword removal with counter   
#counter1=Counter(words)
#meaningful_words_2011 = [w for w in words_2011 if not w in stops] 
