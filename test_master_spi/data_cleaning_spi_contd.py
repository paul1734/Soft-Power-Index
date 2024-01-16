#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 16:52:18 2023

@author: -
"""
import sys
sys.path.append('/files/test_master_spi')

import pandas as pd 
import numpy as np
import os
import country_converter as coco
from itertools import combinations
from config import path_cleaning


########################################
# 6. Combine Refugee data
########################################
spi = pd.read_csv(path_cleaning + "spi_clean1.csv")
spi = spi.drop(['Unnamed: 0'], axis=1)
ref = pd.read_csv(path_cleaning + "/Migration/refugees_unhcr_1990_2023.csv", header=13)

# Drop IDP (Internally displaced persons) as they don't relate to other nations
cols_of_interest = ['Year', 'Country of origin', 'Country of asylum',
                    'Refugees under UNHCR\'s mandate', 'Asylum-seekers',
                    'Other people in need of international protection', 
                    'Stateless persons',
                    'Host Community', 'Others of concern']
ref = ref[cols_of_interest]

df = ref.copy()
# drop rows where Unknown == Unknown in both "Country of origin" and	"Country of asylum" at the same time
#df_filtered = df.query('`Country of origin` != "Unknown" and `Country of asylum` != "Unknown"')
# Sum up the specified columns into a new column "total_refugees"
df['total_refugees'] = df.iloc[:, 3:].sum(axis=1)
# Drop useless columns
df = df.drop(['Refugees under UNHCR\'s mandate', 'Asylum-seekers',
'Other people in need of international protection', 'Stateless persons',
'Host Community', 'Others of concern'], axis=1)

# Rename countries to harmonized names
#df["Country of origin"] = coco.convert(names=df["Country of origin"], to='name_short')
#df["Country of asylum"] = coco.convert(names=df["Country of asylum"], to='name_short')


# Merge the two DataFrames based on "Year" and "Nation_Destination"
#merged_df = pd.merge(spi, df, left_on=['Year', 'Nation_Destination'], right_on=['Year', 'Country of asylum'], how='left')
# Fill NaN values in the new column with 0
#merged_df['total_refugees_dest'] = merged_df['total_refugees'].fillna(0)

# Summing the total refugees for each year and Country of Asylum
result_total_ref_taken = df.groupby(['Year', 'Country of asylum'])['total_refugees'].sum().reset_index()
spi = pd.merge(result_total_ref_taken, spi, left_on=['Year', 'Country of asylum'], right_on=['Year', 'Nation_Destination'])

# Check for wrong country names
# Get unique names from 'Country of origin' and 'Country of asylum'
unique_names_origin = set(spi['Nation_Destination'].unique())
unique_names_asylum = set(spi['Country of asylum'].unique())

# Find common and distinct elements
common_names = unique_names_origin.intersection(unique_names_asylum)
distinct_names_origin = unique_names_origin.difference(unique_names_asylum)
distinct_names_asylum = unique_names_asylum.difference(unique_names_origin)

# Display the results
print("Common Names:", common_names)
print("Distinct Names from 'Country of origin':", distinct_names_origin)
print("Distinct Names from 'Country of asylum':", distinct_names_asylum)
# None found!
spi = spi.drop(['Country of asylum'], axis=1)
# check for nan values
#nan_values = spi.isna().sum()

# drop all unknown country names ither for home or destination country
df_cleaned = df[(df['Country of origin'].str.strip() != 'Unknown') & (df['Country of asylum'].str.strip() != 'Unknown')]

spi = pd.merge(spi, df_cleaned,  how='left', left_on=['Year','Nation_Origin','Nation_Destination']\
        , right_on = ['Year','Country of origin', 'Country of asylum'])
spi = spi.drop(['Country of origin', 'Country of asylum'], axis=1)
spi = spi.rename(columns={"total_refugees_x": "total_refugees", "total_refugees_y": "bilateral_refugees"})
# order columns for readability
spi = spi[['Year', 'Nation_Origin', 'Nation_Destination',
       'polity_origin', 'state_type_origin', 'cpi_origin',
       'Science_score_origin', 'Unesco_cumulative_origin',
       'polity_destination', 'state_type_destination', 'cpi_destination',
       'Science_score_destination', 'Unesco_cumulative_destination',
       'Int_Students', 'CSI_Value','total_refugees', 'bilateral_refugees']]

# check for nan values
nan_values = spi.isna().sum()
# fill nan values
#spi["bilateral_refugees"] = spi["bilateral_refugees"].fillna(0, inplace=True)
spi['bilateral_refugees'] = spi['bilateral_refugees'].fillna(0)
spi.to_csv("spi_clean2.csv", index=False)
"""
Migration
"""
migration = pd.read_csv(path_cleaning + "/Migration/migrants_clean_interpolation.csv")

spi = pd.merge(spi, migration, left_on=['Year', 'Nation_Origin', 'Nation_Destination'],
                     right_on=['Year', 'Origin_Country', 'Destination_Country'], how='left')

# Drop duplicate columns from the merge
spi = spi.drop(['Origin_Country', 'Destination_Country'], axis=1)
# Fill in nan values with 0;
# these are the missing connections where either no data or no migration happened.
spi['amount_migrants'] = spi['amount_migrants'].fillna(0)
print("NaN values summed per column in spi:")
print(spi.isna().sum())

spi["Origin_Destination"] = spi["Nation_Origin"] + "-" + spi["Nation_Destination"]
# order columns for readability
spi = spi[['Year', 'Nation_Origin', 'Nation_Destination', 'Origin_Destination',
       'polity_origin','state_type_origin', 'cpi_origin', 'Science_score_origin',
              'Unesco_cumulative_origin', 'polity_destination',
              'state_type_destination', 'cpi_destination',
              'Science_score_destination', 'Unesco_cumulative_destination',
              'Int_Students', 'CSI_Value', 'total_refugees', 'bilateral_refugees',
              'amount_migrants',]]

# Turn Values to int

column_names_int = ['Unesco_cumulative_destination', 'Unesco_cumulative_origin',
                'cpi_origin', 'cpi_destination',
                'Science_score_origin', 'Science_score_destination',
                'Int_Students',
                'CSI_Value',
                'bilateral_refugees',
                'amount_migrants']

# Iterating over the list of column names and converting them to integers
for column_name in column_names_int:
    spi[column_name] = spi[column_name].astype(int)

# Add SPI_Score row with only 0's
spi["SPI_Score"] = 0
spi.to_csv("spi_clean2.csv", index=False)