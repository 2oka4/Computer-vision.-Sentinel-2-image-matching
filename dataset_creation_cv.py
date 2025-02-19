# -*- coding: utf-8 -*-

!pip install rasterio

import os
import zipfile
import tempfile
import rasterio
import matplotlib.pyplot as plt
import numpy as np
from rasterio.plot import reshape_as_image
import cv2
import pandas as pd

def process_and_store_zip_jp2(directory):
    # Ensure the directory exists
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return []

    processed_data = []  # To store the RGB raster data

    # Iterate over all ZIP files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".zip"):
            zip_path = os.path.join(directory, filename)

            # Create a temporary directory to extract files
            with tempfile.TemporaryDirectory() as temp_dir:
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Find JP2 files in the extracted folder
                for extracted_file in os.listdir(temp_dir):
                    if extracted_file.endswith(".jp2"):
                       jp2_path = os.path.join(temp_dir, extracted_file)
                       with rasterio.open(jp2_path, "r", driver="JP2OpenJPEG") as src:
                        raster_image = src.read()
                        bands, height, width = raster_image.shape
                        scale = 1024 / max(height, width) #scaling image to the format (1024,1024)
                        new_height, new_width = int(height * scale), int(width * scale)

                        resized_bands = [cv2.resize(raster_image[i], (new_width, new_height), interpolation=cv2.INTER_AREA) for i in range(bands)]
                        resized_image = np.stack(resized_bands, axis=-1)
                        processed_data.append(resized_image)
    return processed_data

images = process_and_store_zip_jp2("./images_zip") #getting zip images from path

images[0].shape #checking images shape (3 is number of bands (in our case for RGB))

# Flatten each image into a 1D array
flattened_images = [img.flatten() for img in images]

# Stack flattened arrays into a 2D array
data = np.stack(flattened_images)

# Save to CSV using pandas for better formatting
df = pd.DataFrame(data)
df.to_csv('images.csv', index=False, header=False)
