#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 12:36:18 2023

@author: -
"""
import sys
sys.path.append('/files/test_master_spi')

import pandas as pd
import country_converter as coco
import numpy as np
from config import path_cleaning
import os

"""
# Read Table 1: International migrant stock at mid-year by sex and by region, 
# country or area of destination and origin, 1990-2020
# Source: https://www.un.org/development/desa/pd/content/international-migrant-stock
"""

"""
# Delete useless columns and save in modified .csv
df_migration = pd.read_excel(path + "migration_un_data_1990_2020.xlsx", \
                             sheet_name="Table 1", header=10)
# delete double index col
df_migration = df_migration.drop(['Index'], axis=1)
# delete all columns with separate sexes
df_migration = df_migration.drop(
    ['1990.1','1995.1','2000.1','2005.1','2010.1','2015.1','2020.1',
    '1990.2','1995.2','2000.2','2005.2','2010.2','2015.2', '2020.2'], axis=1)

df_migration.to_csv(path + 'migration_un_data_coldrop.csv', index=False) 
# Only keep country names
"""
df_orig = pd.read_csv(path_cleaning + "/Migration/migration_un_data_coldrop.csv")
"""
# Only keep country names in rows
# get unique destination and origin names
columns names:
'Region, development group, country or area of destination',
       'Notes of destination', 'Location code of destination',
       'Type of data of destination',
       'Region, development group, country or area of origin',
"""
df = df_orig.copy()
df = df.rename(\
columns={"Region, development group, country or area of destination": "Destination_Country",
"Region, development group, country or area of origin":"Origin_Country", })

df = df.drop(['Notes of destination',
       'Location code of destination', 
       'Type of data of destination',
       'Location code of origin'], axis=1)

# Check for nan values -> False
df.isnull().values.any()
# List of all regions, non-countries etc.
not_countries = [
    'WORLD', '  Sub-Saharan Africa',
           '  Northern Africa and Western Asia',
           '  Central and Southern Asia', '  Eastern and South-Eastern Asia',
           '  Latin America and the Caribbean',
           '  Oceania (excluding Australia and New Zealand)',
           '  Australia and New Zealand', '  Europe and Northern America',
           '  Developed regions', '  Less developed regions',
           ' Less developed regions, excluding least developed countries',
           ' Less developed regions, excluding China',
           '  Least developed countries',
           '  Land-locked Developing Countries (LLDC)',
           '  Small island developing States (SIDS)',
           '  High-income countries', '  Middle-income countries',
           ' Upper-middle-income countries', ' Lower-middle-income countries',
           '  Low-income countries', ' AFRICA', '  Eastern Africa',
           '  Middle Africa', '  Northern Africa', '  Southern Africa',
           '  Western Africa', ' ASIA', '  Central Asia', '  Eastern Asia',
           '  South-Eastern Asia', '  Southern Asia', '  Western Asia',
           ' EUROPE', '  Eastern Europe', '  Northern Europe',
           '  Southern Europe', '  Western Europe',
           ' LATIN AMERICA AND THE CARIBBEAN', '  Caribbean',
           '  Central America', '  South America', ' NORTHERN AMERICA',
           ' OCEANIA ', 'Other']

for name in not_countries:    
    df = df.drop(df[df['Origin_Country'] == name].index)
    df = df.drop(df[df['Destination_Country'] == name].index)
  
# Clean Country column values from * 
df['Origin_Country'] = df['Origin_Country'].str.replace('*', '', regex=False)
df['Destination_Country'] = df['Destination_Country'].str.replace('*', '', regex=False)
# Clean Country names from leading and trailing spaces
def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)
df = trim_all_columns(df)
    
non_coco = ['Saint-Martin', 'Tuvalu', 'Turks and Caicos Islands', 
                         'South Georgia and South Sandwich Is.', 
                         'St. Vincent and the Grenadines', 'Norfolk Island', 
                         'Iceland', 'Tonga', 'Reunion', 
                         'Svalbard and Jan Mayen Islands', 'Samoa', 'Malta', 
                         'Greenland', 'Macau', 'Puerto Rico', 
                         'British Virgin Islands', 'Tokelau', 
                         'Wallis and Futuna Islands', 'Curacao', 'South Sudan',
                         'Heard and McDonald Islands', 'Niue', 'Marshall Islands',
                         'Vanuatu', 'Falkland Islands', 'St. Lucia', 'Maldives',
                         'United States Minor Outlying Islands', 'Montenegro', 
                         'Sao Tome and Principe', 'Mayotte', 'Cayman Islands', 
                         'Hong Kong', 'Cocos (Keeling) Islands', 'St. Helena', 
                         'New Caledonia', 'Cook Islands', 'Andorra', 'Grenada',
                         'Aruba', 'Montserrat', 'French Guiana', 'American Samoa', 
                         'Micronesia, Fed. Sts.', 'San Marino', 
                         'St. Kitts and Nevis', 'Palestine', 'Antigua and Barbuda',
                         'Timor-Leste', 'Dominica', 'Serbia', 'Kiribati', 
                         'Faeroe Islands', 'Palau', 'Bermuda', 'Vatican', 
                         'French Southern Territories', 'Liechtenstein', 'Nauru',
                         'British Indian Ocean Territory', 'Bahamas', 'Guam',
                         'Barbados', 'French Polynesia', 'Martinique', 'Guadeloupe',
                         'Western Sahara', 'St. Pierre and Miquelon', 'Belize', 
                         'United States Virgin Islands', 'Brunei Darussalam', 
                         'Christmas Island', 'Sint Maarten', 'Pitcairn',
                         'Northern Mariana Islands', 'Seychelles', 'Anguilla', 
                         'Gibraltar', 'Bouvet Island', 'Monaco', 
                         'China, Taiwan Province of China',
                         'Melanesia', 'Polynesia', 'Channel Islands']

for name in non_coco:    
    df = df.drop(df[df['Origin_Country'].str.strip() == name].index)
    df = df.drop(df[df['Destination_Country'].str.strip() == name].index)
    
"""
For some reasons not all countries are dropped, using a different method:
More then one regular expression match for China, Taiwan Province of China
Channel Islands not found in regex
Melanesia not found in regex
Polynesia not found in regex
"""
# Assuming your DataFrame is named 'df'
columns_to_check = ['Origin_Country', 'Destination_Country']
values_to_drop = ['Melanesia', 'Polynesia', 'Channel Islands',
                'China, Taiwan Province of China']

# Convert values to lowercase and strip whitespaces
values_to_drop_normalized = [value.lower().strip() for value in values_to_drop]

# Drop rows where either 'Origin_Country' or 'Destination_Country' contains any of the specified values
df = df[~df[columns_to_check].apply(lambda x: x.str.lower().str.strip()).isin(values_to_drop_normalized).any(axis=1)]


#country_list = pd.DataFrame()
#country_list["List"] = df["Destination_Country"].unique()
#country_list["List2"] = coco.convert(names=country_list["List"], to='name_short')

    
df["Origin_Country"] = coco.convert(names=df["Origin_Country"], to='name_short')
df["Destination_Country"] = coco.convert(names=df["Destination_Country"], to='name_short')

for name in non_coco:    
    df = df.drop(df[df['Origin_Country'].str.strip() == name].index)
    df = df.drop(df[df['Destination_Country'].str.strip() == name].index)

# check for nan values
nan_values_df = df.isna().sum()

# Turn to long format
df_long = pd.melt(df, id_vars=['Destination_Country', 'Origin_Country'], var_name='Year', value_name='Value')
df_long = df_long.infer_objects()
df_long["Year"] = pd.to_numeric(df_long["Year"])
df_long = df_long.rename(columns={"Value": "amount_migrants"})
# check for nan values
nan_values_df_long = df_long.isna().sum()
"""
# Insert all years from 1990 to 2020 and then interpolate between years
for year in range(1991, 2021):
    df_long = df_long.append({"Origin_Country": df_long.Origin_Country[0], "Destination_Country": df_long.Destination_Country[0], "Year": year}, ignore_index=True)
    df_long = df_long.append({"Origin_Country": df_long.Origin_Country[1], "Destination_Country": df_long.Destination_Country[1], "Year": year}, ignore_index=True)
"""


pivot_df = df_long.pivot_table(index=['Origin_Country', 'Destination_Country', 'Year'], values='amount_migrants', aggfunc='sum').reset_index()
nan_values_pivot_df = pivot_df.isna().sum()
# Create a range of years from 1990 to 2020 with 1-year steps
all_years = list(range(1990, 2021))

# Set the Origin_Country, Destination_Country as index and reindex with all_years
result_df = pivot_df.set_index(['Origin_Country', 'Destination_Country', 'Year'])\
  .reindex(pd.MultiIndex.from_product([pivot_df['Origin_Country'].unique(), \
  pivot_df['Destination_Country'].unique(), all_years], \
   names=['Origin_Country', 'Destination_Country', 'Year']))
nan_values_result_df = result_df.isna().sum()

# Initialize an empty DataFrame to store the result
result_df_intp = pd.DataFrame(columns=['Origin_Country', 'Destination_Country', 'Year', 'amount_migrants'])

# Interpolate values for each pair of 'Origin_Country' and 'Destination_Country'
for (origin, destination), group in pivot_df.groupby(['Origin_Country', 'Destination_Country']):
    interpolated_group = group.set_index('Year').reindex(all_years).interpolate(method='linear').reset_index()
    interpolated_group['Origin_Country'] = origin
    interpolated_group['Destination_Country'] = destination
    result_df_intp = pd.concat([result_df_intp, interpolated_group], ignore_index=True)

# Display the result
print(result_df_intp)
print(result_df_intp.isna().sum())

nan_values_result_df_intp = result_df_intp.isna().sum()

# Inspect specific rows with NaN values after interpolation
nan_rows = result_df_intp[result_df_intp.isna().any(axis=1)]
print("Rows with NaN values after interpolation:")
print(nan_rows)

# Inspect specific columns with NaN values after interpolation
nan_columns = result_df_intp.columns[result_df_intp.isna().any()]
print("\nColumns with NaN values after interpolation:")
print(nan_columns)

# Convert 'amount_migrants' to int
result_df_intp['amount_migrants'] = result_df_intp['amount_migrants'].astype(int)
result_df_intp.to_csv(path_cleaning + "/Migration/migrants_clean_interpolation.csv", index=False)
