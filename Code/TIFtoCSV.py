################################ Annual Crop Data TIF to CSV Coverter ##################################
# This script is written to convert state annual crop data for California and Florida tif files to csv.

# Note:
#  - Crop Data is from https://nassgeodata.gmu.edu/CropScape/
#    Conversion: .222395 acres per pixel

# In the future:
#  - File paths are from Ryan's local file management.
#    Use a python library to save and load files from root directory, instead of using local paths.
########################################################################################################

import rasterio
from rasterio.warp import calculate_default_transform, reproject, transform_bounds
from rasterio.enums import Resampling
import numpy as np
import pandas as pd
import os

# Set beginning year and state
data_year = 2020
state = "Florida"

# Set paths
crs_raster_path = f"D:/Documents/GT/MGT 6203/Project/DataSets/{state}_Corn_Freq_2008_2023.tif"
output_directory = f"D:/Documents/GT/MGT 6203/Project/DataSets/{state}CropData/"

while data_year >= 2010:

    # Set paths and CRS
    crop_data = f"{data_year}.tif"
    fileloc = f"D:/Documents/GT/MGT 6203/Project/DataSets/{state}_{crop_data}"
    dst_crs = 'EPSG:4326'

    # Open the reference raster to get its CRS
    with rasterio.open(crs_raster_path) as ref_raster:
        ref_crs = ref_raster.crs

    # Load the source raster for reprojection
    with rasterio.open(fileloc) as src:
        src_transform = src.transform
        src_crs = src.crs

        # Ensure the source raster has the same CRS as the reference raster before proceeding
        if src_crs != ref_crs:
            print("CRS mismatch detected. Adjusting source CRS to match reference CRS for further operations...")
            # Note: Adjusting CRS in code without reprojecting can lead to incorrect spatial references.
            # The right approach is to reproject if the CRS doesn't match, as done below.

        # Define the metadata for the reprojected raster
        kwargs = src.meta.copy()
        transform_4326, width_4326, height_4326 = calculate_default_transform(
            src_crs, dst_crs, src.width, src.height, *src.bounds)
        kwargs.update({
            'crs': dst_crs,
            'transform': transform_4326,
            'width': width_4326,
            'height': height_4326
        })

        # Create an empty array for the reprojected data
        dst_array = np.empty((height_4326, width_4326), dtype=src.meta['dtype'])

        # Reproject the raster to 'EPSG:4326'
        reproject(
            source=rasterio.band(src, 1),
            destination=dst_array,
            src_transform=src.transform,
            src_crs=src_crs,
            dst_transform=transform_4326,
            dst_crs=dst_crs,
            resampling=Resampling.nearest
        )

    # Process the reprojected data
    rows, cols = np.where(dst_array != 0)
    xs, ys = rasterio.transform.xy(transform_4326, rows, cols, offset='center')
    values = dst_array[rows, cols]

    # Create a DataFrame
    dtPoints = pd.DataFrame({'Longitude': xs, 'Latitude': ys, 'CropValue': values})

    # Load the crop legend and merge
    crop_legend = pd.read_csv("D:/Documents/GT/MGT 6203/Project/DataSets/Legend.csv")
    dfMerged = pd.merge(dtPoints, crop_legend.rename(columns={'Value': 'CropValue', 'Category': 'CropTypes'}), on='CropValue', how='left')
    dfMerged['Year'] = data_year

    # Drop the 'CropValue' column
    dfMerged.drop(columns=['CropValue'], inplace=True)

    # Save to CSV
    output_filename = f"{state}TopCropLonLat_{data_year}.csv"
    dfMerged.to_csv(os.path.join(output_directory, output_filename), index=False)

    # Iterate
    data_year -= 1
