# -*- coding: utf-8 -*-
"""
////////// Daily Climate Data Cleaning \\\\\\\\\

This Script Cleans the Daily Climate Data
(./Clean_Daily_Data/{state}DailyReady.csv)

It completes the following tasks:

- Reads the cleaned daily climate data for a specified state
- Replaces placeholder values in columns like DewPoint, MaxTemp, MinTemp,
      WindGust, MaxWindSpeed, WindSpeed, and Precipitation with NaN
- Ensures the 'Date' column is in the proper datetime format
- Decodes the WeatherType column into separate indicators for weather conditions
      such as Fog, Rain_Drizzle, Snow_Ice, Hail, Thunder, and Tornado_Funnel
- Outputs the further cleaned data into new CSV files (./Clean_Daily_Data/{state}DailyCleaned.csv)
- Fills Missing Values with NA

@author: dforc
"""

import pandas as pd
import numpy as np

#######################################
####### !! >> Set State Here << !!
#######################################
myState = "California"

## Set Dynamic Path
cleanDataPath = f'./Clean_Daily_Data/{myState}DailyReady.csv'

## Read the CSV into Dataframe
dailyCleanedData = pd.read_csv(cleanDataPath)




#######################################
####### Data Cleaning
#######################################


## Handle Missing Value Indicators
missing_value_indicators = {
    'DewPoint': 9999.9,
    'MaxTemp': 9999.9,
    'MinTemp': 9999.9,
    'WindGust': 999.9,
    'MaxWindSpeed': 999.9,
    'WindSpeed': 999.9,
    'Precipitation': 99.99  # Added Precipitation column filter
}

for column, placeholder in missing_value_indicators.items():
    dailyCleanedData[column].replace(placeholder, np.nan, inplace=True)

## Ensure 'Date' is in the datetime format
dailyCleanedData['Date'] = pd.to_datetime(dailyCleanedData['Date'], format='%Y-%m-%d')

## Decode WeatherType column into separate indicators
weather_conditions = ['Fog', 'Rain_Drizzle', 'Snow_Ice', 'Hail', 'Thunder', 'Tornado_Funnel']
for i, condition in enumerate(weather_conditions):
    dailyCleanedData[condition] = dailyCleanedData['WeatherType'].apply(lambda x: int(str(x).zfill(6)[i]) if pd.notnull(x) else np.nan)



## Remove the original 'WeatherType' column as it's no longer needed
dailyCleanedData.drop('WeatherType', axis=1, inplace=True)


## Fill in all missing values with NA
dailyCleanedData.fillna('NA', inplace=True)

## /////////////////////////////////////




#######################################
####### Write Cleaned Data
#######################################

## Construct the file path for output
cleanedOutputPath = f'./Clean_Daily_Data/{myState}DailyCleaned.csv'

## Write the cleaned data to .CSV
dailyCleanedData.to_csv(cleanedOutputPath, index=False)

print(f"Data cleaned and saved to {cleanedOutputPath}")


## /////////////////////////////////////




