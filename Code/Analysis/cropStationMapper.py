# -*- coding: utf-8 -*-
"""
////////// Geospatial Crop Data Weather Station Converter \\\\\\\\\\

This script processes geospatial agricultural data for specified states and years.
It performs the following tasks:

- Loads a mapping of weather stations with their geographical coordinates.
- Reads agricultural data from CSV files contained within zip archives for each specified state and year.
- Converts CSV data into geospatial data format (GeoDataFrame) using coordinates.
- Performs spatial joins to associate crop data points with the nearest daily weather stations.
- Groups the resulting data by daily weather station and crop type, then aggregates it for analysis.
- Saves the processed and grouped data into CSV files, one for each state and year, 
  containing detailed crop data integrated with weather station geospatial information.

@author: dforc
"""

import geopandas as gpd
import pandas as pd
import os
import zipfile
from tqdm import tqdm
import math

#######################################
# Constants and Settings
#######################################
states = ['Florida']
years = [str(year) for year in range(2010, 2021)]
script_dir = os.path.dirname(os.path.realpath(__file__))
station_mapping_filename = f'{states[0]}_Station_Mapping.csv'

# Load weather stations data
station_mapping_file = os.path.join(script_dir, station_mapping_filename)
station_mapping = pd.read_csv(station_mapping_file)

# Keep only the daily weather station data
station_mapping = station_mapping[['DailyStation', 'DailyLong', 'DailyLat']].drop_duplicates()
stations_gdf = gpd.GeoDataFrame(station_mapping, geometry=gpd.points_from_xy(station_mapping['DailyLong'], station_mapping['DailyLat']))
stations_gdf.crs = "EPSG:4326"

#######################################
# Function to calculate UTM zone
#######################################
def get_utm_zone(longitude):
    return math.floor((longitude + 180) / 6) + 1

def get_utm_crs(longitude):
    zone = get_utm_zone(longitude)
    return f"EPSG:326{zone:02d}"

#######################################
# Functions
#######################################
def load_and_convert_csv_to_gdf(zip_file_path, csv_file_name):
    with zipfile.ZipFile(zip_file_path, 'r') as z:
        with z.open(csv_file_name) as csv_file:
            df = pd.read_csv(csv_file)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df['Longitude'], df['Latitude']))
    gdf.crs = "EPSG:4326"
    return gdf

def perform_spatial_join(crop_gdf, weather_stations):
    median_long = weather_stations.geometry.x.median()
    projected_crs = get_utm_crs(median_long)
    
    crop_gdf = crop_gdf.to_crs(projected_crs)
    weather_stations = weather_stations.to_crs(projected_crs)
    
    joined_data = gpd.sjoin_nearest(crop_gdf, weather_stations, how="left", distance_col="distance")
    return joined_data[['geometry', 'DailyStation', 'CropTypes', 'Year', 'distance']]

def group_and_save_data(joined_data, output_path):
    grouping_columns = ['DailyStation', 'CropTypes', 'Year']
    grouped_data = joined_data.groupby(grouping_columns).size().reset_index(name='Count')
    grouped_data.to_csv(output_path, index=False)

#######################################
# Main Processing Loop
#######################################
for state in states:
    zip_file_path = os.path.join(script_dir, f'{state}Data.zip')
    for year in tqdm(years, desc=f'Processing {state}'):
        csv_file_name = f'{state}TopCropLonLat_{year}.csv'
        output_directory = os.path.join(script_dir, 'Output_CSVs', state)
        os.makedirs(output_directory, exist_ok=True)
        output_grouped_file_path = os.path.join(output_directory, f'{state}TopCropLonLat_{year}_GroupedByStation.csv')
        
        crop_gdf = load_and_convert_csv_to_gdf(zip_file_path, csv_file_name)
        joined_data = perform_spatial_join(crop_gdf, stations_gdf)
        group_and_save_data(joined_data, output_grouped_file_path)

print("All data processed successfully.")