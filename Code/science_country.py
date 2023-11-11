#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 11:40:01 2023

@author: -
"""
import pandas as pd
import numpy as np
import os 
import country_converter as coco

os.getcwd()
path = "/files/Science/"
os.chdir(path)

science_orig = pd.read_excel('scimagojr country rank 1996-2022.xlsx')
science_working = science_orig.drop(['Rank', 'Region'], axis=1)
# get rid of 0 in self citations, replace with 1
# otherwise will get infinity in future calculations
science_working['Self-citations'] = science_working['Self-citations'].replace(0, 1)
science_working = science_working.sort_values(by='Citations', ascending=True)

#filtered_science_df = science_working[science_working['Citations'] >= 2000]
filtered_science_df = science_working.copy()
# Netherlands Antilles not found in regex
filtered_science_df = filtered_science_df.drop(filtered_science_df\
                    [filtered_science_df['Country'] == "Netherlands Antilles"].index)
filtered_science_df["Country"] = coco.convert(names=filtered_science_df["Country"],\
                                            to='name_short')
# Check for number of countries
filtered_science_df_val = filtered_science_df['Country'].value_counts()

science = filtered_science_df.copy()
science = science.rename(columns={"Country":"Nation"})
science["% Self-citations"] = science["Self-citations"] / science["Citations"]
# Amount of global foreign citations per country
science["Foreign relevance"] = (science["Citations"] - science["Self-citations"] )/ sum(science["Citations"])*100
# turn into percentage
science["Foreign relevance"] = science["Foreign relevance"] / sum(science["Foreign relevance"]) *100
science["Global relevance"] = science["Citations"]/sum(science["Citations"])*100

science["%H_index"] = science["H index"] / max(science["H index"])*100

"""
Interesting observation:
    -> Strong possible correlation between nominal BIP  and global relevance percentage
"""

science["Score"] =  (science["%H_index"] * science["Citations per document"]) *\
    science["Foreign relevance"] * science["Global relevance"]

# turn score into percentage
science["Score"] = (science["Score"] / max(science["Score"])*100)
science["Score_log"] = np.log2(science["Score"]+1)
science["%Score_log"] = science["Score_log"]/ max(science["Score_log"])*100

science_score = pd.DataFrame()
science_score["Nation"] = science["Nation"]
science_score["Science_score"] = science["%Score_log"]

science_score.to_csv("science_score.csv", index=False)

"""
Explanation of Score:
score = %HI * C/D * %_foreign_citations * %_global_citations

Further score calculations
1. Take Percentage of score to comapre between countries 
2. Take log2 of Score +1 (No negative values)
3. Take percentage again

Abbreviation: (expected relationship of science on soft power)
FC: foreign relevance (+)
HI: % H Index (+)
C/D: (citation / document) (+)
(C / Glob_C): Citations / Total Global Citations as percentage (+)
"""

# =============================================================================
# VISUALIZE WITH BAR PLOT AND GEOPANDAS
# =============================================================================
import seaborn as sns
import matplotlib.pyplot as plt

# Filter the data for Science scores above 1
filtered_data = science_score[science_score['Science_score'] > 1]

# Sort the filtered data by 'Science_score' in descending order
sorted_data = filtered_data.sort_values('Science_score', ascending=False)

# Create a bar plot with custom colors
plt.figure(figsize=(10, 6))
sns.barplot(x='Science_score', y='Nation', data=sorted_data, palette='viridis')
plt.xlabel('Science Score')
plt.ylabel('Nation')
plt.title('Science Scores for Nations (Scores > 1)')
plt.show()

import geopandas as gpd
# Rename some nations with two separate names
science_score['Nation'] = science_score['Nation']\
    .replace({'United States':'United States of America'})
    
filtered_data = science_score[science_score['Science_score'] > 1]
# Load a world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Create a plot
fig, ax = plt.subplots(1, 1, figsize=(15, 10))

# Plot all countries from the world dataset
world.plot(ax=ax, color='lightgrey')

# Plot countries with data and merge them with the map
merged = world.merge(science_score, how='left', left_on='name', right_on='Nation')
merged.plot(column='Science_score', ax=ax, legend=True, legend_kwds={'label': "Science Scores", 'orientation': "horizontal"})

plt.title('Science Scores for Nations')
plt.show()

