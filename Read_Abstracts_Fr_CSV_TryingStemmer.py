#!/usr/bin/env python

import csv
import re
from collections import Counter
from nltk.stem import WordNetLemmatizer
from nltk import cluster
from nltk.corpus import stopwords
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
  
wordnet_tag ={'NN':'n','JJ':'a','VB':'v','RB':'r','VBN':'v','VBD':'v',
    'VBG':'v','VBZ':'v','NNS':'n','VBP':'v','CD':'n','IN':'n','MD':'n',
    'JJR':'a','JJS':'a','DT':'n','RBR':'r','PRP':'n','CC':'n','WRB':'n',
    'PRP$':'n','RP':'r','WP$':'n','PDT':'n','WDT':'n','WP':'n','LS':'n'
}
 
 
# Lemmatizer and POS tagger to fit each word based on its POS
#require wordnet_tag
def lemmatize_words_array(words_array):
    lemmatizer = nltk.stem.WordNetLemmatizer()
    tagged = nltk.pos_tag(words_array)
    lemmatized_words_array = [];
    for word in tagged:
        lemma = lemmatizer.lemmatize(word[0],wordnet_tag[word[1]])
        lemmatized_words_array.append(lemma)
    return lemmatized_words_array
  
#Read 2011 Abstracts from CSV file    
f = open('PowerAbstracts_csv_2011.csv')
csv_f=csv.reader(f)
Abstracts_2011=[]
for row in csv_f:
    Abstracts_2011.append(row[0])    	
Abstracts_str_2011=' '.join(Abstracts_2011)

#Clean and return stopwords from 2011 abstracts          
alpha_only_2011 = re.sub("[^a-zA-Z]", " ", Abstracts_str_2011)  
words_2011 = alpha_only_2011.lower().split()
#Was testing stopword removal with counter   
#counter1=Counter(words)
meaningful_words_2011 = [w for w in words_2011 if not w in stops] 
#Was testing stopword removal with counter     
#counter2=Counter(meaningful_words)

patent_lemmatizer=WordNetLemmatizer()
lemmatized_words_2011 = patent_lemmatizer.lemmatize({(meaningful_words_2011)})

#Read 2012 Abstracts from CSV file    
g = open('PowerAbstracts_csv_2012.csv')
csv_g=csv.reader(g)
Abstracts_2012=[]
for row in csv_g:
    Abstracts_2012.append(row[0])    	
Abstracts_str_2012=' '.join(Abstracts_2012)

#Clean and return stopwords from 2012 abstracts          
alpha_only_2012 = re.sub("[^a-zA-Z]", " ", Abstracts_str_2012)  
words_2012 = alpha_only_2012.lower().split()
#Was testing stopword removal with counter   
#counter1=Counter(words)
meaningful_words_2012 = [w for w in words_2012 if not w in stops] 

#Read 2014 Abstracts from CSV file    
h = open('PowerAbstracts_csv_2014.csv')
csv_h=csv.reader(h)
Abstracts_2014=[]
for row in csv_h:
    Abstracts_2014.append(row[0])    	
Abstracts_str_2014=' '.join(Abstracts_2014)

#Clean and return stopwords from 2014 abstracts          
alpha_only_2014 = re.sub("[^a-zA-Z]", " ", Abstracts_str_2014)  
words_2014 = alpha_only_2014.lower().split()
#Was testing stopword removal with counter   
#counter1=Counter(words)
meaningful_words_2014 = [w for w in words_2014 if not w in stops] 

#Read 2015 Abstracts from CSV file    
j = open('PowerAbstracts_csv_2015.csv')
csv_j=csv.reader(j)
Abstracts_2015=[]
for row in csv_j:
    Abstracts_2015.append(row[0])    	
Abstracts_str_2015=' '.join(Abstracts_2015)

#Clean and return stopwords from 2015 abstracts          
alpha_only_2015 = re.sub("[^a-zA-Z]", " ", Abstracts_str_2015)  
words_2015 = alpha_only_2015.lower().split()
#Was testing stopword removal with counter   
#counter1=Counter(words)
meaningful_words_2015 = [w for w in words_2015 if not w in stops] 

#Counter function creates a TDM for each corpora
counter_2011=Counter(meaningful_words_2011)
counter_2012=Counter(meaningful_words_2012)
counter_2014=Counter(meaningful_words_2014)
counter_2015=Counter(meaningful_words_2015)

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

print('\nCosine Simularity of 2015 and 2014 = %4.2f'% cos_sim_2015and2014)
print('\nCosine Simularity of 2015 and 2011 = %4.2f'% cos_sim_2015and2011)
print('\nCosine Simularity of 2015 and 2012 = %4.2f'% cos_sim_2015and2012)
print('\nCosine Simularity of 2011 and 2012 = %4.2f'% cos_sim_2011and2012)