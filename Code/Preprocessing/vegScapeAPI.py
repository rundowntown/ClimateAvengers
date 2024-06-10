# -*- coding: utf-8 -*-
"""
Created on Sun Jun  9 13:16:53 2024

@author: dforc
"""

import requests
import json

def get_vegscape_data(fips, date):
    url = f"https://nassgeodata.gmu.edu/VegService/GetFile?fips={fips}&date={date}"
    response = requests.get(url, verify=False)  # Disable SSL certificate verification
    if response.status_code == 200:
        # Replace single quotes with double quotes
        corrected_json = response.text.replace("'", '"')
        try:
            data = json.loads(corrected_json)
            if data['success'] == 'true':
                download_url = data['url']
                print("Downloading file from:", download_url)
                download_file(download_url, fips)
            else:
                print("Data retrieval was not successful.")
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            print("Corrected JSON text:", corrected_json)
    else:
        print("Failed to retrieve data:", response.status_code)

def download_tif_file(url, local_path):
    try:
        # Start the download
        with requests.get(url, stream=True, verify=False) as response:
            response.raise_for_status()  # Will raise an exception for HTTP errors
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Download completed successfully. File saved to {local_path}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
fips_code = "19015"
date_string = "2012.07.09_2012.07.15"
weekly_ndvi_string = "weekly_ndvi_28"  # Correcting potential duplication here
url = f"https://nassgeo.csiss.gmu.edu/ndvi_data_cache/byfips/{weekly_ndvi_string}_{date_string}_{fips_code}.tif"
local_filename = f"{weekly_ndvi_string}_{fips_code}_{date_string}.tif"
download_tif_file(url, local_filename)