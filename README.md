# hbwater_cameratrap_pheno
Building a pipeline for processing HB Water aquatic camera trap photos for machine learning, with hopes to support further efforts to produce models from similar datasets.


## Project Steps 
1. image data re-organization 
2. ROI  
3. project file organization, structure, and primary host - GDrive? Server?
4. created inverted masked images
5. classify pixels in image using image annotator 
6. run random forest model
7. create data product: markdown
8. create data product: application

## Code Structure
- scripts/01-Rename --> renaming and organizing image files structure
- scripts/02-ROI ---> Building an interactive application to allow selection of Region of Interest in image files
- scripts/03-ML ----> Running machine learning model to predict ice/snow coverage and produce time series analysis
- data -> passing throgh series of stages from raw ->derived -> munged
- bookdown --> markdown tutorial on how to use this product and documenation of the workflow of the data pipeline
