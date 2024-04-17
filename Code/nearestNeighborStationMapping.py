# -*- coding: utf-8 -*-
"""
////////// Daily to Normal Station Mapping + Visualization \\\\\\\\\

This Script Visualizes the Spatial Relationship Between Daily Weather Stations
and Their Nearest Normal Stations
(./Data/{state}_Station_Mapping.csv)

It completes the following tasks:

- Reads the spatial mapping between daily weather stations and their nearest normal stations,
      which includes coordinates and essential metadata such as station names and counties.
- Plots each daily weather station and its corresponding nearest normal station on a map,
      using distinct markers (daily stations as blue circles, normal stations as red squares).
- Produces a Station Mapping csv {State}_Station_Mapping.csv
"""

import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import FancyArrowPatch

# =============================================================================
## Set Working Directory From Absolute Path
# =============================================================================
absPath = os.path.abspath(__file__)          ## Absolute Path
dirPath = os.path.dirname(absPath)           ## Directory Path
os.chdir(dirPath)                            ## Set Directory

# =============================================================================
## Define Paths
# =============================================================================
state = 'California'
base_dir = os.path.dirname(os.getcwd())
data_dir = os.path.join(base_dir, 'Data')
weather_data_file = os.path.join(data_dir, 'Daily_Weather_Data', f'{state}DailyCleaned.csv')
normals_data_file = os.path.join(data_dir, '30YearNormals_Data', f'{state}NormalsReady.csv')

# =============================================================================
## Load the Data
# =============================================================================
weather_data = pd.read_csv(weather_data_file)
normals_data = pd.read_csv(normals_data_file)

# =============================================================================
## Extract Unique Station Locations for Both Datasets
# =============================================================================
unique_weather_stations = weather_data[['STATION', 'Long', 'Lat', 
                                        'COUNTY', 'StationName']].drop_duplicates().reset_index(drop=True)

unique_normals_stations = normals_data[['STATION', 'Long', 
                                        'Lat', 'COUNTY']].drop_duplicates().reset_index(drop=True)

# =============================================================================
## Convert DataFrame to GeoDataFrame for Weather Stations
# =============================================================================
unique_weather_stations['geometry'] = [Point(xy) for xy in zip(unique_weather_stations['Long'], 
                                                               unique_weather_stations['Lat'])]

gdf_weather_stations = gpd.GeoDataFrame(unique_weather_stations,
                                        geometry='geometry')

gdf_weather_stations.set_crs(epsg=4326, inplace=True)
gdf_weather_stations.to_crs(epsg=32610, inplace=True)  # Reproject to UTM

# =============================================================================
## Convert DataFrame to GeoDataFrame for Normals Stations
# =============================================================================
unique_normals_stations['geometry'] = [Point(xy) for xy in zip(unique_normals_stations['Long'],
                                                               unique_normals_stations['Lat'])]

gdf_normals_stations = gpd.GeoDataFrame(unique_normals_stations, 
                                        geometry='geometry')

gdf_normals_stations.set_crs(epsg=4326, inplace=True)
gdf_normals_stations.to_crs(epsg=32610, inplace=True)  # Reproject to UTM

# =============================================================================
## Perform Spatial Join - This Joins Each Unique Weather Station to the Nearest Normal Station
# =============================================================================
nearest_normals_mapping = gpd.sjoin_nearest(gdf_weather_stations,
                                            gdf_normals_stations, 
                                            how="left", 
                                            distance_col="distance")

nearest_normals_mapping = nearest_normals_mapping[['STATION_left', 'Long_left', 
                                                   'Lat_left', 'COUNTY_left', 
                                                   'StationName', 'STATION_right',
                                                   'Long_right', 'Lat_right',
                                                   'COUNTY_right']].rename(
    columns={'STATION_left': 'DailyStation', 
             'Long_left': 'DailyLong', 
             'Lat_left': 'DailyLat',
             'COUNTY_left': 'DailyCounty', 
             'StationName': 'DailyStationName', 
             'STATION_right': 'NormalStation', 
             'Long_right': 'NormalLong', 
             'Lat_right': 'NormalLat', 
             'COUNTY_right': 'NormalCounty'})

# =============================================================================
## Save the Mapping
# =============================================================================
mapping_output_file = os.path.join(data_dir, 'Station_Mapping', f'{state}_Station_Mapping.csv')
nearest_normals_mapping.to_csv(mapping_output_file, index=False)
print("Station mapping complete. Output saved to:", mapping_output_file)

# =============================================================================
## Function to Plot Connections Between Stations on a Map
# =============================================================================
def plot_station_connections(df):
    '''
    --> This function plots connections between daily weather stations and nearest normal stations on a map
    <-- Plots map with station connections
    '''
    fig, ax = plt.subplots(figsize=(10, 10))
    m = Basemap(projection='merc', llcrnrlat=31, urcrnrlat=42,
                llcrnrlon=-124, urcrnrlon=-114, resolution='i', ax=ax)
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()

    ## Plot each pair of stations
    for _, row in df.iterrows():
        x, y = m(row['DailyLong'], row['DailyLat'])
        xn, yn = m(row['NormalLong'], row['NormalLat'])
        
        ## Plot Daily Station
        m.plot(x, y, marker='o',
               color='blue', 
               markersize=5, 
               label='Daily Station' if 'Daily Station' not in ax.get_legend_handles_labels()[1] else "")
        
        ## Plot Normal Station
        m.plot(xn, yn, marker='s', 
               color='green', 
               markersize=5, 
               label='Normal Station' if 'Normal Station' not in ax.get_legend_handles_labels()[1] else "")
        
        ## Connect with a line
        m.plot([x, xn], [y, yn], linestyle='-',
               color='red', 
               linewidth=1,
               alpha=0.9)

    plt.title("Connections between Daily Weather Stations and Nearest Normal Stations")
    plt.legend()
    plt.show()

# Optionally plot the connections
plot_station_connections(nearest_normals_mapping)
