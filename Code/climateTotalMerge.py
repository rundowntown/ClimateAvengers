# -*- coding: utf-8 -*-
"""
@author: dforc

This script integrates daily weather data with 30-year climate normals based on station mappings,
identifies potential data inconsistencies, and removes duplicate records to ensure data integrity.

The script performs the following steps:
1. Loads daily weather data, 30-year climate normals, and station mapping data from CSV files.
2. Converts station identifiers to strings to ensure consistent data types for merging.
3. Checks for and removes duplicate station mappings to avoid redundancy.
4. Converts the date in daily data to Month-Day format for matching with normals data.
5. Identifies and removes duplicate records in daily and normals data based on station IDs and dates.
6. Creates a composite key in normals data for unique identification.
7. Joins daily data with station mappings and maps daily weather stations to nearest normal stations.
8. Merges the daily data with the normals data using the composite keys to create a combined dataset.
9. Saves the combined data to a CSV file for further analysis.
10. Generates a map plot showing connections between daily weather stations and nearest normal stations.

"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


# =============================================================================
# Set paths to the datasets
# =============================================================================
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

daily_path = os.path.join(base_dir, "Data", 
                          "Daily_Weather_Data", "CaliforniaDailyCleaned.csv")

normals_path = os.path.join(base_dir, "Data", 
                            "30YearNormals_Data", "CaliforniaNormalsReady.csv")

mapping_path = os.path.join(base_dir, "Data", 
                            "Station_Mapping", "California_Station_Mapping.csv")

# =============================================================================
# Load the data
# =============================================================================
daily_data = pd.read_csv(daily_path)
normals_data = pd.read_csv(normals_path)
station_mapping = pd.read_csv(mapping_path)

# =============================================================================
# Data Cleaning and Preparation
# =============================================================================
## Convert station identifiers to string to ensure consistent data types for merging
daily_data['STATION'] = daily_data['STATION'].astype(str)
normals_data['STATION'] = normals_data['STATION'].astype(str)
station_mapping['DailyStation'] = station_mapping['DailyStation'].astype(str)
station_mapping['NormalStation'] = station_mapping['NormalStation'].astype(str)

## Check for and remove duplicate station mappings
if station_mapping.duplicated(subset=['DailyStation']).any():
    print("Warning: Duplicates found in station mappings. Removing duplicates.")
    station_mapping = station_mapping.drop_duplicates(subset=['DailyStation'])

## Convert date in daily data to Month-Day format for matching
daily_data['MonthDay'] = pd.to_datetime(daily_data['Date']).dt.strftime('%m-%d')

## Identify and remove duplicates in daily and normals data based on 'STATION' and 'DATE'
duplicates_daily = daily_data.duplicated(subset=['STATION', 'Date'])
if duplicates_daily.any():
    print(f"Warning: {duplicates_daily.sum()} duplicates found in daily data. Removing duplicates.")
    daily_data = daily_data.drop_duplicates(subset=['STATION', 'Date'])

duplicates_normals = normals_data.duplicated(subset=['STATION', 'DATE'])
if duplicates_normals.any():
    print(f"Warning: {duplicates_normals.sum()} duplicates found in normals data. Removing duplicates.")
    normals_data = normals_data.drop_duplicates(subset=['STATION', 'DATE'])

## Create a composite key in normals data for unique identification
normals_data['CompositeKey'] = normals_data['STATION'] + '-' + normals_data['DATE']
if normals_data.duplicated(subset=['CompositeKey']).any():
    print("Warning: Duplicates found in normals data composite keys. Removing duplicates.")
    normals_data = normals_data.drop_duplicates(subset=['CompositeKey'])

## Join daily data with station mappings
daily_data_mapped = pd.merge(daily_data, station_mapping, left_on='STATION', right_on='DailyStation', how='left')

## Check if any daily station maps to multiple normals stations
if daily_data_mapped.duplicated(subset=['STATION', 'MonthDay']).any():
    print("Warning: Daily data has multiple mappings to normals stations.")

## Create a matching composite key in the daily mapped data for final merging
daily_data_mapped['CompositeKey'] = daily_data_mapped['NormalStation'] + '-' + daily_data_mapped['MonthDay']

## Merge the daily data with the normals data using the composite keys
combined_data = pd.merge(daily_data_mapped, normals_data, on='CompositeKey', how='left', suffixes=('', '_norm'))

# =============================================================================
# Post-processing and Output
# =============================================================================
print(f"Original daily data count: {len(daily_data)}")
print(f"Combined data count: {len(combined_data)}")

## Save the combined data to CSV
output_path = os.path.join(base_dir, "Data", "Combined_Daily_Normals.csv")
combined_data.to_csv(output_path, index=False)


## Plot Station Mapping in Merged Dataframe to Check for Validity
def plot_station_connections(df):
    '''
    Plots connections between daily weather stations and nearest normal stations on a map.
    '''
    ## Group by 'DailyStation' and take the first occurrence
    unique_stations_df = df.groupby('DailyStation').agg('first').reset_index()

    ## Print diagnostic information
    print(f"Number of unique stations in the original dataframe: {df['DailyStation'].nunique()}")
    print(f"Number of rows after grouping: {len(unique_stations_df)}")

    fig, ax = plt.subplots(figsize=(10, 10))
    m = Basemap(projection='merc', llcrnrlat=31, urcrnrlat=42,
                llcrnrlon=-124, urcrnrlon=-114, resolution='i', ax=ax)
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    ## Initialize legend tracking
    plotted_daily = False
    plotted_normal = False

    ## Plot each pair of stations
    for _, row in unique_stations_df.iterrows():
        if pd.notnull(row['DailyLat']) and pd.notnull(row['DailyLong']) and pd.notnull(row['NormalLat']) and pd.notnull(row['NormalLong']):
            x, y = m(row['DailyLong'], row['DailyLat'])
            xn, yn = m(row['NormalLong'], row['NormalLat'])
            
            ## Plot Daily Station
            if not plotted_daily:
                m.plot(x, y, marker='o', color='blue', markersize=5, label='Daily Station')
                plotted_daily = True
            else:
                m.plot(x, y, marker='o', color='blue', markersize=5)
            
            ## Plot Normal Station
            if not plotted_normal:
                m.plot(xn, yn, marker='s', color='green', markersize=5, label='Normal Station')
                plotted_normal = True
            else:
                m.plot(xn, yn, marker='s', color='green', markersize=5)
            
            ## Connect with a line
            m.plot([x, xn], [y, yn], linestyle='-', color='red', linewidth=1, alpha=0.5)

    plt.title("Connections between Daily Weather Stations and Nearest Normal Stations")
    plt.legend(loc='lower left')
    plt.show()

## Generate Map Plot
plot_station_connections(combined_data)