# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 09:57:18 2016

@author: Marcia
"""

with open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/Study_Abs_160513/pat_list_cpc_2011.csv', 'r') as in_file, \
open('/Users/Marcia/OneDrive/DSBA_6880/Parsed_Patent_Files/Study_Abs_160513/pat_list_cpc_2011_dd.csv', 'w') as out_file:
    seen = set()
    for line in in_file:
        if line in seen: continue #if already encountered then skip
            
        seen.add(line) #if not already encountered add it to seen and write it to outfile
        out_file.write(line)
    