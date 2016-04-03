# -*- coding: utf-8 -*-
"""
Updated on Sunday April 3 2016
@author: Marcia Price
In Python 2.7 Version

The print lines that are commented out were used for testing and 
comprehension, ie to understand how the functions worked.
"""

import math
from collections import Counter
from nltk import cluster

#Bring in sentences as corpora and tokenize into words using split function
sentence1 = "it is a dog day afternoon"
words1=sentence1.split()
sentence2='it is a happy afternoon for cats'
words2=sentence2.split()
sentence3='it is a happy afternoon for cats'
words3=sentence3.split()
sentence4='it is a happy afternoon for a horse'
words4=sentence4.split()

#Counter function creates a TDM for each corpora
counter1=Counter(words1)
counter2=Counter(words2)
counter3=Counter(words3)
counter4=Counter(words4)
#print counter4

#Union of the counter.keys creates an unique set of all words used across all corpora
all_items=set()
#print all_items
all_items=set(counter1.keys()).union( set(counter2.keys()) )
#print all_items
all_items=(all_items).union( set(counter3.keys()) )
#print all_items
all_items=(all_items).union( set(counter4.keys()) )
#print all_items

#Create a vector of the counts of all words for each corpora
vector1=[counter1[k] for k in all_items]
vector2=[counter2[k] for k in all_items]
vector3=[counter3[k] for k in all_items]
vector4=[counter4[k] for k in all_items]
#print vector1
#print vector2
#print vector3
#print vector4

#Calc cosine similarity between corpora but remember it equals 1-cosine distance
cos_sim31 = 1-(cluster.util.cosine_distance(vector3,vector1))
cos_sim32 = 1-(cluster.util.cosine_distance(vector3,vector2))
cos_sim34 = 1-(cluster.util.cosine_distance(vector3,vector4))

#Print results to screen
print
print "Sentence 1 says: ",sentence1
print "Sentence 2 says: ",sentence2
print "Sentence 3 says: ",sentence3
print "Sentence 4 says: ",sentence4

print('\nCosine Simularity of Sentence 1 and 3 = %4.2f'% cos_sim31)
angle_in_radians=math.acos(cos_sim31)
print('Cosine Simularity in Radians of Sentence 1 and 3 = %4.2f'% angle_in_radians)
angle_in_degrees=math.degrees(angle_in_radians)
print('Cosine Simularity in Degrees of Sentence 1 and 3 = %4.0f'% angle_in_degrees)


print('\nCosine Simularity of Sentence 2 and 3 = %4.2f'% cos_sim32)
angle_in_radians=math.acos(cos_sim32)
print('Cosine Simularity in Radians of Sentence 2 and 3 = %4.2f'% angle_in_radians)
angle_in_degrees=math.degrees(angle_in_radians)
print('Cosine Simularity in Degrees of Sentence 2 and 3 = %4.0f'% angle_in_degrees)

print('\nCosine Simularity of Sentence 4 and 3 = %4.2f'% cos_sim34)
angle_in_radians=math.acos(cos_sim34)
print('Cosine Simularity in Radians of Sentence 4 and 3 = %4.2f'% angle_in_radians)
angle_in_degrees=math.degrees(angle_in_radians)
print('Cosine Simularity in Degrees of Sentence 4 and 3 = %4.0f'% angle_in_degrees)