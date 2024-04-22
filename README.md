<img src="https://brand.gatech.edu/sites/default/files/inline-images/extended-RGB.png" 
    width="700" 
    height="200" />

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
>  - [Installation](#installation)
>  - [Analysis / Model Building](#analysis-\-model-building)
>      - [30 Year Weather Normals Visualization](#30-year-weather-normals-visualization)
>      - [Nearest Neighbor Mapping and Cardinal Temperatures Scripts](#nearest-neighbor-mapping-and-cardinal-temperatures-scripts)
>      - [Crop Risk Index by Weather Station](#crop-risk-index-by-weather-station)
> - [ArcGIS Crop Suitability Analysis](#arcgis-crop-suitability-analysis)
>   - [Tools Used](#tools-used)
>   - [Methodology](#methodology)
>   - [Data Ranking](#data-ranking)
>   - [Weighted Overlay Analysis](#weighted-overlay-analysis)
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

- `dailyRawCombiner.py`
  - **Description**: Combines GSOD NOAA data, which comes shipped in multiple
files, into a single .CSV for each State selected. User must set the State and Year Ranges of the files at the top of the script.
     - ***Output***: `{state}DailyRaw.csv`

- `dailyClimateShaper.py`
  - **Description**: Processes daily climate data for a specified state, enhancing its usability for further analysis. It reads raw daily climate data, renames columns for clarity, selects essential data fields, replaces missing values with NaN, and maps weather stations to county boundaries using spatial data processing.
     - **Output**: `{state}DailyReady.csv` , `{state}StationsReady.csv`

- `dailyClimateBasicCleaner.py`
  - **Description**: Enhances the cleanliness and usability of daily climate data for a specified state. It focuses on normalizing data formats, decoding complex data fields into usable formats, and handling missing data with sophisticated data cleaning techniques.
     - ***Output***: `{myState}DailyCleaned.csv`

- `normalsCountyConverter.py`
  -  **Description**: Converts raw 30-year normals data into a county-level summary, handling missing values and standardizing units.
     - ***Output***: `{myState}NormalsReady.csv`.

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



## Installation
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


## Analysis / Model Building
Run the following scripts, found in the `Code/Analysis` directory, to analyse the preprocessed datasets found in the `Data/` directory:



### 30 Year Weather Normals Visualization

- `EDA_Normals.Rmd`
  - **Description**: This R script performs exploratory data analysis on 30-year climate normals for various counties in California and Florida. It processes data from CSV files, converts date columns, and visualizes temperature and precipitation progressions throughout the year.
    - **Input**: `30YearNormals_Data/CaliforniaNormalsReady.csv` , `30YearNormals_Data/FloridaNormalsReady.csv` , `Crop_Data/CaliforniaCropsCountyReady.csv`
    - **Output**: The script generates a series of plots visualizing average, maximum, and minimum temperature progressions, as well as precipitation and snowfall patterns through the year. These are visualized using different colors for various statistical measures such as average, standard deviation, and standard error. The final output includes a comprehensive PDF document containing all generated plots, titled '30 Year Normals For All of California'.


<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>


### Recommendation Systems Developed for Effective Crop Production

These scripts are dedicated to developing a recommendation system for effective crop production planning in California. The analysis is focused on assessing the production totals of various crops across different counties in California from 2010 to 2020. By using cardinal temperatures and precipitation conditions alongside a spatial analysis of decade-long weather patterns, these scripts aim to determine the most ideal counties for crop cultivation.

<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

#### Nearest Neighbor Mapping and Cardinal Temperatures Scripts

1. `nearestNeighborsStationMapping.py`
    - **Description**: This script maps daily weather stations to their nearest normal stations based on spatial data. It reads station data, processes geographical coordinates, and uses spatial joins to map each daily weather station with its nearest normal station. The script also visualizes these connections on a map, distinguishing daily and normal stations with different markers.
        - **Input**: `Daily_Weather_Data/{state}DailyCleaned.csv` , `30YearNormals_Data/{state}NormalsReady.csv`
        - **Output**: `{state}_Station_Mapping.csv`, which includes the mapped daily and normal weather stations with their respective coordinates and metadata.

2. `cropStationMapper.py`
    - **Description**: This script is designed to integrate geospatial agricultural data with weather station data. It loads weather station mappings, reads agricultural data from CSV files within zip archives, converts this data to geospatial format, and performs spatial joins to associate crop data with the nearest daily weather stations. The script aggregates this data by weather station and crop type for each specified state and year.
        - **Input**: `{state}_Station_Mapping.csv` from `nearestNeighborsStationMapping.py` , `{state}Data.zip` found in `Crop_Data/Raw_Datasets/` from `ExternalData.txt`.
        - **Output**: CSV files for each state and year, named `{state}TopCropLonLat_{year}_GroupedByStation.csv`, containing detailed crop data integrated with geospatial weather station information.

3. `climateTotalMerge.py`
    - **Description**: This script combines daily weather data with 30-year climate normals based on station mappings. It includes data cleaning steps such as type conversion, duplicate removal, and data merging. The script also generates a composite key for unique identification and merges datasets to create a comprehensive dataset that integrates daily weather data with long-term climate normals.
        - **Input**: `Daily_Weather_Data/{state}DailyCleaned.csv` , `30YearNormals_Data/{state}NormalsReady.csv`, `Station_Mapping/{state}_Station_Mapping.csv`
        - **Output**: A combined CSV file named `Combined_Daily_Normals.csv`, which contains the merged daily and normals data. Additionally, it generates a map plot illustrating the connections between daily weather stations and their nearest normal stations to validate the merging process, `Plots/Nearest_Neighbor_Stations_Mapping_Plot.png`.

#### Recommendation Model Script

4. `MGT-6203 Final Project Spatial Analysis.ipynb`
    - **Description**: Determines the current production totals of crops in each county of California, then recommends ideal counties for producing crops through use of cardinal temperatures/precipitation conditions and spatial analysis of 10-year and 30-year normals.
        - **Input**: `/Main_Data/Imputed_Combined_Daily_Normals.csv` , `/Crop_Data/CaliforniaCropsCountyReady.csv` , `/Crop_Data/CaliforniaCardinalData.csv`

#### Key Outputs:
- **Production Compatibility Analysis**: A detailed analysis comparing current crop production with optimal conditions to suggest potential improvements.
- **Data Visualizations**: Includes maps and charts that illustrate the relationships between daily weather stations and their nearest normal stations, providing visual insights into the spatial distribution of weather impacts on agriculture.
- **Recommendations for Crop Production**: Final recommendations for crop production adjustments per county to align better with the cardinal temperatures and historical climate data.

#### Next Steps
The section concludes with insights into the discrepancies between current and recommended crop production practices. Suggestions for further research include increasing data fidelity, incorporating soil composition, and annual pest invasion cycles to enhance agricultural outcomes.


<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>



### Crop Risk Index by Weather Station

These scripts are dedicated to constructing a Weather Risk Index for crops based on local data from weather stations. The index is designed to assist in agricultural planning by evaluating the risk posed by current weather conditions compared to ideal conditions for crop growth.

#### Crop Risk Index Script
- `Index_V3.Rmd `
  - **Description**:  A comprehensive index that integrates advanced statistical thresholds and risk assessments for agricultural crops based on weather data. It calculates deviation thresholds for temperature and other weather-related variables to determine risk levels, and incorporates detailed visualizations and a dynamic risk index assessment that considers both temperature extremities and cumulative risk factors.
    - **Input**: `Main_Data/Imputed_Combined_Daily_Normals.csv` , `Crop_Data/CaliforniaCropsStationReady.csv` , `Data/Crop_Data/CaliforniaCardinalData.csv`

#### Key Outputs
- **Risk Factors**: Generates detailed CSV reports outlining daily and accumulated risk factors for each crop and weather station.
- **Interactive Maps**: Provides dynamic maps that display risk levels across different regions, allowing stakeholders to visually assess areas of concern and plan interventions accordingly.
- **Dashboard**: A Shiny dashboard presents a user-friendly interface for exploring the risk data, with tools to select specific crops, regions, and time frames.


> ***`Index_1.Rmd` is not essential for building the Risk Index model.*** Rather, we include it here as a proof-of-concept script that many hours went into refining.
> - `Index_1.Rmd`
>   - **Description**: A proof-of-concept script for `Index_V3.Rmd`. `Index_1.Rmd` establishes a weather risk index for crops based on data from weather stations. It integrates daily weather data with crop-specific temperature thresholds to calculate risk scores that indicate potential impacts on crop health and productivity.
>     - **Input**: `Main_Data/Imputed_Combined_Daily_Normals.csv` , `Crop_Data/CaliforniaCropsStationReady.csv` , `Data/Crop_Data/CaliforniaCardinalData.csv`
>     - **Output**: Risk assessment summaries for each crop type and weather station, `indexRoughDraftDaily.csv`, and detailed visualization plots of the risk index and potential impacts on crops, .



<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>


## ArcGIS Crop Suitability Analysis


### Tools Used
- **ArcGIS**: For this project, we utilized the Weighted Overlay spatial analysis tool within ArcGIS to analyze and combine data layers effectively.
  - **Note**: ***ArcGIS is a licensed software suite that requires a paid subscription***. While we leveraged this tool to benefit from its robust capabilities in spatial analysis and unique modeling features, ***we do not intend for others to feel compelled to purchase this software***. We found it to be a valuable resource for gaining perspectives and insights into the data that we otherwise could not have achieved.
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>


### Methodology

The Suitability Analysis utilizes data from:
- `CaliforniaCropDataFromRasters.zip` datasets, found in the `ExternalData.txt` file.
    - **Description**: Ten years of crop production statistics across various counties. 
- `CaliforniaCardinalData.csv`, found in the `Data/Crop_Data/` directory.
    - **Description**: The total days that crops can be cultivated in each county.

The aim is to evaluate and rank each county based on two primary criteria:
1. **Annual Crop Production**: The total number of crops produced annually in each county.
2. **Cultivation Days**: The total days crops can be cultivated in each county, derived from the Cardinal Crop dataset.
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>


### Data Ranking
Each county is assigned two ranks:
- **Crop Count Rank**: Based on the annual crop production.
- **Cultivation Days Rank**: Based on the total days that crops can be cultivated as per the Cardinal Crop dataset.
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>


### Weighted Overlay Analysis
We employed the Weighted Overlay tool in ArcMap to integrate the rankings with respective weights for a comprehensive suitability analysis:
- **70% Weight on Crop Production**: Reflects the emphasis on the volume of crop output per county.
- **30% Weight on Cultivation Days**: Accounts for the climatic and temporal suitability for crop cultivation.

The analysis also incorporates additional factors such as proximity, land value, topology, and profitability, which are crucial for determining the overall agricultural viability of a county.

<div align="center">
  <img src="Visualizations/GIS_CropSuitability_California.png " alt="Logo" width="408" height="578">
</div>
<br>

> *`GIS_CropSuitability_California.png` can be found in the `Visualizations/` directory*

This suitability analysis is designed to highlight counties with optimal conditions for crop production based on a combination of quantitative production data and cultivation feasibility. The resulting weighted analysis aids stakeholders in making informed decisions regarding agricultural investments and operations.
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>

## Credits
+ *Daniel Forcade*
+ *Steven Wasserman*
+ *Ryan Hopkins*
+ *Soheil Sameti*
<div align="right" style="text-align: right;"><a href="#top">Back to Top</a></div>
