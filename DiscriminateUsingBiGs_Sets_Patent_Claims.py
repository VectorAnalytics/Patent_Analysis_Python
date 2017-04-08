#!/usr/bin/env python
# This code takes two separate corpora (of 2 different sets of patents),
#   creates TDM of each (using bigrams), prints list of top 50 bigrams,
#   then calculates cosine simularity between the 2 sets.
#   It also does extensive lemmization to reduce words to lemma's.
# The input files (2) are two corpora, where each line in the file is a
#   different patent.

import csv
import re
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk import cluster
from nltk import bigrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

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
name1='pattern'
name2='enhance'
patset='_a_cpc_2015.csv'
    
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
        lemma=lemmatizer.lemmatize(word,"a")
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
    string_words=' '.join(meaningful_words)
    return counter_final_words, string_words
    
#Counter function creates a TDM for each corpora
counter_1, words_1=parse_abstracts('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/PSAbstractFiles/'+name1+patset)
counter_2, words_2=parse_abstracts('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/PSAbstractFiles/'+name2+patset)


#collac_1=words_1.collocations()
#print(collac_1)
fdist1=FreqDist(counter_1)
fdist1_top50=fdist1.most_common(50)
print('\nTop 50 Bigram List for',name1)
print(fdist1_top50)
#fdist1.plot(25, cumulative=False)
fdist2=FreqDist(counter_2)
fdist2_top50=fdist2.most_common(50)
print('\nTop 50 BigramList for',name2)
print(fdist2_top50)


#all_items creates a set of all unique words used in both counters
all_items=set()
all_items=set(counter_1.keys()).union( set(counter_2.keys()) )

#Create a vector of the counts of all words in each corpora
vector_1=[counter_1[k] for k in all_items]
vector_2=[counter_2[k] for k in all_items]
#print(vector_2)
#Calculate cosine similarities between various corpora
cos_sim = 1-(cluster.util.cosine_distance(vector_1,vector_2))

print('\nCosine Similarity Analysis For',name1,'and',name2, patset,'Patents:')
print('Cosine Simularity = %4.2f'% cos_sim)

