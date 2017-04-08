#!/usr/bin/env python
# Code To Perform Topic Modelling With Gensim LDA Model And Visuals
# Marcia Price, March 10, 2017
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
from gensim import corpora
#from gensim.corpora import Dictionary

lemmatizer=WordNetLemmatizer()
#Note: need to download nltk.data before using nltk.corpus and stopwords the first time!

#Prepare set of stopwords that includes "English" and special stopwords.
# This list of special stopwords include the last 16 I added that made 
#   significant improvement in using cosine to discriminate between patent sets.
ps = open('/Users/Marcia/OneDrive/UNCC General/DSBA_6880/Patent_Parsing/Patent_Analysis_Python/PatentStopwordsIII.csv')
csv_ps=csv.reader(ps)
patent_stopwords=[]
for row in csv_ps:
    patent_stopwords.append(row[0])
xx = stopwords.words("english") 
xx.extend(patent_stopwords)
stops = set(xx) 

#Read in the list of docs you want to perform topic modeling on.
#Input file is a csv with first row of headers: doc_set, doc_id, doc_content.
#I had trouble encoding with "uxxxxx" so switched to "ISO-8859-1".
doclist_df = pd.read_csv('/Users/Marcia/OneDrive/UNCC General/DSBA_6880/Patent_Parsing/Patent_Analysis_Python/power_claims_all_wid.csv',
                      encoding="ISO-8859-1", keep_default_na=False, na_values=[""])
#Look at first five docs in df to see cols names and make sure the read it working.
print(doclist_df.head())

#Put just the content in a df, where "content" is the text you want to use for topic modeling.
content=doclist_df.doc_content
all_ngrams=[]
#Loop through the doc list doc by doc.
for i in content:
    #Put all characters into lowercase.
     lower=i.lower()
     #Only keep alpha (delete punc and numbers).
     alpha_only = re.sub("[^a-zA-Z]", " ", lower)
     #Replace extra white space and tabs and linefeeds.
     alpha_only = (" ".join(alpha_only.split()))
     #Grab the first n number of characters in the content string to use for topic modeling.
     alpha_only = alpha_only[:8000]
     #Split string into tokens of single unigram words.
     token_word=word_tokenize(alpha_only)
 #Setup variables and conduct lemmatization. 
     #I lemmatize as an adjective, noun, and verb sequentially, so all unigrams
     # are reduced as much as possible. Lemmatizing to an adverb I can't get to work. 
#With other corpora, it might be interesting to delete verbs.     
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
     # Create "false" ngrams from cleaned unigrams.
     #doc_ngrams=bigrams(meaningful_words)
     doc_ngrams=trigrams(meaningful_words)
     #Python's bi/trigram function creates a list of 2 or 3 words, 
     #  ie strings of words separated with commas.
     #  Next line of code puts those words together into one string, 
     #  so our ngram acts like a single term.
     doc_ngrams=[' '.join(x) for x in doc_ngrams]
     #Append ngrams for each doc processed to the aggregated list of ngrams.
     all_ngrams.append(doc_ngrams)
     
#Create a dictionary from our ngram list.
dictionary = corpora.Dictionary(all_ngrams)
#Print the number of unique ngrams in the dictionary.
print(dictionary)
#Get rid of ngrams that are too rare or too common.
#    Ignore ngrams that appear in less than no_below documents 
#    or more than no_above percent of documents.
#dictionary.filter_extremes(no_below=5, no_above=0.95, keep_n=None)
dictionary.filter_extremes(no_below=2, no_above=0.95)
#Print the number of unique ngrams again, to see what filter did.
print(dictionary)
#Can't figure out exactly what compactify does; one example used it; another didn't.
dictionary.compactify()
print(dictionary)
#Convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(ngram) for ngram in all_ngrams]
#Tring to logging to work, to see convergence, but so far unable to.
import logging
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
hdlr=logging.FileHandler('/Users/Marcia/OneDrive/UNCC General/DSBA_6880/Misc_Analysis_Files/lda_model_log.txt')
logger.addHandler(hdlr)
#Create an LDA model.
#Input number of topics to num_top variable, just also choose correct "t" lower in code.
num_top=15
num='Testv2_15'
#LdaModel options: passes=complete passes through the corpus
#                  chucksize=number of docs to include in one update/iteration of the lda model
#                  update_every=1 means updating once every chunk =0 means batch usage of LDA
#                  minimum_probability=controls filtering the topics returned for a document
#                  eval_every=none means no log perplexity estimate is logged; otherwise set to a number of iters
lda = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=num_top, 
            id2word = dictionary,
            passes=10, minimum_probability=0) 
hdlr.close()
logger.removeHandler(hdlr)
#Print the top ngrams in each topic and their probabilities.            
#print(lda.print_topics(num_topics=num_top, num_words=10))

#Print topic-distribution for all docs or a range of docs.
#for i in range(len(content)):
#for i in range(1):
#    print(lda[corpus[i]])

#Print topic-distribution for all docs with the doc_set to a csv file.
#First, create a list of lists (a list of topic dists for a list of docs)
topic_prob = [dict(lda[x]) for x in corpus]
#Convert list of list to a dataframe.
topic_prob_df = pd.DataFrame(topic_prob)
#Get the doc_set for each doc from the original dataframe.
doc_set_df = doclist_df.doc_set
#Merge the topic dists with the doc_set by index.
merged_df = pd.concat([doc_set_df, topic_prob_df], axis=1, join_axes=[doc_set_df.index])
#Finally, write merged df to a csv.
merged_df.to_csv('/Users/Marcia/OneDrive/UNCC General/DSBA_6880/Misc_Analysis_Files/TopicDistClaims'+num+'.csv')


    
#View the network of topics and terms/ngrams.
import networkx as nx
import matplotlib.pyplot as plt

def graph_terms_to_topics(lda, num_terms=num_top):
    #topic names: select appropriate "t" based on number of topics
    #Use line below for num_top = 15.
    t = ['0','1', '2','3','4','5','6','7','8','9','10','11','12','13','14']
    #Use line below for num_top = 25.
    #t = ['0','1', '2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
    #Use line below for num_top = 35.
    #t = ['0','1', '2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34']       
    #Use line below for num_top = 45.
    #t = ['0','1', '2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44']       
    
#Create a network graph and size it.
    G = nx.Graph()
    plt.figure(figsize=(16,16))
    # generate the edges
    for i in range(0, lda.num_topics):
        topicLabel = t[i]
        terms = [term for term, val in lda.show_topic(i, num_terms+1)]
        for term in terms:
            G.add_edge(topicLabel, term, edge_color='red')
    
    pos = nx.spring_layout(G) # positions for all nodes
    
    #Plot topic labels and terms labels separately to have different colours
    g = G.subgraph([topic for topic, _ in pos.items() if topic in t])
    nx.draw_networkx_labels(g, pos, font_size=20, font_color='r')
    #If network graph is difficult to read, don't plot ngrams titles.
    #g = G.subgraph([term for term, _ in pos.items() if str(term) not in t])
    #nx.draw_networkx_labels(g, pos, font_size=12, font_color='orange')
    #Plot edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), alpha=0.3)
    #Having trouble saving graph to file automatically; below code not working. Must manually save.
    plt.axis('off')
    plt.show(block=False)
    plt.savefig('/Users/Marcia/OneDrive/UNCC General/DSBA_6880/Misc_Analysis_Files/TopicNetwork'+num+'.png', bbox_inches='tight')

graph_terms_to_topics(lda, num_terms=num_top) 


#Create interactive graph to examine top 30 ngrams in each topic.
#Use pyLDAvis to visualize the topics in a network using 
#   Jensen-Shannon divergence as metric of distance between the topics.
import pyLDAvis.gensim as gensimvis
import pyLDAvis
#Create data to visualize.
vis_data = gensimvis.prepare(lda, corpus, dictionary)
#pyLDAvis.display(vis_data)
#Use vis_data "prepared" in earlier step.
#Now display the visualization in a local server page. 
#pyLDAvis.show(vis_data) 
#Save the visualization to an html file.
pyLDAvis.save_html(vis_data, '/Users/Marcia/OneDrive/UNCC General/DSBA_6880/Misc_Analysis_Files/ClaimsInteractVis'+num+'.html')
