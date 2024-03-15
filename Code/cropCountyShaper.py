# -*- coding: utf-8 -*-
"""
////////// Geospatial Crop Data County Converter \\\\\\\\\\

This script processes geospatial agricultural data for specified states and years.
It performs the following tasks:

- Reads and processes shapefiles for county boundaries to use in spatial analysis.
- Loads agricultural data from CSV files contained within zip archives for each specified state and year.
- Converts CSV data into geospatial data format (GeoDataFrame) using coordinates.
- Performs spatial joins to associate crop data points with corresponding counties.
- Groups the resulting data by county and crop type, then aggregates it for analysis.
- Saves the processed and grouped data into CSV files, one for each state and year, 
  containing detailed crop data integrated with county-level geospatial information.


@author: dforc
"""

import geopandas as gpd
import pandas as pd
import os
import zipfile
from tqdm import tqdm




#######################################
####### !! >> Set State Here << !!
#######################################
states = ['Florida']
years = [str(year) for year in range(2010, 2021)]  ## From 2010 to 2020
#######################################



#######################################
####### Load Shapefiles
#######################################
def load_and_process_shapefile(shapefile_path, columns_needed):
    """
    Load a county shapefile and select the required columns.

    Parameters:
    - shapefile_path: String, path to the shapefile.
    - columns_needed: List of strings, names of the columns to keep.

    Returns:
    - Geopandas GeoDataFrame with only the selected columns.
    """
    return gpd.read_file(shapefile_path)[columns_needed]
######################## End Function ########################





#######################################
####### Read .CSV from Zip; Convert to Geospatial
#######################################
def load_and_convert_csv_to_gdf(zip_file_path, csv_file_name, 
                                longitude_col='Longitude', latitude_col='Latitude'):
    """
    Load CSV data from within a zip file and convert it to a GeoDataFrame.

    Parameters:
    - zip_file_path: String, path to the zip file containing CSV data.
    - csv_file_name: String, name of the CSV file to process.
    - longitude_col: String, name of the column containing longitude data.
    - latitude_col: String, name of the column containing latitude data.

    Returns:
    - Geopandas GeoDataFrame with geometry created from longitude and latitude columns.
    """
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        with z.open(csv_file_name) as csv_file:
            df = pd.read_csv(csv_file)
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df[longitude_col],
                                                            df[latitude_col]))
######################## End Function ########################




#######################################
####### Spatial Join
#######################################
def perform_spatial_join(gdf, counties):
    """
    Perform a spatial join between GeoDataFrames of points and counties.

    Parameters:
    - gdf: Geopandas GeoDataFrame, points to join.
    - counties: Geopandas GeoDataFrame, county polygons to join against.

    Returns:
    - Geopandas GeoDataFrame after performing the spatial join, retaining specified columns.
    """
    gdf.crs = counties.crs
    joined_data = gpd.sjoin(gdf, counties, how="left", op='intersects')
    return joined_data[['geometry', 'STATEFP', 'COUNTYFP', 
                        'GEOID', 'NAME', 'ALAND', 'AWATER', 
                        'CropTypes', 'Year']]

######################## End Function ########################




#######################################
####### Group Data by County and Crop
#######################################
def group_and_save_data(joined_data, output_path, grouping_columns, count_column_name='Count'):
    """
    Group spatially joined data by specified columns and save to CSV.

    Parameters:
    - joined_data: Geopandas GeoDataFrame, data to group.
    - output_path: String, path to save the grouped data CSV.
    - grouping_columns: List of strings, columns to group by.
    - count_column_name: String, name of the count column in the output.

    Outputs:
    - CSV file saved to the specified path.
    """
    grouped_data = joined_data.groupby(grouping_columns).size().reset_index(name=count_column_name)
    grouped_data.to_csv(output_path, index=False)
######################## End Function ########################






#######################################
####### Run Program
#######################################

## Shapefile Location
shapefile_path = 'Shapefiles/tl_2019_us_county.shp'

## Variables of Interest in Shapefile
columns_needed = ['geometry', 'STATEFP', 'COUNTYFP', 
                  'GEOID', 'NAME', 'ALAND', 'AWATER']

## Process and Load Shapefile
counties = load_and_process_shapefile(shapefile_path, columns_needed)

## Process all States and Years Specified at Top of Script
for state in states:
    zip_file_path = f'{state}Data.zip'
    for year in tqdm(years, desc=f'Processing {state}'):
        csv_file_name = f'{state}TopCropLonLat_{year}.csv'
        
        ## Define and ensure the output directory exists
        output_directory = f'Output_CSVs/{state}'
        os.makedirs(output_directory, exist_ok=True)
        
        output_grouped_file_path = f'{output_directory}/{state}TopCropLonLat_{year}_with_County_Grouped.csv'

        if not zipfile.is_zipfile(zip_file_path):
            print(f"Zip file not found or is corrupted: {zip_file_path}")
            continue

        if csv_file_name not in zipfile.ZipFile(zip_file_path, 'r').namelist():
            print(f"File not found in zip: {csv_file_name}")
            continue

        ## Load and convert CSV data to GeoDataFrame
        gdf = load_and_convert_csv_to_gdf(zip_file_path, csv_file_name)

        ## Perform the spatial join
        joined_data = perform_spatial_join(gdf, counties)

        ## Rename the 'NAME' column to 'County' for clarity
        joined_data.rename(columns={'NAME': 'County'}, inplace=True)

        ## Define grouping columns for the grouped data
        grouping_columns = ['County', 'CropTypes', 'Year', 'STATEFP', 
                            'COUNTYFP', 'GEOID', 'ALAND', 'AWATER']

        ## Group by specified columns and save the result
        group_and_save_data(joined_data, output_grouped_file_path, grouping_columns)
        
######################## And We're Done  ########################