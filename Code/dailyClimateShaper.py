# -*- coding: utf-8 -*-
"""
////////// Daily Climate Data Processing \\\\\\\\\

This script is run after dailyRawCombiner.py, and before
dailyClimateBasicCleaner.py
    
This Script Processes Daily Climate Data
(./Raw_Daily_Data/{state}DailyRaw.csv)
It completes the following tasks:

- Reads raw daily climate data for a specified state
- Renames relevant columns for clarity and ease of use
- Selects a subset of columns, including date, temperature, precipitation, wind speed, 
  dew point, weather conditions, elevation, station, and geographic coordinates
- Replaces missing values indicated by -9999 with NaN to handle missing data
- Extracts unique weather station identifiers along with their coordinates
- Loads county boundaries shapefile to map stations to their respective counties
- Performs a spatial join to associate weather stations with county and state information
- Outputs the processed data into clean CSV files, including station locations and daily climate data

@author: dforc
"""

import pandas as pd
import geopandas as gpd
import numpy as np

#######################################
####### !! >> Set State Here << !!
#######################################
myState = "Florida"




## Dynamically construct the file paths for raw data
rawDataPath = f'./Raw_Daily_Data/{myState}DailyRaw.csv'

## Read the CSV data into a DataFrame
dailyData = pd.read_csv(rawDataPath)



#######################################
####### Column Rename and Select
#######################################
## Rename columns of interest
rename_dict = {
    'LATITUDE': 'Lat',
    'LONGITUDE': 'Long',
    'ELEVATION': 'Elevation',
    'DATE': 'Date',
    'DEWP': 'DewPoint',
    'FRSHTT': 'WeatherType',
    'GUST': 'WindGust',
    'MAX': 'MaxTemp',
    'MIN': 'MinTemp',
    'MXSPD': 'MaxWindSpeed',
    'PRCP': 'Precipitation',
    'TEMP': 'AvgTemp',
    'WDSP': 'WindSpeed'
}


## Rename Columns
dailyData = dailyData.rename(columns=rename_dict)

## Select columns of interest and replace -9999 with NaN
columns_of_interest = ['Date', 'DewPoint', 'WeatherType', 
                       'WindGust', 'MaxTemp', 'MinTemp',
                       'MaxWindSpeed', 'Precipitation', 
                       'AvgTemp', 'WindSpeed',
                       'Elevation', 'STATION', 
                       'Long', 'Lat']


dailySelect = dailyData[columns_of_interest].replace(-9999, np.nan)


## Extract UNIQUE STATIONS
uniqueStations = dailySelect[['STATION', 'Lat', 'Long']].drop_duplicates()

## /////////////////////////////////////





#######################################
####### Shapefile Processing and Mapping
#######################################

## Load county boundaries shapefile
shapeFilePath = "./Shape_Files/tl_2019_us_county.shp"
counties_sf = gpd.read_file(shapeFilePath)

## Select the necessary columns and rename for clarity
counties_sf = counties_sf[['geometry', 'STATEFP', 'COUNTYFP', 
                           'GEOID', 'NAME', 'ALAND', 'AWATER']]

## Rename Columns of Interest
counties_sf = counties_sf.rename(columns={'NAME': 'COUNTY', 'STATEFP': 'STATE_CODE'})

## Convert unique stations to a GeoDataFrame and perform a spatial join
stations_sf = gpd.GeoDataFrame(uniqueStations, 
                               geometry=gpd.points_from_xy(uniqueStations['Long'], uniqueStations['Lat']), 
                               crs='EPSG:4326')

## Perform a spatial join between Stations and Map to Counties
counties_sf_transformed = counties_sf.to_crs(stations_sf.crs)
stations_with_county = gpd.sjoin(stations_sf, counties_sf_transformed, how="left")

## Prepare the stations data with county and state information
stations_with_county = stations_with_county[['STATION', 'COUNTY', 'STATE_CODE', 'Lat', 'Long']]

## /////////////////////////////////////




#######################################
####### Write Files
#######################################

## Construct the file paths for output
dailyOutputPath = f'./Clean_Daily_Data/{myState}DailyReady.csv'
stationsOutputPath = f'./Clean_Daily_Data/{myState}StationsReady.csv'

## Merge Daily Data with Spatial Data
dailyData_with_county = pd.merge(dailySelect, stations_with_county, on='STATION', 
                                 suffixes=('_x', '_y'))

## Drop the 'Lat_y' and 'Long_y' Columns (Dupes)
dailyData_with_county.drop(columns=['Lat_y', 'Long_y'], inplace=True)

## Rename Lat_x Long_x to Standard Lat/Long
dailyData_with_county.rename(columns={'Lat_x': 'Lat', 'Long_x': 'Long'}, inplace=True)

## Write the Processed Daily Data to .CSV
dailyData_with_county.to_csv(dailyOutputPath, index=False)
stations_with_county.to_csv(stationsOutputPath, index=False)

