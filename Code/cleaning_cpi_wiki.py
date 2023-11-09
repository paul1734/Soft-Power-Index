import pandas as pd
import os
import numpy as np
import copy

"""
data from https://en.wikipedia.org/wiki/Corruption_Perceptions_Index
using https://wikitable2csv.ggor.de/
 Additional data from 2010 and 2011 from https://www.transparency.org/en/cpi/2010
 and https://www.transparency.org/en/cpi/2011
"""
os.getcwd()
path = "/files"
os.chdir(path)

cpi5 = pd.read_csv("Corruption_Perceptions_Index_5.csv")
cpi4 = pd.read_csv("Corruption_Perceptions_Index_4.csv")
cpi3 = pd.read_csv("Corruption_Perceptions_Index_3.csv")
cpi2 = pd.read_csv("Corruption_Perceptions_Index_2.csv")

cpi_10 = pd.read_csv("CPI_2010.csv")
cpi_11 = pd.read_csv("CPI_2011.csv")

list_cpi_add = [cpi_10, cpi_11]


for df in list_cpi_add:
    df.drop(['iso', 'region', 'rank', 'interval'], axis=1, inplace=True)
    

list_cpi_clean = [cpi2, cpi3, cpi4, cpi5]
# Loop through the list of DataFrames and drop the first row from each DataFrame
# Drop add column showing change ending in XXXX.1
# Rename "COuntry or Territory" to "Nation"
for df in list_cpi_clean:
    df.drop(0, axis=0, inplace=True)
    df.drop('#', axis=1, inplace=True)
    cols_to_drop = [col for col in df.columns if col.endswith('.1')]
    df.drop(cols_to_drop, axis=1, inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.columns.values[0] = 'Nation'
    #df = df.replace({'—':np.nan, 'nan':np.nan})
    df = df.infer_objects()
    # Reset the index after dropping rows
#test1 = cpi5.iloc[:,1:].apply(pd.to_numeric)
# Now the original DataFrames have the first row and undesired columns removed and are modified in place

# Merge cpi_10 into cpi3 for the year 2010 using 'Nation' as the common column
cpi3 = pd.merge(cpi3, cpi_10, left_on='Nation', right_on='country', how='left')
# Merge cpi_11 into cpi3 for the year 2011 using 'Nation' as the common column
cpi3 = pd.merge(cpi3, cpi_11, left_on='Nation', right_on='country', how='left')
# Drop the 'country' columns from the merged DataFrames
cpi3.drop(columns=['2010', '2011', 'country_x', 'country_y'], inplace=True)
cpi3 = cpi3.rename(columns={'score_x': '2010', 'score_y': '2011'})


cpi2 = cpi2.replace({'—':np.nan, 'nan':np.nan})
cpi3 = cpi3.replace({'—':np.nan, 'nan':np.nan})
cpi4 = cpi4.replace({'—':np.nan, 'nan':np.nan})
cpi5 = cpi5.replace({'—':np.nan, 'nan':np.nan})

cpi2 = cpi2.infer_objects()
cpi3 = cpi3.infer_objects()
cpi4 = cpi4.infer_objects()
cpi5 = cpi5.infer_objects()

list_cpi_clean = [cpi2, cpi3, cpi4, cpi5]

for df in list_cpi_clean:
    df.iloc[:,1:] = df.iloc[:,1:].apply(pd.to_numeric)
    
# Data from 2010 - 1995 is in a different format
# Index then is from 0-10, the current is from 0-100
# Multiply former Index by 10 to get the same format

cpi3.iloc[:,9:] = cpi3.iloc[:,9:].mul(10)
cpi4.iloc[:,1:] = cpi4.iloc[:,1:].mul(10)
cpi5.iloc[:,1:] = cpi5.iloc[:,1:].mul(10)

cpi_test5 = copy.deepcopy(cpi5)
cpi_test4 = copy.deepcopy(cpi4)
cpi_test3 = copy.deepcopy(cpi3)
cpi_test2 = copy.deepcopy(cpi2)
"""
# WORKING WELL
# DATA IS CLEANED AND TURNED TO NUMERIC VALUES

# Data from 2010 - 1995 is in a different format
# Index then is from 0-10, the current is from 0-100
# Multiply former Index by 10 to get the same format  
""" 
# Concatenate dataframes and fill missing values with NaN


result = pd.concat([df.set_index('Nation') for df in list_cpi_clean], axis=1).reset_index()
result_bfill = result.fillna(method='bfill', axis=1)
result = result_bfill.fillna(method='ffill', axis=1)
print(result)
result.to_csv('/files/CPI_Index.csv') 
# Concatenate the DataFrames vertically
#merged_df = pd.concat(list_cpi_clean)

#merged_df = merged_df.apply(pd.to_numeric, errors='ignore')
#print(merged_df)


