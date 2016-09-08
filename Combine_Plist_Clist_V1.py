#!/usr/bin/env python
# -- coding: utf-8 -- 
import csv

#This program match merges a list of patents under study (from a particular year)
#    with a year's worth of cleaned claim data from Walid's SOLR server.

#Was using timer to understand processing time for various filesizes.
#from timeit import default_timer as timer

#start = timer()

#I have various "outfile" and "with open" statements, based on if running on MAC or at WW432 and if test or real file.

#Name and open the file I want to saved my matched merge results to.
#outfile = open("/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/Claim_Files/claim_20_200.csv", 'w')
outfile = open("/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/Claim_Files/pat_list_2013_match_to_claims.csv", 'w')
#outfile = open("/Users/mprice79/claim_21_200.csv", 'w')

#Get list of patents that I want to find matching claims for.
#Debugging errors lead to need for "utf-8" and "ignore" in the open statement.
#The ignore due to some pats lacking a claim field, I think.

#with open('/Users/mprice79/patonly_test_2015.csv', \
#with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/Study_Abs_160513/pat_test_2015.csv', \
with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/Study_Abs_160513/pat_list_2013.csv', \
    encoding='utf-8', errors='ignore' ) as patfile:   
    patlist = csv.DictReader(patfile)
    for pat in patlist:           
#Get list of claims under study, this is Walid data after reformatting pat number
#   and grabbing only first 6500 alpha chars of claim.
        #with open('/Users/mprice79/claims_6500_200.csv', \
        with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/WalidFiles/claims_6500_2013_ut.csv', \
            encoding='utf-8', errors='ignore' ) as claimfile:
                fieldnames = ['pat_num', 'claim']    
                claimlist = csv.DictReader(claimfile, fieldnames=fieldnames)
                for patc in claimlist:
                    if pat['pat_num'] == patc['pat_num']:
                        Claim=[patc['pat_num'], patc['claim'], pat['pat_set']]
                        wr =  csv.writer(outfile, lineterminator='\n', dialect='excel')
                        #Write one row at a time to the open outfile.        
                        wr.writerow(Claim) 
#Needed to close outfile officially as I didn't use "with open" to open it.
outfile.close()
#end = timer()
#print(end-start)   