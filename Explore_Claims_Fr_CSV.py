#!/usr/bin/env python
# -- coding: utf-8 -- 
import csv
import re
import sys
#Had to add this sys.maxsize statement because rows from Walid are so long
csv.field_size_limit(sys.maxsize)

#Opening the file I write to before getting in the "for" loop.

outfile = open("claims_6500_20155.csv", 'w')

#Debugging errors lead to need for "utf-8" and "ignore" in the open statement.
#The ignore due to some pats lacking a claim field, I think.
with open('/Users/mprice79/claims_2015.csv', \
    encoding='utf-8', errors='ignore' ) as claimfile:
    claimlist = csv.reader(claimfile)
    #Skip the header row    
    next(claimlist)    
    for row in claimlist:
        #Shortened claim to 6500 chars which is approx 1000 words to make filezise more manageable.        
        #And Walid data is riddled with \n line breaks between the quotes,  
        #which open ok in EXCEL but lead to issues here.        
        claim_c= row[1][0:6500].replace('\n', ' ') 
        #Was getting an error about "ascii codec can't encode character" so kept only alpha's
        claim_ao = re.sub("[^a-zA-Z]", " ", claim_c) 
        #Grabbed just patnumber from Walid ID num, deleting US and TypeCode.        
        pat_num=str(row[0])[2:9] 
        #Put two strs into one list per row.        
        pat_list=[pat_num, claim_ao]
        #print(pat_list)           
        wr =  csv.writer(outfile, dialect='excel')
        #Write one row at a time to the open outfile.        
        wr.writerow(pat_list) 
#Needed to close outfile officially as I didn't use "with open" to open it.
outfile.close()   
        