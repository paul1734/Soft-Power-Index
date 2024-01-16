#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 11:40:01 2023

@author: -
"""
import pandas as pd

science_orig = pd.read_excel('scimagojr country rank 1996-2022.xlsx')
science_working = science_orig.drop(['Rank', 'Region'], axis=1)
# get rid of 0 in self citations, replace with 1

science_working['Self-citations'] = science_working['Self-citations'].replace(0, 1)

science_working['score'] = science_working['Citations'] * science_working\
['Citations per document'] / science_working['Self-citations']
