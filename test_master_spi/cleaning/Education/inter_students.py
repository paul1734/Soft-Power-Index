#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 11:45:21 2023

@author: -
"""
import sys
sys.path.append('/files/test_master_spi')

import re
import requests
import pandas as pd
import country_converter as coco
from config import path_cleaning
# Specify the URL of the data you want to download
data = pd.read_csv(path_cleaning + "/Education/unesco_wto_short.csv")
df = data.copy()
# Define a function to extract country names using regular expressions
def extract_country_name(indicator):
    match = re.search(r'from (.+?),', indicator)
    if match:
        return match.group(1)
    else:
        return 'Unknown'

# Apply the function to create a new column 'Country'
df['Origin_Country'] = df['Indicator'].apply(extract_country_name)

# List of columns to drop, only interested in complete polity score
columns_to_drop = ['NATMON_IND', 'Indicator', 'LOCATION', 'TIME',
        'Flag Codes',]

# Drop the specified columns
df = df.drop(columns=columns_to_drop)
# rename Column
df = df.rename(columns={"Country": "Destination_Country", "Time": "Year"})
# If 	Flags: "Magnitude nil or negligible" insert 0 as value
df.loc[df['Flags'] == 'Magnitude nil or negligible', 'Value'] = 0

# Change position of columns for better readability
df = df[['Origin_Country', 'Destination_Country', 'Year', 'Value', 'Flags']]


# Count number of unique countries
unique = pd.DataFrame()
unique['Origin_Country'] = df['Origin_Country'].value_counts()
unique['Destination_Country'] = df['Destination_Country'].value_counts()

"""
How to read unique:
Origin_Country	Destination_Country
Angola	2201	10.0

# Origin_Country: There are 2201 origin countries Angolans could have studied.
# Destination_Country: There are only students from 10 countries which have 
# studied in Angola
    
	Origin_Country	Destination_Country
462302	Sudan	Andorra
9078	Angola	Angola
9079	Angola	Angola
9080	Angola	Angola
9081	Angola	Angola
9082	Angola	Angola
9083	Angola	Angola
9084	Angola	Angola
9085	Angola	Angola
9086	Angola	Angola
9087	Angola	Angola
1704	the Congo	Anguilla

ERROR: It is impossible that the origin country and the Destination Country
are the same. Need to drop all columns where Origin = Destination

"""
# Drop all columns where Origin = Destination
df = df[df['Origin_Country'] != df['Destination_Country']]
unique2 = pd.DataFrame()
unique2['Origin_Country'] = df['Origin_Country'].value_counts()
unique2['Destination_Country'] = df['Destination_Country'].value_counts()

# drop all rows where unknown countries are present in nation columns
df = df[(df['Origin_Country'] != 'unknown countries') & (df['Destination_Country'] != 'unknown countries')]

# Change Country names not readable by coco 
# Sudan (pre-secession) -> Sudan
df['Origin_Country'] = df['Origin_Country']\
    .replace({'Sudan (pre-secession)':'Sudan'})
df['Destination_Country'] = df['Destination_Country']\
    .replace({'Sudan (pre-secession)':'Sudan'})

# check for countries unreadable by coco using the unique2 index from 
# .unique()
coco_checkD = pd.DataFrame()
coco_checkD["Destination_Country"] = df['Destination_Country'].unique()
coco_checkD["Destination_Country"] = coco.convert(names=coco_checkD["Destination_Country"], to='name_short')

coco_checkO = pd.DataFrame()
coco_checkO["Origin_Country"] = df['Origin_Country'].unique()
coco_checkO["Origin_Country"] = coco.convert(names=coco_checkO["Origin_Country"], to='name_short')  
# Problem: the Netherlands Antilles not found in regex
# drop all rows where unknown (to coco) countries are present in nation columns
df = df[(df['Origin_Country'] != 'the Netherlands Antilles') & (df['Destination_Country'] != 'the Netherlands Antilles')]

# Convert country names / start with unique 
df["Origin_Country"] = coco.convert(names=df["Origin_Country"], to='name_short')
df["Destination_Country"] = coco.convert(names=df["Destination_Country"], to='name_short')

df.to_csv(path_cleaning + "/Education/clean_inter_students.csv")


"""
Clean Inter students more
"""

df = pd.read_csv(path_cleaning + "/Education/clean_inter_students.csv")
# Drop former index column
df = df.drop(['Unnamed: 0'], axis=1)


"""
It is bilateral data, it shows the destination and origin country of international 
exchange students.
There are some nan values in the column "Value".
I would like to fill them with the former value from the years before. 
If that doesn't work, take the value from the following year. 
"""
# Group the data by Nation and fill missing values within each group
df['Value'] = df.groupby(['Origin_Country', 'Destination_Country'])['Value'].apply(lambda x: x.ffill().bfill())
# Fill in 0 for the missing values
# assume the missing values are not recorded due to negligible sizes
df['Value'].fillna(0, inplace=True)

"""
Following that, I want to create the data for the years not recorded. As you can see in the xample below, there are some years missing for the Central African Republic. Fill those rows with the missing years. I want to interpolate them with the years using bfill or ffill if the first one doesn't work just like before.

	Origin_Country	Destination_Country	Year	Value
78	Ethiopia	Seychelles	2022	0.0
79	Central African Republic	Gibraltar	1999	
80	Central African Republic	Gibraltar	2000	
81	Central African Republic	Gibraltar	2001	
82	Central African Republic	Gibraltar	2002	
83	Central African Republic	Gibraltar	2003	
84	Central African Republic	Gibraltar	2005	
85	Central African Republic	Gibraltar	2008	
86	Central African Republic	Gibraltar	2016	
87	Central African Republic	Gibraltar	2020	
88	Ghana	Germany	2013	331.0
89	Ghana	Germany	2014	373.0

Ideally, I would get something like this for the full df: 

82	Central African Republic	Gibraltar	2002	
83	Central African Republic	Gibraltar	2003	
84	Central African Republic	Gibraltar	2004
85	Central African Republic	Gibraltar	2005
86	Central African Republic	Gibraltar	2006
87	Central African Republic	Gibraltar	2007	
88	Central African Republic	Gibraltar	2008	
"""
# Create a DataFrame with all possible combinations of 'Year', 'Origin_Country', and 'Destination_Country'
all_combinations = pd.DataFrame([(year, origin, dest) for year in df['Year'].unique()
                                 for origin in df['Origin_Country'].unique()
                                 for dest in df['Destination_Country'].unique()],
                                columns=['Year', 'Origin_Country', 'Destination_Country'])

# Merge the original DataFrame with the new DataFrame to fill in missing values
result_df = pd.merge(all_combinations, df, on=['Year', 'Origin_Country', 'Destination_Country'], how='left')

# Interpolate missing values with former values as an estimate
result_df['Value'] = result_df.groupby(['Origin_Country', 'Destination_Country'])['Value'].apply(lambda x: x.ffill().bfill())
result_df['Value'].fillna(0, inplace=True)

result_df = result_df.drop(['Flags'], axis=1)
result_df.to_csv(path_cleaning + "/Education/interpolated_inter_students.csv")
