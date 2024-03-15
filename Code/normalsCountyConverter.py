# -*- coding: utf-8 -*-
"""
////////// Climate 30 Year Normals Processing \\\\\\\\\

This Script Takes in 30 Year Climate Normals 
(./Raw_Normal_Data/{state}NormalsRaw.csv)
It completes the following tasks:

- Reads raw climate normals data for a specified state
- Renames relevant columns for clarity and ease of use
- Selects a subset of columns, including date, temperature averages, 
      precipitation, snowfall, elevation, station, and geographic coordinates
- Replaces missing values indicated by -9999 with NaN to handle missing data
- Extracts unique weather station identifiers along with their coordinates
- Loads a county boundaries shapefile to map stations to their respective counties
- Performs a spatial join to associate weather stations with county and state information
- Outputs the processed data into clean CSV files, including station locations and climate normals

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
rawDataPath = f'./Raw_Normal_Data/{myState}NormalsRaw.csv'

## Read the CSV data into a DataFrame
myNormals = pd.read_csv(rawDataPath)




#######################################
####### Column Rename and Select
#######################################
## Rename columns of interest
rename_dict = {
    'DLY-TAVG-NORMAL': 'normalAvgTemp',
    'DLY-TAVG-STDDEV': 'normalAvgTempStd',
    'DLY-TMAX-NORMAL': 'normalMaxTemp',
    'DLY-TMAX-STDDEV': 'normalMaxTempStd',
    'DLY-TMIN-NORMAL': 'normalMinTemp',
    'DLY-TMIN-STDDEV': 'normalMinTempStd',
    'MTD-PRCP-NORMAL': 'normalMtdPrcp',
    'MTD-SNOW-NORMAL': 'normalMtdSnow',
    'LATITUDE': 'Lat',
    'LONGITUDE': 'Long'
    }

## Rename Columns
myNormals = myNormals.rename(columns=rename_dict)



## Select columns of interest and replace -9999 with NaN
columns_of_interest = ['DATE', 'normalAvgTemp', 'normalAvgTempStd', 
                       'normalMaxTemp', 'normalMaxTempStd', 
                       'normalMinTemp', 'normalMinTempStd', 
                       'normalMtdPrcp', 'normalMtdSnow', 
                       'ELEVATION', 'STATION',
                       'Long', 'Lat']


## Handle the missing columns case
normalSelect = myNormals[columns_of_interest].replace(-9999, np.nan)


## Extract UNIQUE STATIONS
uniqueStations = normalSelect[['STATION', 'Lat', 'Long']].drop_duplicates()

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
counties_sf = counties_sf.rename(columns={'NAME': 'COUNTY',
                                          'STATEFP': 'STATE_CODE'})

## Convert unique stations to a GeoDataFrame and perform a spatial join
stations_sf = gpd.GeoDataFrame(uniqueStations, 
                               geometry=gpd.points_from_xy(uniqueStations['Long'],
                                                           uniqueStations['Lat']), 
                               crs='EPSG:4326')


## Perform a spatial join between Stations and Map to Counties
counties_sf_transformed = counties_sf.to_crs(stations_sf.crs)
stations_with_county = gpd.sjoin(stations_sf, counties_sf_transformed,
                                 how="left")

## Prepare the stations data with county and state information
stations_with_county = stations_with_county[['STATION', 'COUNTY', 
                                             'STATE_CODE', 'Lat', 'Long']]

## /////////////////////////////////////






#######################################
####### Write Files
#######################################

## Construct the file paths for output
normalsOutputPath = f'./Clean_Normal_Data/{myState}NormalsReady.csv'
stationsOutputPath = f'./Clean_Normal_Data/{myState}StationsReady.csv'


## Merge Climate Normals with Spatial Data
myNormals_with_county = pd.merge(normalSelect, stations_with_county, on='STATION', 
                                 suffixes=('_x', '_y'))

## Drop the 'Lat_y' and 'Long_y' Columns (Dupes)
myNormals_with_county.drop(columns=['Lat_y', 'Long_y'], inplace=True)

## Rename Lat_x Long_x to Standard Latlong
myNormals_with_county.rename(columns={'Lat_x': 'Lat', 'Long_x': 'Long'}, inplace=True)



## Write the Processed 30 Year Normal Data to .CSV
myNormals_with_county.to_csv(normalsOutputPath, index=False)
stations_with_county.to_csv(stationsOutputPath, index=False)

