# -*- coding: utf-8 -*-
"""
////////// Weather Data Imputation and Visualization \\\\\\\\\

This script manages the cleaning and imputation of missing weather data for multiple stations
from the dataset (./Data/Combined_Daily_Normals.csv).

Key tasks:
- Visualizes missing data patterns using matrix and heatmap plots.
- Implements rolling mean imputation for temperature, wind speed, and other variables.
- Generates comprehensive visual comparisons of data distributions before and after imputation.
- Saves the cleaned and imputed dataset.
"""


import os
import pandas as pd
import missingno as msno
import matplotlib.pyplot as plt
import seaborn as sns


# =============================================================================
# Set paths to the datasets
# =============================================================================

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data_path = os.path.join(base_dir, "Data",
                         "Main_Data", "Combined_Daily_Normals.csv")

output_path = os.path.join(base_dir, "Data",
                           "Main_Data", "Imputed_Combined_Daily_Normals.csv")

## Load Data
df = pd.read_csv(data_path)

# =============================================================================
# View Missing Data
# =============================================================================
## Matrix plot to visualize missing data
msno.matrix(df)

## Heatmap to show correlations of missingness between columns
msno.heatmap(df)


# =============================================================================
# Check Stations Individually
# =============================================================================

# Get a list of unique stations
unique_stations = df['DailyStationName'].unique()

# Loop through each station and generate a matrix plot with a title
for station in unique_stations[:10]:  # Limit to first 10 for demonstration
    station_data = df[df['DailyStationName'] == station]
    plt.figure(figsize=(12, 6))
    msno.matrix(station_data)
    plt.title(f'Missing Data Matrix for {station}')  # Setting the title using matplotlib
    plt.show()  # This line ensures that the plot shows up in most environments
    
# =============================================================================
# Drop Extra Columns
# =============================================================================   
    
columns_to_drop = ['STATION', 'StationName', 'Long',
                   'Lat', 'COUNTY', 'STATION_norm', 
                   'Long_norm', 'Lat_norm', 'COUNTY_norm',
                   'DATE', 'WindGust']

df = df.drop(columns=columns_to_drop)

## View Missing Matrix after Cols Removed
msno.matrix(df)


# =============================================================================
# Impute Missing Values
# ============================================================================= 
## Implement a 6 Day Rolling Average Imputation

## Sort data by Station and Date
df = df.sort_values(by=['DailyStation', 'Date'])

## Function for Rolling Average
def rolling_mean_impute(series):
    return series.fillna(series.rolling(window=6, min_periods=1, center=True).mean())

## Apply imputation and mark the imputations
columns_to_impute = ['MaxTemp', 'MinTemp', 'MaxWindSpeed', 
                     'WindSpeed', 'Precipitation', 'DewPoint']

## Impute All Columns
for column in columns_to_impute:
    df[f'{column}_imputed'] = df.groupby('DailyStation')[column].transform(rolling_mean_impute)



# =============================================================================
# Visual Imputation Analysis
# ============================================================================= 
## Create plots for the entire dataset to compare original and imputed data
fig, axes = plt.subplots(len(columns_to_impute), 4, figsize=(20, len(columns_to_impute) * 5))

for i, column in enumerate(columns_to_impute):
    ## Before Imputation Line Plot
    axes[i, 0].plot(df['Date'], df[column], label='Original', alpha=0.7, marker='o', linestyle='-')
    axes[i, 0].set_title(f'Original {column}')
    axes[i, 0].set_ylabel(column)
    
    ## After Imputation Line Plot
    axes[i, 1].plot(df['Date'], df[f'{column}_imputed'], label='Imputed', color='orange', marker='o', linestyle='-')
    imputed_points = df['Date'][df[column].isna()]
    imputed_values = df[f'{column}_imputed'][df[column].isna()]
    axes[i, 1].scatter(imputed_points, imputed_values, color='red', label='Imputed Values', zorder=5)
    axes[i, 1].set_title(f'Imputed {column}')
    
    ## Before Imputation Histogram and Boxplot
    sns.histplot(df[column].dropna(), kde=True, ax=axes[i, 2])
    sns.boxplot(x=df[column], ax=axes[i, 3])
    axes[i, 2].set_title(f'Before Imputation Histogram: {column}')
    axes[i, 3].set_title(f'Before Imputation Boxplot: {column}')
    
    ## After Imputation Histogram and Boxplot
    sns.histplot(df[f'{column}_imputed'], kde=True, ax=axes[i, 2], color="orange")
    sns.boxplot(x=df[f'{column}_imputed'], ax=axes[i, 3], color="orange")
    axes[i, 2].set_title(f'After Imputation Histogram: {column}')
    axes[i, 3].set_title(f'After Imputation Boxplot: {column}')

axes[0, 0].legend()
axes[0, 1].legend()

plt.tight_layout()
plt.show()


## Check Post Imputation Missing Matrix
msno.matrix(df)


# =============================================================================
# Add Imputed Values to NAs and Drop _isImputed Columns
# ============================================================================= 
for column in columns_to_impute:
    df[column] = df[f'{column}_imputed']
    df.drop(columns=f'{column}_imputed', inplace=True)  ## Removes is_imputed Cols

## Write to CSV
df.to_csv(output_path, index=False)
