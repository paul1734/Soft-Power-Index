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

# Convert 'Year' to the same data type in both DataFrames
polity_data['year'] = polity_data['year'].astype(int)
cpi_long['Year'] = cpi_long['Year'].astype(int)

# inner starts at 1995 but polity alredy starts at 1990
spi_inner = pd.merge(polity_data, cpi_long, left_on=['country', 'year'], \
            right_on=['Nation','Year'], how='inner')
spi_inner = spi_inner.rename(columns={"Value": "cpi"})
# create outer, maybe interpolation for cpi is possible
spi_outer = pd.merge(polity_data, cpi_long, left_on=['country', 'year'], \
            right_on=['Nation','Year'], how='outer')
spi_outer = spi_outer.rename(columns={"Value": "cpi"})

# use outer
# Interpolate the data for cpi before 1995
# Interpolate data for polity after 2018