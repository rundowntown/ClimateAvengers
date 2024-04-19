<a name="top"></a>
# Local Weather Impact Analysis on Crop Production

> ## Table of Contents
> - [Introduction](#introduction)
> - [Motivation](#motivation)
> - [Data](#data)
>   - [Raw Data Sources](#raw-data-sources)
>   - [State and Crop Selection](#state-and-crop-selection)
> - [Data Preparation and Preprocessing](#data-preparation-and-preprocessing)
>   - [Available Data](#available-data)
>   - [Scripts](#scripts)
>     - [Weather Data Preparation](#weather-data-preparation)
>     - [Crop Raster Data Preprocessing](#crop-raster-data-preprocessing)
> - [Usage](#usage)
>   - [Installation](#installation)
>   - [Analysis](#analysis)
> - [Credits](#credits)

## Introduction
This project aims to explore the impact of micro-climate conditions on crop production. By correlating regional climate conditions with crop yields across the United States, we aim to demonstrate a proof-of-concept modeling approach that can recommend crop production adjustments based on dynamic weather patterns.
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

## Motivation
Precision agriculture relies heavily on localized climate data to optimize crop output. Our research focuses on understanding how micro-climate affects crop yields and how data-driven insights can aid farmers in making informed decisions to enhance productivity and sustainability.
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

## Data

### Raw Data Sources
We utilize several datasets consisting of local weather data and crop yields, primarily sourced from:

- *USDA National Agricultural Statistics Service [Cropland Data Layer](https://croplandcros.scinet.usda.gov/)*
- *[Global Surface Summary of Day](https://www.ncei.noaa.gov/cdo-web/search) by NOAA*
- *National Climate Data Center (NCDC) [Storm Events Data](https://catalog.data.gov/dataset/ncdc-storm-events-database2)*
- *George Mason University’s [CropScape](https://nassgeodata.gmu.edu/CropScape/)*
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

### State and Crop Selection
**State selections (Florida, California)**: Based on crop and weather diversity.

**Crop selections:** Limited to 10 crops on the basis of crop frequency and contribution to local economies.
- *Florida selection criteria based on [crop economic value](https://farmingwork.com/blog/from-almonds-to-oranges-exploring-californias-top-10-crops/)*
- *California: selection criteria based on [crop economic value](https://www.fdacs.gov/Agriculture-Industry/Florida-Agriculture-Overview-and-Statistics)*

| Crop | California           | Florida      |
|------|----------------------|--------------|
| 1    | Rice                 | Corn         |
| 2    | Other Hay/Non Alfalfa| Potatoes     |
| 3    | Tomatoes             | Sugarcane    |
| 4    | Grapes               | Watermelons  |
| 5    | Almonds              | Tomatoes     |
| 6    | Walnuts              | Citrus       |
| 7    | Pistachios           | Oranges      |
| 8    | Oranges              | Peppers      |
| 9    | Strawberries         | Strawberries |
| 10   | Lettuce              | Blueberries  |

> **Data Discrepancies:**
> - *Florida 2015 (No Tomatoes)*
> - *Florida 2013 (No Peppers)*
> - *Florida 2012 (No Tomatoes)*
> - *Florida 2010 (No Watermelons, Peppers)*
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

## Data Preparation and Preprocessing

***(Users do not need to run these scripts, as the cleaned and preprocessed datasets are already available in the repository.)***

The `Code/Prep` repository contains scripts used for data cleaning and preprocessing, which were crucial in preparing the datasets used in our analyses. These scripts are included for transparency and for those interested in understanding or replicating our preprocessing steps.
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

### Available Data

The preprocessed datasets used for analysis are available in the `Data/` directory. These datasets have been cleaned, merged, and formatted for direct use in the analysis scripts provided in the `Code/Analysis` repository.

> Links to the raw datasets used for data preparation and preprocessing can be found in the `ExternalData.txt` file.
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

### Scripts

Although it is **not necessary to run these scripts** to use the preprocessed data, here is a brief description of what each script does and their respective output file locations:
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

#### Weather Data Preparation

- `normalsCountyConverter.py`
  -  **Description**: Converts raw 30-year normals data into a county-level summary, handling missing values and standardizing units.
     - ***Output***: `{myState}NormalsReady.csv`.

- `dailyRawCombiner.py`
  - **Description**: Combines GSOD NOAA data, which comes shipped in multiple
files, into a single .CSV for each State selected. User must set the State and Year Ranges of the files at the top of the script.
     - ***Output***: `{state}DailyRaw.csv`

- `dailyClimateBasicCleaner.py`
  - **Description**: Enhances the cleanliness and usability of daily climate data for a specified state. It focuses on normalizing data formats, decoding complex data fields into usable formats, and handling missing data with sophisticated data cleaning techniques.
     - ***Output***: `{myState}DailyCleaned.csv`

- `combinedDiagnosticImpute.py`
  - **Description**: Addresses missing data within a comprehensive weather dataset and includes advanced visualization to illustrate data patterns. It is designed to clean and impute missing values across various weather parameters such as temperature, wind speed, and more.
    - ***Output***: `Imputed_Combined_Daily_Normals.csv`
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

#### Crop Raster Data Preprocessing

- `TIFtoCSV.py`
  - **Description**: Converts geospatial raster data *(.tif files)* representing annual crop data for California and Florida into a more accessible CSV format. This conversion facilitates easier analysis and integration with other data types in the project.
    - ***Output***: `{state}TopCropLonLat_{year}.csv`

- `cropCountyShaper.py `
  - **Description**: Converts and integrates agricultural data from `TIFtoCSV_R.py` with geospatial county information. It processes annual crop data by associating crop data points with the corresponding county boundaries through spatial joins, and then groups and aggregates this data for further analysis.
    - ***Output***: `{state}TopCropLonLat_{year}_with_County_Grouped.csv`

- `cropCountyAllYearsCombine.py`
  - **Description**: Consolidate agricultural data from multiple years into a single dataset. It processes files generated by `cropCountyShaper.py`, which are specific to crop types and geographic data for counties within a state, and creates a comprehensive dataset that spans multiple years.
    - ***Output***: `{state}CropsCountyReady.csv`

> *Optional Scripts used for debugging and proof-of-concepts:*
> - `cropYearlyCSVAnalysis.r`
>    - **Description**: Filters out unwanted crop types, aggregates crop frequency data, selects the top 10 crops by acreage, and visualizes the data through density maps to verify the validity of longitude and latitude data.
>       - ***Output***: `{state}_top_crops_lonlat_{year}.csv` , `{state}_top_crops_freq_{year}.csv`
> - `TIFtoCSV_R.r`
>    - **Description**: Same as the analogous python script that goes by the same name. Memory issues necessitated the transition to Python for large raster files, like California and Florida.
>       - ***Output***: `{state}TopCropLatLon_{year}`

*These scripts are well-documented and can be explored to understand the data preparation pipeline more thoroughly.*
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

## Usage

### Installation
To set up this project locally, follow these steps:
1. Clone the repository:
``` console
git clone https://github.gatech.edu/MGT-6203-Spring-2024-Canvas/Team-95.git
```
2. Install required libraries:
``` console
pip install -r requirements.txt
```
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

### Analysis
Run the following scripts, found in the `Code/Analysis` directory, to analyse the preprocessed datasets found in the `Data/` directory:

#### 30 Year Weather Normals
- `EDA_Normals.Rmd`
  - **Description**:
    - **Output**:

#### Nearest Neighbor Mapping and Cardinal Temperatures


#### GIS

## Credits
+ *Daniel Forcade*
+ *Steven Wasserman*
+ *Ryan Hopkins*
+ *Soheil Sameti*
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>
