# Computer-Vision: Sentinel-2 Image Matching

## Overview
The goal of this project is to create a computer vision (CV) model for matching satellite images. For this purpose, the pretrained LoFTR model was used.

## 1. Data Preprocessing
### Dataset
The working dataset was created from the first 10 images obtained from [Deforestation in Ukraine from Sentinel-2 data](https://www.kaggle.com/datasets/isaienkov/deforestation-in-ukraine). The photos (in `.zip` format) can be found on Google Drive, with the link provided in *images_data.txt*. 

### Steps
All data preprocessing steps were performed in the file *dataset_creation_cv.py*. The steps included:
1. Unzipping the images.
2. Reading the images using the specialized *rasterio* library, which is commonly used for georeferenced images.
3. Scaling the images to a resolution of `(1024, 1024)`.
4. Saving the preprocessed images into the *images.csv* file, which can also be obtained from the same Google Drive location as the original images (*images_data.txt*).

## 2. Model Creation
### Process
The entire model creation process is implemented in the file *algorithm_creation.py*. For this project, the pretrained LoFTR model was selected and fine-tuned for "outdoor" images. To simplify usage, all necessary steps (functions) required to get the model working are encapsulated within a single class.

### Key Steps
1. **Normalization**: If needed, the data is normalized.
2. **Tensor Conversion**: Data is transformed into PyTorch tensors (as the LoFTR model works exclusively with tensors).
3. **Matching**: Matches are detected using the model, and valid matches (recognized as inliers) are selected.
4. **Visualization**: Matches are visualized using the `draw_LAF_matches` function from the *kornia_moons.viz* class.

## 3. Model Inference
### Evaluation
Model inference was performed on the *images.csv* dataset created during the Data Preprocessing step. The resulting images with visualized matches are included in the *Model_inference_cv.ipynb* file.

## Additional Files
- **potential_improvements.pdf**: Describes possible steps to improve the model's performance.
- **requirements.txt**: Lists all libraries used in this project.
