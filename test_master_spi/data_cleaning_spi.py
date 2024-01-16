import sys
sys.path.append('/files/test_master_spi')

import pandas as pd 
import numpy as np
import os
import country_converter as coco
from itertools import combinations
from config import path_cleaning



"""
Overview of Data Cleaning:
U1 - U4: Combine Unilateral data with each other
S1. Split data into two separate df's; one for source, one for destination country
B1. -: Append Bilateral data to either source or destination df
Final: Combine the two dataframes into one and calculate Soft Power Score
-----Unilateral------
U1. Combining Polity and Corruption Perceptions Index
	1.1 Find and delete mismatched country names
	1.2 Extrapolate the data for cpi before 1995 and for polity after 2018
	1.3 Fill in missing values
2. Import and combine Science data
3. Import and combine Unesco data
4. Import and combine Country Similarity Index
--------------------
S1. Create bilateral country df from 1990 to 2020, for destination and source country
------Bilateral------
B1. Import and combine International Student data

"""
########################################
# 1. Combining Polity and Corruption Perceptions Index
########################################
# Start with combining Polity and CPI data
polity_data = pd.read_csv(path_cleaning + '/Polity/polity95.csv')
# convert cpi to long format
cpi_long = pd.read_csv(path_cleaning + "/CPI/CPI_Index.csv", index_col=0)
# cpi has 198 countries (see cpi data), polity has 178
polity_data["Nation"].nunique()
#polity_data = polity_data.rename(columns={"country": "Nation", "year": "Year"})

# CPI has complete data for all 28 years
cpi_long_uniqueval = cpi_long['Nation'].value_counts()
# Drop countries with only little (less than 5 years)
polity_uniqueval = polity_data['Nation'].value_counts()
####
# 1.1     
# Find and delete mismatched country names
polity_countries = set(polity_data["Nation"].unique())
cpi_countries = set(cpi_long["Nation"].unique())

mismatched_countries = polity_countries.symmetric_difference(cpi_countries)
print(mismatched_countries)

# The following countries are not present in Polity 5-
# Countries not available in Polity5 will be dropped
# Thankfully mostly small island nations or nations with 
# geopolitically unresolved disputes, i.e. difficulty of finding 
# further data
unmatched_countries = ['Samoa', 'Puerto Rico', 'St. Vincent and the Grenadines', 
'Sao Tome and Principe', 'Maldives', 'Iceland', 'Brunei Darussalam', 
'Grenada', 'Kiribati', 'St. Lucia', 'Barbados', 'Timor-Leste', 'Belize', 
'Seychelles', 'Palestine', 'Dominica', 'Tonga', 'Bahamas', 'Vanuatu', 
'Hong Kong', 'Macau', 'Malta']

for name in unmatched_countries:    
    polity_data = polity_data.drop(polity_data[polity_data['Nation'] == name].index)
    cpi_long = cpi_long.drop(cpi_long[cpi_long['Nation'] == name].index)

# Convert 'Year' to the same data type in both DataFrames
polity_data['Year'] = polity_data['Year'].astype(int)
cpi_long['Year'] = cpi_long['Year'].astype(int)

####
# 1.2 Extrapolate the data for cpi before 1995 and for polity after 2018
# inner starts at 1995 but polity alredy starts at 1990
spi_inner = pd.merge(polity_data, cpi_long, left_on=['Nation', 'Year'], \
            right_on=['Nation','Year'], how='inner')
spi_inner = spi_inner.rename(columns={"Value": "cpi"})

spi_outer = pd.merge(polity_data, cpi_long, left_on=['Nation', 'Year'], \
            right_on=['Nation','Year'], how='outer')
spi_outer = spi_outer.rename(columns={"Value": "cpi"})

spi_outer = spi_outer.sort_values(by=['Nation','Year'])

# CPI has complete data for all 28 years
spi_uniqueval = spi_outer['Nation'].value_counts()
# Count NaN values in 'polity' and 'cpi' columns grouped by 'Nation'
nan_counts = spi_outer.groupby('Nation')[['polity', 'cpi']].apply(lambda x: x.isna().sum())
# Filter out rows where either 'polity' or 'cpi' is above 5
test_nan = nan_counts[(nan_counts['polity'] >= 6) | (nan_counts['cpi'] >= 6)]
# Extrapolate the data for cpi before 1995
# Extrapolate data for polity after 2018

# Sort the data by Nation and Year
panel_data = spi_outer.sort_values(by=['Nation', 'Year'])

# Group the data by Nation and fill missing values within each group
filled_data = panel_data.groupby('Nation').apply(
    lambda x: x.ffill().bfill())


# Filter years 2022 and 2021 from data
filled_data = filled_data[~filled_data['Year'].isin([2021, 2022])].reset_index(drop=True)
spi_data = filled_data.reset_index(drop=True)
spi_data = spi_data.sort_values(by=['Nation', 'Year'])
spi_data = spi_data.apply(lambda x: x.ffill().bfill())
"""
# Reset the index after filling missing values in spi_data due to merging
spi_data = filled_data.reset_index(drop=True)
spi_data = spi_data.sort_values(by=['Nation', 'Year'])
spi_data = spi_data.apply(lambda x: x.ffill().bfill())
#spi_data = spi_data.sort_values(by=['Nation', 'Year'])
spi_data = spi_data.bfill(limit=1)
"""


########################################
# 2. Import and combine Science data
########################################
science = pd.read_csv(path_cleaning + '/Science/science_score.csv')
# Find mismatched country names
spi_data_c = set(spi_data["Nation"].unique())
science_c = set(science["Nation"].unique())

mismatched_c2 = spi_data_c.symmetric_difference(science_c)
print(mismatched_c2)

unmatched_countries_2 = ['Saint-Martin', 'Tuvalu', 'Turks and Caicos Islands', 
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
                         'Gibraltar', 'Bouvet Island', 'Monaco', 'Faroe Islands']
# Merge to SPI_data
spi_data = pd.merge(spi_data, science, on="Nation", how='outer')
for name in unmatched_countries_2:    
    spi_data = spi_data.drop(spi_data[spi_data['Nation'] == name].index)

spi_data = spi_data.astype({'Year':'int', 'polity':'int'})
########################################
# 3. Import and combine Unesco data
########################################
unesco = pd.read_csv(path_cleaning + "/Unesco/Sum_Unesco.csv")
# Drop Czech Data by row index which appears twice
"""
	Year	Nation	Unesco_cumulative
210	1991	Czech Republic	0.0
386	1992	Czech Republic	1.0
387	1992	Czech Republic	2.0
388	1992	Czech Republic	3.0

"""
unesco = unesco.drop([386, 387])
# Find mismatched country names
spi_data_c = set(spi_data["Nation"].unique())
unesco_c = set(unesco["Nation"].unique())

mismatched_c3 = spi_data_c.symmetric_difference(unesco_c)
print(mismatched_c3)

unmatched_countries_3 = ['Vanuatu', 'Djibouti', 'Montenegro', 'Guinea-Bissau', 
   'Iceland', 'Palau', 'Kuwait', 'Barbados', 'Andorra', 'St. Lucia', 'Vatican', 
  'Seychelles', 'Serbia', 'Antigua and Barbuda', 'Guyana', 'Trinidad and Tobago', 
 'Dominica', 'Equatorial Guinea', 'Eswatini', 'Somalia', 'Kiribati', 'Comoros',
 'Taiwan', 'Belize', 'Palestine', 'San Marino', 'Malta', 'Marshall Islands', 
 'St. Kitts and Nevis', 'Burundi', 'Sierra Leone', 'Bhutan', 'Liberia', 
 'Micronesia, Fed. Sts.']

spi_data = pd.merge(spi_data, unesco, on=["Nation", "Year"], how='outer')
for name in unmatched_countries_3:    
    spi_data = spi_data.drop(spi_data[spi_data['Nation'] == name].index)



spi_data = spi_data.sort_values(by=['Nation', 'Year'])
spi_data = spi_data.bfill(limit=1)
spi_data = spi_data.query('Year not in [2021, 2022]').reset_index(drop=True)

# Some values are counted twice due do renaming of old soviet / East bloc member states
spi_data = spi_data.sort_values(by=['polity'], na_position='first')
"""
	Nation	Year	polity	state_type	cpi	Science_score	Unesco_cumulative
479	Bosnia and Herzegovina	1990					0.0
1134	Czech Republic	1991					0.0
1135	Czech Republic	1992					1.0
1136	Czech Republic	1992					2.0
1133	Czech Republic	1990					0.0
1355	Eritrea	1990					0.0
1356	Eritrea	1991					0.0
3784	Slovakia	1990					0.0
3785	Slovakia	1991					0.0

"""
spi_data = spi_data.sort_values(by=['Nation', 'Year'])
spi_data = spi_data.bfill(limit=3)
# Count NaN values in 'polity' and 'cpi' columns grouped by 'Nation'
nan_counts_spi_data = spi_data.groupby('Nation')[['polity', 'Unesco_cumulative']].apply(lambda x: x.isna().sum())
"""
Nation	polity	Unesco_cumulative
Rwanda	0	27
Afghanistan	0	0
-> Fill in Ruandas Unesco counts with 0
"""
spi_data['Unesco_cumulative'] = spi_data['Unesco_cumulative'].fillna(0)
spi_data.to_csv(path_cleaning + "spi_data.csv", index=False) 
####
# 4. Import Country Similarity Index and rename -> append to bilateral final df
csi = pd.read_csv(path_cleaning + "/CSI/country-similarity-distance-matrix.csv")
# rename column
csi = csi.rename(columns={'Unnamed: 0': 'Countries'})
csi = csi.set_index('Countries')
# turn all elements to float
csi = csi.astype(float)
csi = csi.reset_index()
# Melt the DataFrame to long format
csi = csi.melt(id_vars='Countries', var_name='Country', value_name='Value')
csi = csi.rename(columns={'Value': 'CSI_Value', 'Countries':'Country_Origin', 'Country':'Country_Destination'})

# CENT AFR REP not found in regex
csi['Country_Origin'] = csi['Country_Origin'].str.replace('CENT AFR REP', 'Central African Republic', regex=False)
csi['Country_Destination'] = csi['Country_Destination'].str.replace('CENT AFR REP', 'Central African Republic', regex=False)

# Rename countries to harmonized names
csi["Country_Origin"] = coco.convert(names=csi["Country_Origin"], to='name_short')
csi["Country_Destination"] = coco.convert(names=csi["Country_Destination"], to='name_short')

########################################
# 4. Create bilateral country df from 1990 to 2020
########################################
df_nation = pd.DataFrame()
df_nation["Nation_Orig"] = spi_data["Nation"].unique()
# Generate all combinations of Nation-Nation pairs excluding combinations with the same nation
combinations_list = list(combinations(df_nation['Nation_Orig'], 2))
# Create a new DataFrame with the combinations
result_df = pd.DataFrame(combinations_list, columns=['Nation_Origin', 'Nation_Destination'])
# Add a new column for each year from 1990 to 2020
for year in range(1990, 2021):
    result_df[year] = None  # You can replace None with your actual data for each year

# Melt the DataFrame to convert it to long format
result_df_long = result_df.melt(id_vars=['Nation_Origin', 'Nation_Destination'], var_name='Year', value_name='Value')
result_df_long = result_df_long.drop("Value",axis=1)
# Convert 'Year' column in result_df_long to int64
result_df_long['Year'] = result_df_long['Year'].astype(int)
# Merge the spi_data DataFrame for the origin nation
merged_df_origin = pd.merge(result_df_long.copy(), spi_data, 
        left_on=['Nation_Origin', 'Year'], right_on=['Nation', 'Year'], 
        how='left', suffixes=('_origin', '_origin'))
# Drop the redundant 'Nation' column
merged_df_origin = merged_df_origin.drop(columns=['Nation'])
#merged_df_origin = merged_df_origin.add_suffix('_orig')

# Merge the spi_data DataFrame for the destination nation
merged_df_bilateral = pd.merge(merged_df_origin, spi_data, 
 left_on=['Nation_Destination', 'Year'], right_on=['Nation', 'Year'], 
 how='left', suffixes=('_origin', '_destination'))
# Drop the redundant 'Nation' column
merged_df_bilateral = merged_df_bilateral.drop(columns=['Nation'])
#merged_df_destination = merged_df_destination.add_suffix('_dest')

########################################
# 5. Import and combine International Student data
########################################
inter_students = pd.read_csv(path_cleaning + "/Education/interpolated_inter_students.csv")
inter_students = inter_students.drop(['Unnamed: 0'], axis=1)
inter_students = inter_students.rename(columns={"Value": "Int_Students",
                                                "Origin_Country":"Student_Origin",
                                                "Destination_Country":"Student_Destination"})
# Merge the DataFrames based on 'Student_Origin', 'Student_Destination', and 'Year'
merged_df_student = pd.merge(merged_df_bilateral, inter_students, 
                           left_on=['Nation_Origin', 'Nation_Destination', 'Year'], 
                           right_on=['Student_Origin', 'Student_Destination', 'Year'], 
                           how='left')

# Drop redundant columns from the second DataFrame
merged_df_student = merged_df_student.drop(columns=['Student_Origin', 'Student_Destination'])
merged_df_student['Int_Students'] = merged_df_student['Int_Students'].fillna(0)

########################################
# 5. Combine Country Similarity data
########################################
merged_df_csi = pd.merge(merged_df_student, csi, 
                           left_on=['Nation_Origin', 'Nation_Destination'], 
                           right_on=['Country_Origin', 'Country_Destination'], 
                           how='left')
# Drop redundant columns from the second DataFrame
merged_df_csi = merged_df_csi.drop(columns=['Country_Origin', 'Country_Destination'])
merged_df_csi.to_csv(path_cleaning + "spi_clean1.csv")



