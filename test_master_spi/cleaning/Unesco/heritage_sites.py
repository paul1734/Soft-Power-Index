#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 13:57:21 2023

@author: -
"""
import sys
sys.path.append('/files/test_master_spi')

import pandas as pd
import os
import numpy as np
import copy
import country_converter as coco
from config import path_cleaning
"""
UNESCO WORLD HERITAGE SITES
data from https://en.wikipedia.org/wiki/World_Heritage_Sites_by_country
"""


# Webpage url                              
"""
url:
As of September 2023, there are a total of 1,199 World Heritage Sites located 
across 168 countries, of which 933 are cultural, 227 are natural, and 39 are 
mixed properties.
"""                                                                                 
url = 'https://en.wikipedia.org/wiki/World_Heritage_Sites_by_country'

"""
url2: World Heritage List
with Year of monument being added to list for each country
    
"""
url2 = 'https://whc.unesco.org/en/list/?order=year&mode=table'
# Extract tables
#dfs = pd.read_html(url)
dfs2 = pd.read_html(url2)
# Get first table                                                                                                           
#df = dfs[0]
#print(df[df['Country'].isnull()])
df2 = dfs2[2]
df2.loc[df2['Country'].isnull()]
"""
No Country Name given
1) Israel
2) and 3) Namibia

      Year                 Name of the property  ... Property (ha)    ID
105   1981  Old City of Jerusalem and its Walls  ...             0   148
902   2007           Twyfelfontein or /Ui-//aes  ...            57  1255
1039  2013                       Namib Sand Sea  ...       3077700  1430

[3 rows x 7 columns]
"""
# Insert ISO2 into df
df2.at[105, 'Country'] = 'IL'
df2.at[902, 'Country'] = 'NA'
df2.at[1039, 'Country'] = 'NA'
check_iso = df2["Country"].unique()

# rename column
#df = df.rename(columns={"Country": "Nation"})
df2 = df2.rename(columns={"Country": "Nation"})
# Country Conversion
#df["Nation"] = coco.convert(names=df["Nation"], to='name_short')
df2["Nation"] = coco.convert(names=df2["Nation"], to='name_short')

df2 = df2.drop(['Name of the property', 'Type', 'Region',
       'Property (ha)', 'ID'], axis=1)

# Assuming your DataFrame is named df
#df2['Unesco_cumulative'] = df2.groupby(['Nation'])['Year'].cumcount() + 1
# Drop Year 2023
df2 = df2[df2['Year'] != 2023]
# Sort the DataFrame by 'Year' and 'Nation'
df2 = df2.sort_values(by=['Year', 'Nation'])
# Filter out rows where 'Year' is 2021 or 2022
df2 = df2[~df2['Year'].isin([2021, 2022])]
# Group by 'Year' and 'Nation' and calculate the cumulative count
df2['Unesco_cumulative'] = df2.groupby(['Year', 'Nation']).cumcount() + 1

# Get the maximum cumulative value for each 'Year' and 'Nation'
df2['Unesco_cumulative'] = df2.groupby(['Year', 'Nation'])['Unesco_cumulative'].transform('max')
df2 = df2.drop_duplicates()
df = df2.copy()
# Grouping by 'Nation' and calculating cumulative sum
df['Unesco_cumulative'] = df.groupby('Nation')['Unesco_cumulative'].cumsum()

# Creating a DataFrame with all combinations of 'Year' and 'Nation'
all_combinations = pd.DataFrame([(year, country) for year in df['Year'].unique() for country in df['Nation'].unique()],
                                columns=['Year', 'Nation'])

# Merging the original DataFrame with all_combinations
filled_df = pd.merge(all_combinations, df, on=['Year', 'Nation'], how='left')

# Sorting the DataFrame by 'Year' and 'Nation'
filled_df = filled_df.sort_values(by=['Year', 'Nation'])

# Forward-filling NaN values in 'Unesco_cumulative'
filled_df['Unesco_cumulative'] = filled_df.groupby('Nation')['Unesco_cumulative'].transform(lambda x: x.ffill())

# Filling NaN values in 'Unesco_cumulative' with 0
filled_df['Unesco_cumulative'] = filled_df['Unesco_cumulative'].fillna(0)
# Save file
filled_df.to_csv(path_cleaning + "/Unesco/Sum_Unesco.csv", index=False)

"""
all_countries = df2['Nation'].unique()
# Then we create a DataFrame with all combinations of Year and Nation
all_combinations2 = pd.DataFrame([(year, country) for year in df2['Year'].unique() for country in all_countries],
                                columns=['Year', 'Nation'])
# Merge the original DataFrame with all_combinations
filled_df2 = pd.merge(all_combinations2, df2, on=['Year', 'Nation'], how='left')
# The year 2020 is missing in the UNESCO data; add it based on 2019 values
df_2020 = pd.DataFrame({'Year': [2020] * len(filled_df2['Nation'].unique())})
# Add the unique nations to the DataFrame
df_2020['Nation'] = filled_df2['Nation'].unique()
# Merge the DataFrames on 'Year' and 'Nation'
filled_df2 = pd.merge(filled_df2, df_2020, how='outer', on=['Year', 'Nation'])
# Fill NaN values in 'Unesco_cumulative' with the values from 2019
filled_df2['Unesco_cumulative'] = filled_df2.groupby('Nation')['Year'].transform(lambda x: x.ffill())
# Handle NaN values in 'Unesco_cumulative' for the year 2020
filled_df2['Unesco_cumulative'] = filled_df2.groupby('Nation')['Unesco_cumulative'].transform(lambda x: x.fillna(method='ffill'))
filled_df2['Unesco_cumulative'] = filled_df2['Unesco_cumulative'].fillna(0)

# Sort the DataFrame by 'Year' and 'Nation'
filled_df2 = filled_df2.sort_values(by=['Year', 'Nation']).reset_index(drop=True)

# Drop Years before 1990
filled_df2 = filled_df2[filled_df2['Year'] >= 1990]

# Save file
filled_df2.to_csv(path_cleaning + "/Unesco/Sum_Unesco.csv", index=False)
"""
"""
# Merge the original DataFrame with all_combinations
filled_df2 = pd.merge(all_combinations2, df2, on=['Year', 'Nation'], how='left')
# Fill NaN values in 'Unesco_cumulative' with the last years available 
# cumulative value using ffill
filled_df2['Unesco_cumulative'] = filled_df2.groupby('Nation')['Unesco_cumulative'].transform(lambda x: x.ffill())
# now the only nan left are from the years before where
filled_df2['Unesco_cumulative'] = filled_df2['Unesco_cumulative'].fillna(0)
"""
"""
# The year 2020 is missing in the UNESCO data; add it based on 2019 values
df_2020 = pd.DataFrame({'Year': [2020] * len(filled_df2['Nation'].unique())})
# Add the unique nations to the DataFrame
df_2020['Nation'] = filled_df2['Nation'].unique()
# Merge the DataFrames on 'Year' and 'Nation'
filled_df2 = pd.merge(filled_df2, df_2020, how='outer', on=['Year', 'Nation'])
# Fill NaN values in 'Unesco_cumulative' with the values from 2019
filled_df2['Unesco_cumulative'] = filled_df2.groupby('Nation')['Unesco_cumulative'].transform(lambda x: x.fillna(method='ffill'))
# Sort the DataFrame by 'Year' and 'Nation'
filled_df2 = filled_df2.sort_values(by=['Year', 'Nation']).reset_index(drop=True)

# Drop Years before 1990
filled_df2 = filled_df2[filled_df2['Year'] >= 1990]
# Save file
filled_df2.to_csv(path_cleaning + "/Unesco/Sum_Unesco.csv", index=False)
"""