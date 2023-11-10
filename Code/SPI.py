#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 15:50:27 2023

@author: -
"""
import pandas as pd 
import numpy as np
import os
import country_converter as coco

# set path
os.getcwd()
path = "/files/"
os.chdir(path)

"""
The following code will create the Soft Power Index in a single dataframe
 It will combine several cleaned data sources such as the
 Polity 5 or CPI dataset.
"""
# Create Soft Power Index

# Start with combining Polity and CPI data
polity_data = pd.read_csv('polity95.csv')
# convert cpi to long format
cpi = pd.read_csv("CPI/CPI_Index.csv")
cpi = cpi.drop(['Unnamed: 0'], axis=1)
cpi_long = pd.melt(cpi, id_vars=['Nation'], var_name='Year', value_name='Value')

# cpi has 198 countries (see cpi data), polity has 178
polity_data["country"].nunique()
polity_data = polity_data.rename(columns={"country": "Nation", "year": "Year"})

# CPI has complete data for all 28 years
cpi_long_uniqueval = cpi_long['Nation'].value_counts()
# Drop countries with only little (less than 5 years)
polity_uniqueval = polity_data['Nation'].value_counts()

# Rename some nations with two separate names
polity_data['Nation'] = polity_data['Nation']\
    .replace({'UAE':'United Arab Emirates'})
polity_data['Nation'] = polity_data['Nation']\
    .replace({'Sudan-North':'Sudan'})
polity_data['Nation'] = polity_data['Nation']\
    .replace({'Congo-Brazzaville':'Congo Brazzaville'})
polity_data['Nation'] = polity_data['Nation']\
    .replace({'Myanmar (Burma)':'Myanmar'})
polity_data['Nation'] = polity_data['Nation']\
    .replace({'Congo Kinshasa':'DR Congo'})
polity_data['Nation'] = polity_data['Nation']\
     .replace({"Cote d'Ivoire":'Ivory Coast'})
     

"""
Problems for polity coco:
Germany West not found in regex
Serbia and Montenegro not found in regex
Yugoslavia not found in regex
USSR not found in regex
UAE not found in ISO3
Germany East not found in regex

Problems for cpi coco:
Serbia and Montenegro not found in regex
Yugoslavia not found in regex

-> turn UAE into United Arab Emirates
-> turn SUdan-North into Sudan
- > turn Congo-Brazzaville into Congo Brazzaville

-> Drop the following due to low representations:
Serbia and Montenegro	4
Czechoslovakia	3
USSR	2
Ivory Coast	2
Yemen North	1
Yemen South	1
Germany West	1
Germany East	1
"""
     
uncommon_countries = ["Serbia and Montenegro", "Yugoslavia",
"Czechoslovakia", "USSR", "Ivory Coast","Yemen North",
"Yemen South","Germany West","Germany East"]
for name in uncommon_countries:    
    polity_data = polity_data.drop(polity_data[polity_data['Nation'] == name].index)
    cpi_long = cpi_long.drop(cpi_long[cpi_long['Nation'] == name].index)

double_names = ["Czechia"]
polity_data["Nation"] = coco.convert(names=polity_data["Nation"], to='name_short')
cpi_long["Nation"] = coco.convert(names=cpi_long["Nation"], to='name_short')

test_df = pd.DataFrame()
test_df['cpi'] = cpi_long_uniqueval
test_df['polity'] = polity_uniqueval
# Find mismatched country names
polity_countries = set(polity_data["Nation"].unique())
cpi_countries = set(cpi_long["Nation"].unique())

mismatched_countries = polity_countries.symmetric_difference(cpi_countries)
print(mismatched_countries)

# The following countries are not present in Polity 5
# 

# countries not available in Polity5 will be dropped
# Thankfully mostly small island nations or nations with 
# geopolitically unresolved disputes, i.e. difficulty of finding 
# further data
unmatched_countries = ['Hong Kong', 'Tonga', 'Maldives', 'Malta', 
 'Sao Tome and Principe', 'Kiribati', 'Grenada', 'Barbados', 
 'Bahamas', 'Samoa', 'Palestine', 'Belize', 'Vanuatu', 'Macau', 
 'St. Vincent and the Grenadines', 'Brunei Darussalam', 'Iceland', 
 'Seychelles', 'Puerto Rico', 'St. Lucia', 'Dominica']

lack_polity_countries = ['Congo Republic','Czech Republic', 'Eswatini',
       'Ethiopia', 'Kosovo', 'Kyrgyz Republic', 'Montenegro',
       'North Macedonia', 'Serbia', 'Slovakia', 'South Sudan', 'Timor-Leste']

for name in unmatched_countries:    
    polity_data = polity_data.drop(polity_data[polity_data['Nation'] == name].index)
    cpi_long = cpi_long.drop(cpi_long[cpi_long['Nation'] == name].index)
#Use country converter to change both cpi and polity country names
# to standardized names -> Iso 



# Search matching countries between polity and cpi
#countries = pd.DataFrame()
#countries["polity_c"] = polity_data["Nation"].unique()
#countries["cpi_c"] = cpi_long["Nation"].unique()

# Convert 'Year' to the same data type in both DataFrames
polity_data['Year'] = polity_data['Year'].astype(int)
cpi_long['Year'] = cpi_long['Year'].astype(int)

# inner starts at 1995 but polity alredy starts at 1990
spi_inner = pd.merge(polity_data, cpi_long, left_on=['Nation', 'Year'], \
            right_on=['Nation','Year'], how='inner')
spi_inner = spi_inner.rename(columns={"Value": "cpi"})
# create outer, maybe interpolation for cpi is possible

"""
SOME NAMES, E.G. SLOVAKIA ARE counted twice in cpi_long!!!
"""
spi_outer = pd.merge(polity_data, cpi_long, left_on=['Nation', 'Year'], \
            right_on=['Nation','Year'], how='outer')
spi_outer = spi_outer.rename(columns={"Value": "cpi"})

spi_outer = spi_outer.sort_values(by=['Nation','Year'])

# CPI has complete data for all 28 years
spi_uniqueval = spi_outer['Nation'].value_counts()
# Count NaN values in 'polity' and 'cpi' columns grouped by 'Nation'
nan_counts = spi_outer.groupby('Nation')[['polity', 'cpi']].apply(lambda x: x.isna().sum())
# Filter out rows where either 'polity' or 'cpi' is above 5
test_nan = nan_counts[(nan_counts['polity'] >= 6) | (nan_counts['cpi'] >= 6)]
# Interpolate the data for cpi before 1995
# Interpolate data for polity after 2018
