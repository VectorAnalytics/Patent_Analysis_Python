#!/usr/bin/env python
# Code To Perform Topic Modelling With Gensim LDA Model
# Marcia Price, March 9, 2017
# Python 3.5 
import csv
import re
import pandas as pd
import gensim
#from collections import Counter
from nltk.stem import WordNetLemmatizer
#from nltk import cluster
from nltk import bigrams, trigrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
#from nltk.tokenize import RegexpTokenizer
#from nltk.probability import FreqDist
from gensim import corpora, models
#from gensim.corpora import Dictionary

lemmatizer=WordNetLemmatizer()
#Note: need to download nltk.data before using nltk.corpus and stopwords the first time!

#Prepare set of stopwords that includes "English" and special stopwords.
# This list of special stopwords include the last 16 I added that made 
#   significant improvement in using cosine to discriminate between patent sets.
ps = open('PatentStopwordsIII.csv')
csv_ps=csv.reader(ps)
patent_stopwords=[]
for row in csv_ps:
    patent_stopwords.append(row[0])
xx = stopwords.words("english") 
xx.extend(patent_stopwords)
stops = set(xx) 

#Read in the list of docs you want to perform topic modeling on.
#Input file is a csv with first row of headers: doc_set, doc_id, doc_content.
doclist_df = pd.read_csv('power_all_wid.csv',
                         keep_default_na=False, na_values=[""])
#Look at first five docs in df to see cols names and make sure the read it working.
print(doclist_df.head())

#Put just the content in a df.
content=doclist_df.doc_content
all_ngrams=[]
#Loop through the doc list doc by doc.
for i in content:
    #Put all characters into lowercase.
     lower=i.lower()
     #Only keep alpha (delete punc and numbers).
     alpha_only = re.sub("[^a-zA-Z]", " ", lower) 
     #Split string into tokens of single unigram words.
     token_word=word_tokenize(alpha_only)
 #Setup variables and conduct lemmatization. 
     #I lemmatize as an adjective, noun, and verb sequentially, so all unigrams
     # are reduced as much as possible. Lemmatizing to an adverb I can't get to work. 
     lemma=[]   
     lemma_token_word=[]
     #For every unigram in the doc "i":
     for word in token_word:
     #For every word in the list, assign it's POS tag as a "a" for adj and lemmatize it as a adjective.    
        lemma=lemmatizer.lemmatize(word,"a")
     #For every word in the list, assign it's POS tag as a "v" for verb and lemmatize it as a verb.
        lemma=lemmatizer.lemmatize(lemma,"v")
     #For every word in the list, assign it's POS tag as a "n" for noun and lemmatize it as a noun.
        lemma=lemmatizer.lemmatize(lemma,"n")
        lemma_token_word.append(lemma)   
     #Remove stop words.
     meaningful_words = [w for w in lemma_token_word if not w in stops] 
     # Creat "false" N-grams from cleaned unigrams.
     #doc_ngrams=bigrams(meaningful_words)
     doc_ngrams=trigrams(meaningful_words)
     #Python's bi/trigram function creates a string of 2 or 3 words.
     #Next line of code puts those words together into one string.
     doc_ngrams=[' '.join(x) for x in doc_ngrams]
     #Append ngrams for each doc processed to the aggregated list of ngrams.
     all_ngrams.append(doc_ngrams)
     
#Create a dictionary from our ngram list.
dictionary = corpora.Dictionary(all_ngrams)
#Convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(ngram) for ngram in all_ngrams]
#Create an LDA model.
ldamodel = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=15, 
            id2word = dictionary, 
            passes=5, minimum_probability=0) 
#Print the top ngrams in each topic and their probabilities.            
print(ldamodel.print_topics(num_topics=15, num_words=10))

#Print topic-distrubtion for all docs or a range of docs.
#for i in range(len(content)):
for i in range(2):
    print(ldamodel[corpus[i]])
