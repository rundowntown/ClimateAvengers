################################ Annual Crop Data TIF to CSV Coverter ##################################
# This script is written to convert state annual crop data tif files to csv. This script is relient
#  on your local machine's RAM. With 16GB of RAM, there were memory allocation issues with any state
#  larger than Vermont. To convert larger state tif files, use the analogous python script.

# Note:
#  - Crop Data is from https://nassgeodata.gmu.edu/CropScape/
#    Conversion: .222395 acres per pixel

# In the future:
#  - File paths are from Ryan's local file management.
#    Use "here" package to save and load files from root directory on github
########################################################################################################




#################################### Install necessary packages ########################################

install.packages(c("dplyr", "data.table", "raster"))
library(dplyr)
library(data.table)
library(raster)
memory.limit(size=NA) # Check the current memory limit
memory.limit(size=90000) # Attempt to increase the memory limit 

########################################################################################################




####################### Set most recent year of data, file, and path names #############################

data_year <- 2020
crop_datasets <- list("2020.tif", "2019.tif", "2018.tif", "2017.tif", "2016.tif", "2015.tif", 
                      "2014.tif", "2013.tif", "2012.tif", "2011.tif", "2010.tif")
# Create path to write csv files
output_directory <- "D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/"
# Raster file with correct CRS to map onto other raster objects
crs_raster <- raster("D:/Documents/GT/MGT 6203/Project/DataSets/Vermont_Corn_Freq_2008_2023.tif")
# Create lengend to apply to crop values
crop_codes <- data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/Legend.csv"))
crop_legend <- data.table(CropValue = crop_codes$Value, CropTypes = crop_codes$Category)

########################################################################################################




###################################### TIF to CSV Conversion ############################################

#For loop to automate reading and converting mutiple tif files
for (crop_data in crop_datasets) {

fileloc <- paste("D:/Documents/GT/MGT 6203/Project/DataSets/Vermont_", crop_data, sep = "")

# Read raster and assign correct CRS
raster_layer <- raster(fileloc)
crs(raster_layer) <- crs(crs_raster)
raster_layer_latlon <- projectRaster(raster_layer, crs = CRS("EPSG:4326"), method="ngb")

# Create a mask where 0 values are set to NA (Reduces memory allocation)
mask_raster <- raster_layer_latlon
values(mask_raster)[values(mask_raster) == 0] <- NA

# Apply the mask
raster_layer_latlon <- mask(raster_layer_latlon, mask_raster)

# Convert new lat/lon data to a table of points
dtPoints <- as.data.table(rasterToPoints(raster_layer_latlon))
colnames(dtPoints) <- c("Longitude", "Latitude", "CropValue")

# Use crop_legend to replace numeric values with crop names
dfMerged <- merge(dtPoints, crop_legend, by = "CropValue", all.x = TRUE)
dfMerged[, Year := data_year]

# Construct the name of the output CSV file
output_filename <- paste0("VermontTopCropLatLon_", data_year, ".csv")

# Create the full path for the .csv file
file_path <- file.path(output_directory, output_filename)
  
# Write the dataframe to a .csv file
fwrite(dfMerged, file_path, row.names = FALSE)

# Decrease year for naming purposes
 data_year <- data_year - 1
} 

########################################################################################################
