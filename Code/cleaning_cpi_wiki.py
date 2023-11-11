import pandas as pd
import os
import numpy as np
import copy
import country_converter as coco

"""
data from https://en.wikipedia.org/wiki/Corruption_Perceptions_Index
using https://wikitable2csv.ggor.de/
 Additional data from 2010 and 2011 from https://www.transparency.org/en/cpi/2010
 and https://www.transparency.org/en/cpi/2011
"""
os.getcwd()
path = "/files/CPI"
os.chdir(path)


"""
List CPI Annoying Countries Doubles

Kyrgyz Republic	56 | Kyrgyzstan
Slovakia	56 | Slovak Republic
Congo Republic	56 | Republic of the Congo
Czech Republic	56 | Czechia
Sao Tome and Principe 56 | S㯠Tom頡nd Pr�ipe
North Macedonia	56 | FYR Macedonia
Eswatini 56 | Swaziland

# Change 1995-1999 to equalize
Kyrgyzstan (2000 - 2022)
Kyrgyz Republic (1995 -1999)

# Change 1995-1999 to equalize
Slovakia (2000 - 2022)
Slovak Republic (1995 -1999)

Congo (2020 - 2022)
Republic of the Congo (2000 - 2019)
missing before

North Macedonia (2010 - 2022)
FYR Macedonia (1995-2009)

Eswatini (2010 - 2022)
Swaziland (2000 - 2009)
missing 1999 before

Czechia (2020 -2022)
Czech rep (1995 - 2019)

Sao Tome and Principe (2000 - 2009)
S㯠Tom頡nd Pr�ipe (2010 - 2022)
missing before

Nation | Number of appearances | Former double Counterpart (changed by coco)
Kyrgyz Republic	56 | Kyrgyzstan
Slovakia	56 | Slovak Republic
Congo Republic	56 | Republic of the Congo
Czech Republic	56 | Czechia
Sao Tome and Principe 56 | S㯠Tom頡nd Pr�ipe
North Macedonia	56 | FYR Macedonia
Eswatini 56 | Swaziland
"""

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
    #df = df.replace({'?':np.nan, 'nan':np.nan})
    df = df.infer_objects()
    # Reset the index after dropping rows
#test1 = cpi5.iloc[:,1:].apply(pd.to_numeric)
# Now the original DataFrames have the first row and undesired columns removed and are modified in place

cpi5['Nation'] = cpi5['Nation']\
    .replace({'Kyrgyz Republic':'Kyrgyzstan'})
cpi5['Nation'] = cpi5['Nation']\
    .replace({'Slovak Republic':'Slovakia'})
cpi5['Nation'] = cpi5['Nation']\
    .replace({'FYR Macedonia':'North Macedonia'})
cpi4['Nation'] = cpi4['Nation']\
    .replace({'FYR Macedonia':'North Macedonia'})
cpi4['Nation'] = cpi4['Nation']\
    .replace({'Swaziland':'Eswatini'})
cpi4['Nation'] = cpi4['Nation']\
    .replace({'Sao Tome and Principe':'S㯠Tom頡nd Pr�ipe'})  
cpi2['Nation'] = cpi2['Nation']\
    .replace({'Czechia':'Czech Republic'})
cpi2['Nation'] = cpi2['Nation']\
    .replace({'Congo':'Republic of the Congo'})

# Merge cpi_10 into cpi3 for the year 2010 using 'Nation' as the common column
cpi3 = pd.merge(cpi3, cpi_10, left_on='Nation', right_on='country', how='left')
# Merge cpi_11 into cpi3 for the year 2011 using 'Nation' as the common column
cpi3 = pd.merge(cpi3, cpi_11, left_on='Nation', right_on='country', how='left')
# Drop the 'country' columns from the merged DataFrames
cpi3.drop(columns=['2010', '2011', 'country_x', 'country_y'], inplace=True)
cpi3 = cpi3.rename(columns={'score_x': '2010', 'score_y': '2011'})


cpi2 = cpi2.replace({'?':np.nan, 'nan':np.nan})
cpi3 = cpi3.replace({'?':np.nan, 'nan':np.nan})
cpi4 = cpi4.replace({'?':np.nan, 'nan':np.nan})
cpi5 = cpi5.replace({'?':np.nan, 'nan':np.nan})

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
cpi_uniqueval = result['Nation'].value_counts()
# change to long format
cpi_long = pd.melt(result, id_vars=['Nation'], var_name='Year', value_name='Value')
# Check data, all countries should only appear once for every year
# all years should appear 198 times
cpi_uniqueval = pd.DataFrame()
cpi_uniqueval["count_country"] = cpi_long['Nation'].value_counts()
print(cpi_long['Year'].value_counts())

"""
Drop countries also dropped from polity data due to stated reasons

"""
dropped_countries = ["Serbia and Montenegro", "Yugoslavia",
"Czechoslovakia","Yemen North",
"Yemen South","Germany West","Germany East",
"South Sudan", "Kosovo","Serbia","Montenegro" , "Timor Leste"]

for name in dropped_countries:    
    cpi_long = cpi_long.drop(cpi_long[cpi_long['Nation'] == name].index)



cpi_long2 = pd.DataFrame()
cpi_long["Nation"] = coco.convert(names=cpi_long["Nation"], to='name_short')
cpi_uniqueval2 = cpi_long['Nation'].value_counts()

cpi_long.to_csv(path + '/CPI_Index.csv')
