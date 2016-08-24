# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 09:57:18 2016

@author: Marcia
"""
# This script dedupes the claim files for any duplicates, just in case. 
#  One problem in this code would be if the "lines" were not exactly the same,
#    i.e. if the same pat_num had two different claim texts. 

with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/WalidFiles/claims_6500_200.csv', 'r') as in_file, \
open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/WalidFiles/claims_6500_200_dd.csv', 'w') as out_file:
    seen = set()
    for line in in_file:
        if line in seen: continue #if already encountered then skip
            
        seen.add(line) #if not already encountered add it to seen and write it to outfile
        out_file.write(line)



