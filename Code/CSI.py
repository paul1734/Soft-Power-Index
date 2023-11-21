#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 10:30:18 2023

@author: -
"""

import pandas as pd
import numpy as np
import os 
import country_converter as coco

os.getcwd()
path = "/files/"
os.chdir(path)

csi = pd.read_csv("country-similarity-distance-matrix.csv")
csi.dtypes
csi.infer_objects().dtypes  
csi = csi.rename(columns={"Unnamed: 0":"Nation"})

df = csi.copy()
df = df.set_index('Nation')
# Create an empty DataFrame to store the long-format data
long_format_df = pd.DataFrame(columns=['Country1', 'Country2', 'CSI'])

# Loop through the original DataFrame to extract direct bilateral relationships
for country1 in df.index:
    for country2 in df.columns:
        if country1 != country2:  # Exclude self-reference
            csi_value = df.loc[country1, country2]
            long_format_df = long_format_df.append({'Country1': country1, 'Country2': country2, 'CSI': csi_value},
                                                   ignore_index=True)

# Print or further analyze the long-format DataFrame
print(long_format_df)
long_format_df.to_csv("/files/long_csi.csv")  
