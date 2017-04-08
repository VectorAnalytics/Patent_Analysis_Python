#!/usr/bin/env python

import csv
import re
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk import cluster
from nltk import bigrams
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
name='/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/PSAbstractFiles/control_a'
namet='Control Abstract'
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
    token_word=word_tokenize(lower)
    #For every word in the list, assign it's POS tag as a "a" for verb and lemmatize it as a adjective.
    token_adjective=[]    
    for word in token_word:
        lemma=lemmatizer.lemmatize(word,"v")
        token_adjective.append(lemma)    
    #For every word in the list, assign it's POS tag as a "v" for verb and lemmatize it as a verb.
    token_verb=[]    
    for word in token_adjective:
        lemma=lemmatizer.lemmatize(word,"v")
        token_verb.append(lemma)
    #For every word in the list, assign it's POS tag as a "n" for noun and lemmatize it as a noun.
    token_noun=[]
    for word in token_verb:
        lemma=lemmatizer.lemmatize(word,"n")
        token_noun.append(lemma)    
    meaningful_words = [w for w in token_noun if not w in stops]
    pat_bigrams=bigrams(meaningful_words)
    counter_final_words=Counter(pat_bigrams)
    return counter_final_words
    
#Counter function creates a TDM for each corpora
counter_cpc_2015=parse_abstracts(name+'_cpc_2015.csv')
counter_cpc_2014=parse_abstracts(name+'_cpc_2014.csv')
counter_cpc_2013=parse_abstracts(name+'_cpc_2013.csv')
counter_cpc_2012=parse_abstracts(name+'_cpc_2012.csv')
counter_uspc_2013=parse_abstracts(name+'_uspc_2013.csv')
counter_uspc_2012=parse_abstracts(name+'_uspc_2012.csv')

#all_items creates a set of all unique words used in both counters
all_items=set()
all_items=set(counter_cpc_2015.keys()).union( set(counter_cpc_2014.keys()) )
all_items=(all_items).union( set(counter_cpc_2013.keys()) )
all_items=(all_items).union( set(counter_cpc_2012.keys()) )
all_items=(all_items).union( set(counter_uspc_2013.keys()) )
all_items=(all_items).union( set(counter_uspc_2012.keys()) )

#Create a vector of the counts of all words in each corpora
vector_cpc_2015=[counter_cpc_2015[k] for k in all_items]
vector_cpc_2014=[counter_cpc_2014[k] for k in all_items]
vector_cpc_2013=[counter_cpc_2013[k] for k in all_items]
vector_cpc_2012=[counter_cpc_2012[k] for k in all_items]
vector_uspc_2013=[counter_uspc_2013[k] for k in all_items]
vector_uspc_2012=[counter_uspc_2012[k] for k in all_items]

#Calculate cosine similarities between various corpora
cos_sim_cpc2015_cpc2014 = 1-(cluster.util.cosine_distance(vector_cpc_2015,vector_cpc_2014))
cos_sim_cpc2013_uspc2013 = 1-(cluster.util.cosine_distance(vector_cpc_2013,vector_uspc_2013))
cos_sim_cpc2012_uspc2012 = 1-(cluster.util.cosine_distance(vector_cpc_2012,vector_uspc_2012))
cos_sim_uspc2012_uspc2013 = 1-(cluster.util.cosine_distance(vector_uspc_2012,vector_uspc_2013))

print('\nCosine Similarity Analysis For',namet,'Patents:')
print('Cosine Simularity of 2015 CPC and 2014 CPC = %4.2f'% cos_sim_cpc2015_cpc2014)
print('Cosine Simularity of 2013 CPC and 2013 USPC = %4.2f'% cos_sim_cpc2013_uspc2013)
print('Cosine Simularity of 2012 CPC and 2012 USPC = %4.2f'% cos_sim_cpc2012_uspc2012)
print('Cosine Simularity of 2012 USPC and 2013 USPC = %4.2f'% cos_sim_uspc2012_uspc2013)
