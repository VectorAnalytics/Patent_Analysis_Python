#!/usr/bin/env python

import csv
import re
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk import cluster
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

lemmatizer=WordNetLemmatizer()
#Note: need to download nltk.data before using nltk.corpus and stopwords the first time!


#Prepare set of stopwords that includes "English" and Patent Stopwords
ps = open('PatentStopwordsIII.csv')
csv_ps=csv.reader(ps)
patent_stopwords=[]
for row in csv_ps:
    patent_stopwords.append(row[0])
xx = stopwords.words("english") 
xx.extend(patent_stopwords)
stops = set(xx) 

#Input name of patent dataset you want to analyze.
name1='Power'
name2='Control'
year='2015'
patsys='CPC'
    
#Function that reads Abstracts from CSV file, parses, removes stopwords, lemmatizes    
def parse_abstracts(filename):
    f = open(filename)
    csv_f=csv.reader(f)
    Abstracts=[]
    for row in csv_f:
        Abstracts.append(row[0])    	
    Abstracts_str=' '.join(Abstracts)
    #Clean and remove stopwords from abstracts          
    alpha_only = re.sub("[^a-zA-Z]", " ", Abstracts_str)  
    lower = alpha_only.lower()
    #Split string into tokens of words
    token_verb=word_tokenize(lower)
    #Create an empty list
    token_array_verb=[]
    #For every word in the list, assign it's POS tag as a "v" for verb and lemmatize it as a verb.
    for word in token_verb:
        lemma=lemmatizer.lemmatize(word,"v")
        token_array_verb.append(lemma)
        #For every word in the list, assign it's POS tag as a "n" for noun and lemmatize it as a noun.
        token_array_noun=[]
    for word in token_array_verb:
        lemma=lemmatizer.lemmatize(word,"n")
        token_array_noun.append(lemma)    
    meaningful_words = [w for w in token_array_noun if not w in stops]  
    counter_final_words=Counter(meaningful_words)
    return counter_final_words
    
#Counter function creates a TDM for each corpora
counter_1=parse_abstracts(name1+'_cpc_2015.csv')
counter_2=parse_abstracts(name2+'_cpc_2015.csv')

#all_items creates a set of all unique words used in both counters
all_items=set()
all_items=set(counter_1.keys()).union( set(counter_2.keys()) )

#Create a vector of the counts of all words in each corpora
vector_1=[counter_1[k] for k in all_items]
vector_2=[counter_2[k] for k in all_items]

#Calculate cosine similarities between various corpora
cos_sim = 1-(cluster.util.cosine_distance(vector_1,vector_2))

print('\nCosine Similarity Analysis For',name1,'and',name2, patsys, year,'Patents:')
print('Cosine Simularity = %4.2f'% cos_sim)

