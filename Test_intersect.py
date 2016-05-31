# -*- coding: utf-8 -*-
"""
Created on Wed May 18 20:13:15 2016

@author: Marcia
"""

pat_list = {'pat_num': '1234567', 'pat_num': '2345678'}
claim_list={'pat_num': '1234567', 'claim':'this is the claim', 'pat_num': '2345678','claim':'this is claim two', 'pat_num':'3456789','claim':'this is claim three'}

for key in pat_list:
    if key in claim_list:
        print ( claim_list)