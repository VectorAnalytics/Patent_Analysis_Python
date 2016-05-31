#!/usr/bin/env python
# -- coding: utf-8 -- 
import csv
import re
import sys

csv.field_size_limit(sys.maxsize)   
#Get list of claims under study
with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/WalidFiles/claims_test_20000.csv', \
    encoding='utf-8' ) as infile, open("pat_test_20000.csv", 'w') as outfile:
    header = next(infile)
    outfile.write(header)
    next(infile)
    for row in infile:
        pat_num = str(row[0])[2:9]
        claim_c= str(row[1][0:5000].replace('\n', ' ')) 
            #claim_c=[re.sub(r'[^\w\s]','', claim_c)]
        row=(pat_num + ', ' + claim_c)
        outfile.write(row)
      
        