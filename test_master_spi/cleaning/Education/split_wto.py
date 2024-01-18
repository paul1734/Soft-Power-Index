#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 11:40:53 2024

@author: -
"""

import re
import requests
import pandas as pd
import country_converter as coco
# from config import path_cleaning
# Specify the URL of the data you want to download
data = pd.read_csv("/files/test_master_spi/cleaning/Education/unesco_wto.csv")

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

# List of columns to drop, only interested in complete students
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