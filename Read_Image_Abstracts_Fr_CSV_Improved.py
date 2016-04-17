#!/usr/bin/env python

import csv
import re
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk import cluster
from nltk.corpus import stopwords

#Note: need to download nltk.data before using nltk.corpus and stopwords the first time!
patent_lemmatizer=WordNetLemmatizer()

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
name='Image'
    
#Function that reads Abstracts from CSV file, parses, removes stopwords    
def parse_abstracts(filename):
    f = open(filename)
    csv_f=csv.reader(f)
    Abstracts=[]
    for row in csv_f:
        Abstracts.append(row[0])    	
    Abstracts_str=' '.join(Abstracts)
    #Clean and remove stopwords from abstracts          
    alpha_only = re.sub("[^a-zA-Z]", " ", Abstracts_str)  
    lower_alpha_only = alpha_only.lower()
    lemmered_lao = patent_lemmatizer.lemmatize(lower_alpha_only)
    words = lemmered_lao.split()
    counter_all_words=Counter(words)
    meaningful_words = [w for w in words if not w in stops] 
    counter_final_words=Counter(meaningful_words)
    num_pats=len(Abstracts)
    return counter_all_words, counter_final_words, num_pats
    
#Counter function creates a TDM for each corpora
counter_all_2011, counter_2011, num_pats_2011=parse_abstracts(name+'Abstracts_csv_2011.csv')
counter_all_2012, counter_2012, num_pats_2012=parse_abstracts(name+'Abstracts_csv_2012.csv')
counter_all_2014, counter_2014, num_pats_2014=parse_abstracts(name+'Abstracts_csv_2014.csv')
counter_all_2015, counter_2015, num_pats_2015=parse_abstracts(name+'Abstracts_csv_2015.csv')

#Was testing stopword removal with counter     
#counter2=Counter(meaningful_words)

#Lemmatizer is not working!!!!
#patent_lemmatizer=WordNetLemmatizer()
#lemmatized_words = patent_lemmatizer.lemmatize(meaningful_words)
#counter3=Counter(lemmatized_words)

#Union of the counter.keys creates an unique set of all words used across all corpora

#Sean: I got the following error with the statement below
#TypeError: descriptor 'union' requires a 'set'object but received a 'dict_keys'
#all_items=set.union(counter_2011.keys(), counter_2012.keys(), counter_2014.keys(), counter_2015.keys())

all_items=set()
#print all_items
all_items=set(counter_2011.keys()).union( set(counter_2012.keys()) )
#print all_items
all_items=(all_items).union( set(counter_2014.keys()) )
#print all_items
all_items=(all_items).union( set(counter_2015.keys()) )

#Create a vector of the counts of all words in each corpora
vector_2011=[counter_2011[k] for k in all_items]
vector_2012=[counter_2012[k] for k in all_items]
vector_2014=[counter_2014[k] for k in all_items]
vector_2015=[counter_2015[k] for k in all_items]

#Calculate cosine similarities between various corpora
cos_sim_2015and2014 = 1-(cluster.util.cosine_distance(vector_2015,vector_2014))
cos_sim_2015and2011 = 1-(cluster.util.cosine_distance(vector_2015,vector_2011))
cos_sim_2015and2012 = 1-(cluster.util.cosine_distance(vector_2015,vector_2012))
cos_sim_2011and2012 = 1-(cluster.util.cosine_distance(vector_2011,vector_2012))

print('\nCosine Similarity Analysis For',name,'Patents:')
print('Cosine Simularity of 2015 and 2014 = %4.2f'% cos_sim_2015and2014)
print('Cosine Simularity of 2015 and 2011 = %4.2f'% cos_sim_2015and2011)
print('Cosine Simularity of 2015 and 2012 = %4.2f'% cos_sim_2015and2012)
print('Cosine Simularity of 2011 and 2012 = %4.2f'% cos_sim_2011and2012)
print('Number of Patents Per Year = ', num_pats_2011, num_pats_2012, num_pats_2014, num_pats_2015)