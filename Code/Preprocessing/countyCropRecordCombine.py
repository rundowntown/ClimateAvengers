
"""
////////// Crop Report Data Aggregation \\\\\\\\\

This Script Aggregates Crop Production Data from Multiple Years
(Data/Crop_Production_Data/Crop_Report_{Year}.csv)

It completes the following tasks:

- Reads crop production data files from 2010 to 2020,
      which include essential metadata such as crop types, production quantities, and locations.
- Standardizes the column names across different years.
- Converts whitespace Column names to Snake Case
- Concatenates all the data files into a single DataFrame for further analysis.
- Saves the aggregated DataFrame to a CSV file named Crop_Report_2010_2020.csv

- @Daniel
"""

import os
import re
import pandas as pd

# =============================================================================
## Set Working Directory From Absolute Path
# =============================================================================
absPath = os.path.abspath(__file__)          ## Absolute Path
dirPath = os.path.dirname(absPath)           ## Directory Path
os.chdir(dirPath)                            ## Set Directory

# =============================================================================
## Define Paths
# =============================================================================
base_dir = os.path.dirname(os.path.dirname(os.getcwd()))  ## Move up two levels to WeatherProject
data_dir = os.path.join(base_dir, 'Data', 'Crop_Production_Data')
output_file = os.path.join(data_dir, 'Crop_Report_2010_2020.csv')

# =============================================================================
## Initialize an Empty DataFrame to Store Aggregated Data
# =============================================================================
aggregated_data = pd.DataFrame()

# =============================================================================
## Function to Standardize Column Names
# =============================================================================
def standardize_columns(df):
    ## Remove leading and trailing spaces from column names
    df.columns = df.columns.str.strip()

    ## Replace spaces with underscores to follow variable naming conventions
    df.columns = df.columns.str.replace(' ', '_', regex=True)

    ## Apply further standardization for specific cases
    df.columns = df.columns.str.replace('Yield.*', 'Yield', regex=True)
    df.columns = df.columns.str.replace('Price.*', 'Price_Per_Unit', regex=True)
    df.columns = df.columns.str.replace('Value.*', 'Value', regex=True)
    df.columns = df.columns.str.replace('Yield_\(Unit/Acre\)', 'Yield', regex=True)
    df.columns = df.columns.str.replace('Price_\(Dollars/Unit\)', 'Price_Per_Unit', regex=True)
    df.columns = df.columns.str.replace('Value_\(Dollars\)', 'Value', regex=True)

    ## Convert data types
    numeric_cols = ['Year', 'Commodity_Code', 'County_Code', 
                    'Harvested_Acres', 'Yield', 'Production', 
                    'Price_Per_Unit', 'Value']
    
    for col in numeric_cols:
        if col in df.columns:  ## Check if the column exists in the DataFrame
            ## Convert to numeric, make non-convertible values NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    ## Handle character columns
    char_cols = ['Crop_Name', 'County', 'Unit']
    for col in char_cols:
        if col in df.columns:
            ## Ensure these are treated as string data
            df[col] = df[col].astype(str)  
    
    return df

# =============================================================================
## Read and Concatenate Crop Report Data Files
# =============================================================================
for year in range(2010, 2021):
    file_path = os.path.join(data_dir, f'Crop_Report_{year}.csv')
    if os.path.exists(file_path):
        yearly_data = pd.read_csv(file_path)
        yearly_data = standardize_columns(yearly_data)
        ## Check Column Names are Consistent
        print(f"Column names for {year}: {list(yearly_data.columns)}")
        aggregated_data = pd.concat([aggregated_data, yearly_data], ignore_index=True)
    else:
        print(f"File not found: {file_path}")
        
        
# =============================================================================
## Fix misspellings in the County column
# =============================================================================
## Use regex to catch variations of "San Luis Obisp" to "San Luis Obispo
aggregated_data['County'] = aggregated_data['County'].replace(to_replace=r'^San Luis Obis[p|bo]?.*$',
                                                              value='San Luis Obispo', regex=True)

# =============================================================================
## Save the Aggregated Data to a CSV File
# =============================================================================
aggregated_data.to_csv(output_file, index=False)
print(f"Aggregated data saved to {output_file}")



crops = ["HAY", "RICE", "TOMATO", 
         "GRAPE", "ALMOND", "WALNUT",
         "PISTACH", "ORANGE", "STRAWB", 
         "LETTUCE"]


# Joining the list into a regex pattern that matches any of the crops
regex_pattern = '|'.join(crops)




# Filter the DataFrame for rows where the Crop_Name contains any of the specified crops
filtered_data = aggregated_data[aggregated_data['Crop_Name'].str.contains(regex_pattern, case=False, na=False)]

# Display or process your filtered data
print(filtered_data)

# Optionally, save the filtered data to a new CSV file
filtered_output_file = os.path.join(data_dir, 'Filtered_Crop_Report_2010_2020.csv')
filtered_data.to_csv(filtered_output_file, index=False)
print(f"Filtered data saved to {filtered_output_file}")


