# Team-95 #
 *Team 95's group project GitHub repository for MGT 6203 (Canvas) Spring of 2024 semester.*

 ***Goal:** To use a geagraphic, crop, and weather data to recommend argricultural solutions to local/government farmers.*
---------------------------------------------------
## Data ##

### State and Crop Selection ###
 Vermont data originally used as testing case for data cleaning and transformation, then included for more diversity in
  weather patterns and crop frequencies of the selected states. Vermont crop selection based on a custom exclusion selection 
  criteria found in CropGeoDatAnalysis.r code.

 Vermont:

  1   - Corn

  5   - Soybeans

  68  - Apples

  21  - Barley

  27  - Rye

  229 - Pumpkins

  24  - Winter Wheat

  43  - Potatoes

  71  - Other Tree Crops

  222 - Squash



 State selection (Florida, California): Based on crop and weather diversity.

 Crop selections: Limited to 10 crops on the basis of crop frequency and contribution to local economies.

 Cali: https://farmingwork.com/blog/from-almonds-to-oranges-exploring-californias-top-10-crops/

  3   - Rice

  37  - Other Hay/Non Alfalfa

  54  - Tomatoes

  69  - Grapes

  75  - Almonds

  76  - Walnuts

  204 - Pistachios

  212 - Oranges

  221 - Strawberries

  227 - Lettuce



 Florida: https://www.fdacs.gov/Agriculture-Industry/Florida-Agriculture-Overview-and-Statistics

  1   - Corn

  43  - Potatoes

  45  - Sugarcane

  48  - Watermelons

  54  - Tomatoes

  72  - Citrus

  212 - Oranges

  216 - Peppers

  221 - Strawberries

  242 - Blueberries


 Note:

  Florida 2015 (No Tomatoes)

  Florida 2013 (No Peppers)

  Florida 2012 (No Tomatoes)

  Florida 2010 (No Watermelons, Peppers)


### Data Stored Elsewhere ###
 Our csv and tif files for California and Florida were too large to store on GitHub, thus we used OneDrive to store them.
  
  OneDrive Directory URL: https://gtvault-my.sharepoint.com/:f:/g/personal/rhopkins40_gatech_edu/Ekrxp3Qm-s5Opuhuu-Q-JiQBiq_C7tN1Mn_MDoxR2razFQ?e=0g6cbN


---------------------------------------------------
## Code ##

### Code Naming Redundancy Rationale ###
 There are two different TIFtoCSV scripts, one in R and the other in Python, due to memory allocation problems with
  the larger .tif files (California, Florida). R would run out of memory when processign the rasters, so we had to
  use a Python script that did the same thing.
