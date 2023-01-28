# hbwater_cameratrap_pheno
Building a Data Pipeline for processing Hubbard Brook  Water aquatic camera trap photos for machine learning, that can be extended to produce models from similar datasets.


## Project Steps 
1. Image data re-organization 
2. Region of Interest(ROI)  
3. Project File organization
4. Creation of inverted masked images
5. Creation of Training Data sets using Image Annotation
6. Building Machine Learning Classification Model
7. Creation of Streamlied Data Pipeline for Quantiative Prediction and Additional Training
8. Creation of accompanying data product: Bookdown, Application, Demo

## Code Structure
- Scripts/01-Rename -> renaming and organizing image files structure
- Scripts/02-ROI -> Building an interactive application to allow selection of Region of Interest in image files
- Scripts/03-ML -> Running machine learning model to predict ice/snow coverage and produce time series analysis
- Data -> passing throgh series of stages from raw ->derived -> munged
- Bookdown -> markdown tutorial on how to use this product and documenation of the workflow of the data pipeline
