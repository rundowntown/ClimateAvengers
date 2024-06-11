
"""
////////// Crop Report Data Aggregation \\\\\\\\\

This Script Aggregates Crop Production Data from Multiple Years
(Data/Crop_Production_Data/Crop_Report_{Year}.csv)

It completes the following tasks:

- Reads crop production data files from 2010 to 2020,
      which include essential metadata such as crop types, production quantities, and locations.
- Standardizes the column names across different years.
- Concatenates all the data files into a single DataFrame for further analysis.
- Saves the aggregated DataFrame to a CSV file named Crop_Report_2010_2020.csv

- @Daniel
"""

import os
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

    ## Standardize column names
    df.columns = df.columns.str.replace('Yield.*', 'Yield', regex=True)
    df.columns = df.columns.str.replace('Price.*', 'Price P/U', regex=True)
    df.columns = df.columns.str.replace('Value.*', 'Value', regex=True)
    df.columns = df.columns.str.replace('Yield \(Unit/Acre\)', 'Yield', regex=True)
    df.columns = df.columns.str.replace('Price \(Dollars/Unit\)', 'Price P/U', regex=True)
    df.columns = df.columns.str.replace('Value \(Dollars\)', 'Value', regex=True)

    ## Convert data types
    numeric_cols = ['Year', 'Commodity Code', 'County Code', 'Harvested Acres', 'Yield', 'Production', 'Price P/U', 'Value']
    for col in numeric_cols:
        if col in df.columns:  ## Check if the column exists in the DataFrame
            df[col] = pd.to_numeric(df[col], errors='coerce')  ## Convert to numeric, make non-convertible values NaN
    
    ## Handle character columns
    char_cols = ['Crop Name', 'County', 'Unit']
    for col in char_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)  # Ensure these are treated as string data
    
    return df

# =============================================================================
## Read and Concatenate Crop Report Data Files
# =============================================================================
for year in range(2010, 2021):
    file_path = os.path.join(data_dir, f'Crop_Report_{year}.csv')
    if os.path.exists(file_path):
        yearly_data = pd.read_csv(file_path)
        yearly_data = standardize_columns(yearly_data)
        print(f"Column names for {year}: {list(yearly_data.columns)}")  # Add this line to check columns
        aggregated_data = pd.concat([aggregated_data, yearly_data], ignore_index=True)
    else:
        print(f"File not found: {file_path}")

# =============================================================================
## Save the Aggregated Data to a CSV File
# =============================================================================
aggregated_data.to_csv(output_file, index=False)
print(f"Aggregated data saved to {output_file}")


