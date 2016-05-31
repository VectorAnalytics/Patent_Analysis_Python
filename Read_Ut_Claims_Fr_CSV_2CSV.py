#!/usr/bin/env python
# -- coding: utf-8 -- 
import csv
import re
import sys

csv.field_size_limit(sys.maxsize)
all_pat_num=[]
all_m_claims=[]    
#Get list of claims under study
with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/WalidFiles/claims_test_20000.csv', \
    encoding='utf-8' ) as claimfile:
    for row in csv.reader(claimfile):
        #next(row)
        if str(row[0])[2:3] in '6789':
            #pat_num = str(row[0])[2:9]
            row[0] = str(row[0])[2:9]
            claim_c= str(row[1][0:5000].replace('\n', ' ')) 
            #claim_c_ca=[re.sub(r'[^\w\s]','', claim_c)]
            row[1]=[re.sub(r'[^\w\s]','', claim_c)]
            #next(claimlist)
            #for claim in claimlist:
             #   pat_num_c=str(claim[0])[2:9]
                #claim_c=str(claim[1][0:7500].replace('\n', ' '))        
            all.append(row[0],row[1])            
            #all_pat_num.append(pat_num)    
            #all_m_claims.append(claim_c_ca)
        else:
                next(row)           
#print(all_m_claims)           
with open("pat_test_20000.csv", 'w') as outfile:
        wr =  csv.writer(outfile, dialect='excel')
        wr.writerows(all)        
   
        