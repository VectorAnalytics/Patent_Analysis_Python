#!/usr/bin/env python
# -- coding: utf-8 -- 
import csv
from timeit import default_timer as timer

start = timer()

#Opening the file I write to before getting into the "for" loop.
outfile = open("/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/Claim_Files/claim_20_20000.csv", 'w')

#Debugging errors lead to need for "utf-8" and "ignore" in the open statement.
#The ignore due to some pats lacking a claim field, I think.

#Get list of patents that you want to find matching claims for.
#with open('/Users/mprice79/patonly_test_2015.csv', \
with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/Study_Abs_160513/pat_test_2015.csv', \
    encoding='utf-8', errors='ignore' ) as patfile:   
    patlist = csv.DictReader(patfile)
    for pat in patlist:           
#Get list of claims under study
        #with open('/Users/mprice79/claims_6500_200.csv', \
        with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/WalidFiles/claims_6500_20000.csv', \
            encoding='utf-8', errors='ignore' ) as claimfile:
                fieldnames = ['pat_num', 'claim']    
                claimlist = csv.DictReader(claimfile, fieldnames=fieldnames)
                for patc in claimlist:
                    if pat['pat_num'] == patc['pat_num']:
                        #print(patc['pat_num'], patc['claim'])
                        Claim=[patc['pat_num'], patc['claim'], pat['pat_set']]
                        #print(pat_list) 
                        wr =  csv.writer(outfile, lineterminator='\n', dialect='excel')
                        #Write one row at a time to the open outfile.        
                        wr.writerow(Claim) 
#Needed to close outfile officially as I didn't use "with open" to open it.
outfile.close()
end = timer()
print(end-start)   