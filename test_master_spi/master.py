#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 11:58:48 2024

@author: -
"""
# master.py
import pandas as pd
import subprocess
import os
import sys
from config import path_cleaning
from config import path

"""
INSTALL THE FOLLOWING PACKAGES
pip install (package_name):
    - openpyxl
    - xlrd
    - pandas
    - country-converter
    - numpy
    - dash
    - matplotlib
    - requests
    - seaborn
    - scipy
    - scikit-learn 
    - itertools
    - re

"""

"""
Run Data Cleaning scripts
1) Data Cleaning
- migration_cleaning.py (DATA USED: migration_un_data_coldrop.csv)
    -> Creates: migrants_clean_interpolation.csv
- heritage_sites.py (DATA USED: Webscraping)
    -> Creates: Sum_Unesco.csv
- polity_data.py (DATA USED: p5v2018.xls
    -> Creates: polity_95.csv
science_country.py (DATA USED: "scimagojr country rank 1996 2022.xlsx")
    -> Creates: science_score.csv
cleaning_cpi_wiki.py (DATA USED: CPI_INDEX (2-5).csv; CPI 2010 / 2011.csv)
inter_students (DATA USED: unesco_wto)
    -> Creates: interpolated_inter_students.csv

2) Run data_cleaning_spi.py
CSI: DATA USED: contry-similarity-distance-matrix.csv
"""

"""
# Migration
subprocess.run(["python", path_cleaning + "/Migration/migration_cleaning.py"])
# UNESCO
subprocess.run(["python", path_cleaning + "/Unesco/heritage_sites.py"])
# Polity
subprocess.run(["python", path_cleaning + "/Polity/polity_data.py"])
# Science
subprocess.run(["python", path_cleaning + "/Science/science_country.py"])
# CPI
subprocess.run(["python", path_cleaning + "/CPI/cleaning_cpi_wiki.py"])
# International Students
subprocess.run(["python", path_cleaning + "/Education/inter_students.py"])
"""
# Run Data Cleaning scripts
subprocess.run([sys.executable, os.path.join(path_cleaning, "Migration", "migration_cleaning.py")])
subprocess.run([sys.executable, os.path.join(path_cleaning, "Unesco", "heritage_sites.py")])
subprocess.run([sys.executable, os.path.join(path_cleaning, "Polity", "polity_data.py")])
subprocess.run([sys.executable, os.path.join(path_cleaning, "Science", "science_country.py")])
subprocess.run([sys.executable, os.path.join(path_cleaning, "CPI", "cleaning_cpi_wiki.py")])
subprocess.run([sys.executable, os.path.join(path_cleaning, "Education", "inter_students.py")])



"""
SPI Creation: Combine the cleaned data from above to create the Soft Power Index
1) data_cleaning_spi.py
    -> Creates: spi_clean1.csv
2) data_cleaning_spi_contd.py
    -> Creates: spi_clean2.csv
3) single_spi_score.py

"""
"""
# Run SPI Scripts
subprocess.run(["python", "data_cleaning_spi.py"])
subprocess.run(["python", "data_cleaning_spi_contd.py"])
"""
# Run SPI Scripts
subprocess.run([sys.executable, os.path.join(path, "data_cleaning_spi.py")])
subprocess.run([sys.executable, os.path.join(path, "data_cleaning_spi_contd.py")])

