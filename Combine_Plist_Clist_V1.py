#!/usr/bin/env python
# -- coding: utf-8 -- 
import csv

#Opening the file I write to before getting in the "for" loop.
outfile = open("/Users/mprice79/claim_set_test.csv", 'w')

#Debugging errors lead to need for "utf-8" and "ignore" in the open statement.
#The ignore due to some pats lacking a claim field, I think.
with open('/Users/mprice79/patonly_test_2015.csv', \
    encoding='utf-8', errors='ignore' ) as patfile:
    patlist = csv.DictReader(patfile)
    #Skip the header row    
    next(patlist)    
    #set_claims=[]
    for pat in patlist:           
#Get list of claims under study
        with open('/Users/mprice79/claims_6500_200.csv', \
            encoding='utf-8', errors='ignore' ) as claimfile:
                fieldnames = ['pat_num', 'claim']    
                claimlist = csv.DictReader(claimfile, fieldnames=fieldnames)
                for patc in claimlist:
                    if pat['pat_num'] == patc['pat_num']:
                        #print(patc['pat_num'], patc['claim'])
                        Claim=[patc['pat_num'], patc['claim']]
                        #print(pat_list)           
                        wr =  csv.writer(outfile, lineterminator='\n', dialect='excel')
                        #Write one row at a time to the open outfile.        
                        wr.writerow(Claim) 
#Needed to close outfile officially as I didn't use "with open" to open it.
outfile.close()   