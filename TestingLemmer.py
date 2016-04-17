# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

#Even though I imported pos_tag, I get an error when i invoke it, in Ryan Wesslen's code and in a sample example.
#If you don't use some sort of pos_tag, the lemmatizer does nothing. 
#from nltk import pos_tag

from nltk.tokenize import word_tokenize

lemmatizer=WordNetLemmatizer() 

#This is Ryan's code from last semester DSBA 6100. The pos_tag throws an error.

#wordnet_tag ={'NN':'n','JJ':'a','VB':'v','RB':'r','VBN':'v','VBD':'v', 
#    'VBG':'v','VBZ':'v','NNS':'n','VBP':'v','CD':'n','IN':'n','MD':'n', 
#    'JJR':'a','JJS':'a','DT':'n','RBR':'r','PRP':'n','CC':'n','WRB':'n', 
#    'PRP$':'n','RP':'r','WP$':'n','PDT':'n','WDT':'n','WP':'n','LS':'n' 
#} 

#def lemmatize_words_array(words_array): 
#    lemmatizer = WordNetLemmatizer() 
#    tagged = pos_tag(words_array) 
#    lemmatized_words_array = []; 
#    for word in tagged: 
#        lemma = lemmatizer.lemmatize(word[0],wordnet_tag[word[1]]) 
#        lemmatized_words_array.append(lemma) 
#    return lemmatized_words_array 

#Prepare set of stopwords that includes "English" and Patent Stopwords
ps = open('PatentStopwordsIII.csv')
csv_ps=csv.reader(ps)
patent_stopwords=[]
for row in csv_ps:
    patent_stopwords.append(row[0])
xx = stopwords.words("english") 
xx.extend(patent_stopwords)
stops = set(xx) 

#Input string called "Abstract" to test lemmatization.

Abstract='Tests methods method organ organize organizing testing of the blue mast by the Blues master'    

#Keep only alpha's in the string.         
alpha_only = re.sub("[^a-zA-Z]", " ", Abstract) 
print(Abstract) 
#Convert all characters to lowercase
lower = alpha_only.lower()
print(lower)
#Split string into tokens of words
token_verb=word_tokenize(lower)
#Create an empty list
token_array_verb=[]
#For every word in the list, assign it's POS tag as a "v" for verb and lemmatize it as a verb.
for word in token_verb:
        lemma=lemmatizer.lemmatize(word,"v")
        token_array_verb.append(lemma)
print(token_array_verb)
#For every word in the list, assign it's POS tag as a "n" for noun and lemmatize it as a noun.
token_array_noun=[]
for word in token_array_verb:
        lemma=lemmatizer.lemmatize(word,"n")
        token_array_noun.append(lemma)
print(token_array_noun)  

#Here I was trying to use NLTK's built in function to generate POS tags, but got same error as when using Ryan's code.      
#tokens_pos=pos_tag(tokens)
#print(tokens_pos)
#lemmered=lemmatizer.lemmatize(tokens_pos)
#print(lemmered)
#words = alpha_only.lower().split()
#print(words)

#Remove stopwords from lemmatized list (both English and special stopwords)
meaningful_words = [w for w in token_array_noun if not w in stops] 
#print(meaningful_words)
print(meaningful_words)
#lemmatization = lemmatize_words_array(meaningful_words)
