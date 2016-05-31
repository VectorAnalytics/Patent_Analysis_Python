#!/usr/bin/env python
# -- coding: utf-8 -- 
import csv
import re
import sys

csv.field_size_limit(sys.maxsize)
#this code words for Claims_text_200, but not claims_test_20000 (it runs but is empty)
#Get list of patents under study
with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/Study_Abs_160513/pat_test_2015.csv', "r" ) \
    as patfile:
    patlist = csv.reader(patfile)
    next(patlist)
    all_m_claims=[]
    for pat in patlist:      
#Get list of claims under study
        with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/WalidFiles/claims_test_200.csv', \
            encoding='utf-8', errors='ignore' ) as claimfile:
            #claim_c= [row[1][0:6500].replace('\n', ' ') for row in csv.reader(claimfile) if str(row[0])[2:9] == pat[2]]
            claim_c= [row[1][0:6500] for row in csv.reader(claimfile) if str(row[0])[2:9] == pat[2]]
            #claim_c_ca=[re.sub(r'[^\w\s]','', str(claim_c[0]))]            
            all_m_claims.append(claim_c)           
    print(all_m_claims)           
    with open("test_claims_200.csv", 'w') as outfile:
        wr =  csv.writer(outfile, dialect='excel')
        wr.writerows(all_m_claims)        
   
        