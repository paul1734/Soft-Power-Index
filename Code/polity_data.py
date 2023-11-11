#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 15:00:40 2023

@author: -
"""

import pandas as pd 
import numpy as np
import os
import country_converter as coco

# set path
os.getcwd()
path = "/files/Polity"
os.chdir(path)

# load data
polity_orig = pd.read_excel('p5v2018.xls')
test = polity_orig[polity_orig['year'] >= 1990]
test = test[test['country'] == "USSR"]
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

# Clean Data for country names
# polity has 178 countries
polity_year95["country"].nunique()
polity_year95 = polity_year95.rename(columns={"country": "Nation", "year": "Year"})

# Drop countries with only little (less than 5 years)
polity_uniqueval = polity_year95['Nation'].value_counts()

"""
-> turn UAE into United Arab Emirates
-> turn Sudan-North into Sudan
- > turn Congo-Brazzaville into Congo Brazzaville
- > turn Cote D'Ivoire' into Ivory Coast
-> turn USSR into Russia; only two years affected (1990 - 1991);
encompasses majority of the population and the main part of the state system
"""
# Rename some nations with two separate names
polity_year95['Nation'] = polity_year95['Nation']\
    .replace({'UAE':'United Arab Emirates'})
polity_year95['Nation'] = polity_year95['Nation']\
    .replace({'Sudan-North':'Sudan'})
polity_year95['Nation'] = polity_year95['Nation']\
    .replace({'Congo-Brazzaville':'Congo Brazzaville'})
polity_year95['Nation'] = polity_year95['Nation']\
    .replace({'Myanmar (Burma)':'Myanmar'})
polity_year95['Nation'] = polity_year95['Nation']\
    .replace({'Congo Kinshasa':'DR Congo'})
polity_year95['Nation'] = polity_year95['Nation']\
     .replace({"Cote D'Ivoire":'Ivory Coast'})
polity_year95['Nation'] = polity_year95['Nation']\
     .replace({"USSR":'Russia'})
"""
-> Drop the following due to low representations and difficulty of 
 representing the changes of the Balkan countries

Nation | Number of appearances
South Sudan	8
Kosovo	11
Serbia	13
Montenegro	13
Timor-Leste	17

Serbia and Montenegro	4
Czechoslovakia	3
Yemen North	1
Yemen South	1
Germany West	1
Germany East	1

OTHER POSSIBILITY:
    Instead of dropping, use the data for the following two nations.
    So for Czechoslovakia, use the 3 years and add them to Czech Rep. and
    Slovakia. 
    However, time consuming. Will look into it in the future.
"""
dropped_countries = ["Serbia and Montenegro", "Yugoslavia",
"Czechoslovakia","Yemen North",
"Yemen South","Germany West","Germany East",
"South Sudan", "Kosovo","Serbia","Montenegro" , "Timor Leste"]

for name in dropped_countries:    
    polity_year95 = polity_year95.drop(polity_year95[polity_year95['Nation'] == name].index)

polity_year95["Nation"] = coco.convert(names=polity_year95["Nation"], to='name_short')
polity_uniqueval2 = polity_year95['Nation'].value_counts()
# print(polity_year95[polity_year95['Nation'] == "Cote D'Ivoire"])
# Save data as .csv
polity_year95.to_csv(path + "/polity95.csv", index=False) 
