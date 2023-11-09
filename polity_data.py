#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:00:40 2023

@author: -
"""

import pandas as pd 
import numpy as np
import os

# set path
os.getcwd()
path = "/files/"
os.chdir(path)

# load data
polity_orig = pd.read_excel('p5v2018.xls')

#only use data from 1990 onwards
polity_year95 = polity_orig[polity_orig['year'] >= 1990]
# List of columns to drop, only interested in complete polity score
columns_to_drop = ['p5', 'cyear', 'ccode', 'scode', 'flag', 'fragment',
    'durable', 'xrreg', 'xrcomp', 'polity2', 'democ', 'autoc',
       'xropen', 'xconst', 'parreg', 'parcomp', 'exrec', 'exconst', 'polcomp',
       'prior', 'emonth', 'eday', 'eyear', 'eprec', 'interim', 'bmonth',
       'bday', 'byear', 'bprec', 'post', 'change', 'd5', 'sf', 'regtrans']

# Drop the specified columns
polity_year95 = polity_year95.drop(columns=columns_to_drop)

columns_to_replace = ['polity']
"""
# replace special number -77 with 0
# -77 is equal to anarchy/neutral and converted to 0 as stated by codebook
# Source: https://www.systemicpeace.org/inscr/p5manualv2018.pdf
"""
polity_year95[columns_to_replace] = polity_year95[columns_to_replace].replace(-77, 0)
"""
# " -66: Cases of foreign 'interruption' are treated as system missing."
# -77 is a case of transition and should be interpolated acc to codebook 
# (See source)
"""
# turn -66 and -88 into nan
polity_year95['polity'] = polity_year95['polity'].replace([-66, -88], np.nan)
# linear interpolation of nan values
polity_year95['polity'] = polity_year95['polity'].interpolate(method='linear')
# convert to int value
polity_year95['polity'] = polity_year95['polity'].round().astype(int)
print(polity_year95)

# CHeck for nan values in polity score, none found
polity_year95['polity'].isna().sum()

# function to classify state type acc. to Polity 5
def classify_regime(value):
    if value >= 6 and value <= 10:
        return "Democracy"
    elif value >= -5 and value <= 5:
        return "Anocracy"
    elif value >= -10 and value <= -6:
        return "Autocracy"
    else:
        return "Invalid value"
    
# create new column for state type
polity_year95['state_type'] = polity_year95['polity'].apply(classify_regime)

polity_year95.to_csv(path + "polity95.csv", index=False) 










