# -*- coding: utf-8 -*-
"""
This Script Combines the California Daily Temp Files
NOAA Global Summaries of the Day
Source: https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C00516
@author: dforc
"""

import pandas as pd
import os

#######################################
####### !! >> Set State Here << !!
#######################################
states = ['Florida']

#######################################
####### !! >> Define Year Ranges of Files << !!
#######################################
year_ranges = ['2010-2014', '2015-2018', '2019-2020']  ## Update or add ranges as needed


#######################################
## Combine Segemented Raw Years into Single .CSV
#######################################

## Loop through each state
for state in states:
    ## Initialize an empty list to store DataFrames for the current state
    dataframes = []

    ## Loop through each year range
    for year_range in year_ranges:
        ## Generate the file name based on the state and year range
        file_name = f'{state}DailyRaw{year_range}.csv'
        
        ## Check if the file exists before reading
        if os.path.exists(file_name):
            ## Read the CSV file into a DataFrame
            df = pd.read_csv(file_name)
            
            ## Append the DataFrame to the list
            dataframes.append(df)
        else:
            ## Print a message if the file is not found
            print(f'File not found: {file_name}')

    ## Combine all DataFrames for the current state into a single DataFrame
    combined_df = pd.concat(dataframes, ignore_index=True)

    ## Write the combined DataFrame for the current state to a new CSV file
    output_file_name = f'{state}DailyRaw.csv'  ## Generate output file name based on the state
    combined_df.to_csv(output_file_name, index=False)