# -*- coding: utf-8 -*-
"""
////////// Crop Data County Integration Script \\\\\\\\\\

This Script Processes Agricultural Data Files produced by cropCountyShaper.py
(Output_CSVs/{state}/{state}TopCropLonLat_{year}_with_County_Grouped.csv)
It completes the following tasks:
 
- Reads multiple CSV files containing crop data for different years within a specified state
- Each file contains information on crop types, geographic coordinates, and other relevant data
- Combines these files into a single DataFrame to create a consolidated view of the data across years
- Saves the combined data in a structured CSV file named {state}CropsCountyReady.csv within the state-specific folder
- Ensures that all spatial and temporal data is aligned and correctly formatted for further analysis


@author: dforc
"""

import pandas as pd
import os

#######################################
####### !! >> Set State Here << !!
#######################################
STATE_OF_INTEREST = 'Florida'

## TODO: Set Dynamic 'State of interest' button on master script





#######################################
####### Combine Files
#######################################
def combine_csv_files(state, start_year, end_year, output_directory_base='Output_CSVs'):
    """
    Combine CSV files for the specified state and year range into a single DataFrame.
    Saves the combined data in the Output_CSVs/{state} directory with a specific filename.
    """
    ## File pattern to match the specific CSV files for the state and year
    file_pattern = f'{state}TopCropLonLat_{{}}_with_County_Grouped.csv'
    years = range(start_year, end_year + 1)

    dataframes = []
    output_directory = os.path.join(output_directory_base, state)

    ## Loop through each year, loading and appending the data to the dataframes list
    for year in years:
        file_path = os.path.join(output_directory, file_pattern.format(year))
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            dataframes.append(df)
            print(f'Successfully processed file: {file_path}')
        else:
            print(f'File not found: {file_path}')

    ## Check dataframes are there to be combined, if so, concatenate them
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        print('Successfully combined all dataframes.')
        return combined_df
    else:
        print('No dataframes to combine, returning empty dataframe.')
        return pd.DataFrame()
######################## End Function ########################






#######################################
####### Run Program
#######################################

## Combining CSV files for the specified state and year range
combined_df = combine_csv_files(STATE_OF_INTEREST, 2010, 2020)

## Define Path for Save Location
output_file_path = os.path.join('Output_CSVs', STATE_OF_INTEREST, f'{STATE_OF_INTEREST}CropsCountyReady.csv')

if not combined_df.empty:
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)  ## Ensure the output directory exists
    combined_df.to_csv(output_file_path, index=False)
    print(f'Combined data saved to {output_file_path}')
else:
    print('No combined data to save.')
    
    
    