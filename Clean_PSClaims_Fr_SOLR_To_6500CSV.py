#!/usr/bin/env python
# -- coding: utf-8 -- 

# This code takes the Walid claim csv file created from SOLR for a patent set,
#   takes only the first 6500 characters of the claim, 
#   and writes those lines back to a new cvs file.
# Input file (Walid's claim csv file) was one file that contained multiple rows,
#   where each row was one patent. So the input file contained the whole corpus.

import csv
import re
import sys
#Had to add this sys.maxsize statement because rows from SOLR are so long.
csv.field_size_limit(sys.maxsize)

#Opening the file I write to before getting in the "for" loop.
outfile = open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/PSClaimFiles/power_6500c_uspc_2013.csv', 'w')

#Debugging errors lead to need for "utf-8" and "ignore" in the open statement.
#The ignore due to some pats lacking a claim field, I think.
with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/PSClaimFiles/power_c_uspc_2013.csv', \
    encoding='utf-8', errors='ignore' ) as claimfile:
    claimlist = csv.reader(claimfile)
    #Skip the header row    
    next(claimlist)    
    for row in claimlist:
        #Used next line of code to only pull utility patents, but didn't seem to reduce filesize.
        #if str(row[0])[2:3] in '6789' and str(row[0])[9:10] == 'B':        
        #Shortened claim to 6500 chars which is approx 1000 words to make filezise more manageable.        
        #And SOLR data is riddled with \n line breaks between the quotes,  
        #   which open ok in EXCEL but lead to issues here, so I replaced \n with a blank.        
            claim_c= row[0][0:6500].replace('\n', ' ') 
        #Was getting an error about "ascii codec can't encode character" so kept only alpha's.
            claim_ao = re.sub("[^a-zA-Z]", " ", claim_c) 
        #Grabbed just patnumber from Walid ID num, deleting US and TypeCode.        
            #pat_num=str(row[0])[2:9] 
        #Put two strs into one list per row.        
            wlist=[claim_ao]
            #row_count = sum(1 for row in claimlist) 
            wr =  csv.writer(outfile, dialect='excel')
        #Write one row at a time to the open outfile.        
            wr.writerow(wlist) 
#Needed to close outfile officially as I didn't use "with open" to open it.   
outfile.close()   
#print(row_count)          