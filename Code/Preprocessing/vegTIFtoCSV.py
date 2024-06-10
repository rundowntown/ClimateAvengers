# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 16:26:17 2024

@author: dforc
"""

import rasterio
from rasterio.warp import calculate_default_transform, reproject
from rasterio.enums import Resampling
import numpy as np
import pandas as pd
import os

# Define the base directory based on the current script location
base_directory = os.path.dirname(__file__)

# Define paths and constants
data_year = 2011
state = "California"
fileloc = os.path.join(base_directory, f"{state}_ndvi_week1_{data_year}.tif")
output_directory = os.path.join(base_directory, f"{state}NDVIData/")
dst_crs = 'EPSG:4326'

# Check if output directory exists, if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Open the NDVI raster
with rasterio.open(fileloc) as src:
    src_transform = src.transform
    src_crs = src.crs

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
        src_crs=src.crs,
        dst_transform=transform_4326,
        dst_crs=dst_crs,
        resampling=Resampling.nearest
    )

# Process the reprojected data to exclude non-vegetative or unclear data (typically NDVI < 0)
rows, cols = np.where(dst_array >= 0)  # Adjust threshold as needed
xs, ys = rasterio.transform.xy(transform_4326, rows, cols, offset='center')
values = dst_array[rows, cols]

# Create a DataFrame
dtPoints = pd.DataFrame({
    'Longitude': xs,
    'Latitude': ys,
    'NDVI': values
})

# Save to CSV
output_filename = f"{state}_NDVI_{data_year}.csv"
dtPoints.to_csv(os.path.join(output_directory, output_filename), index=False)

print("Conversion completed and saved to:", os.path.join(output_directory, output_filename))