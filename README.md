# hbwater_cameratrap_pheno
building a pipeline for processing HB Water aquatic camera trap photos for machine learning, with hopes to support further efforts to produce models from similar datasets.


## Project Steps 
1. image data re-organization 
2. ROI  
3. project file organization, structure, and primary host - GDrive? Server?
4. created inverted masked images
5. classify pixels in image using image annotator 
6. run random forest model
7. create data product: markdown
8. create data product: application


## Current Objectives
Tasks | People | Step
------- | -------- | --------
~~continue debugging the GDrive image copy/rename/organization scripts~~| BG, HS | **1**
~~figure out how to show mask on consecutive images (clicking thru all the images from a particular watershed year)~~ | HO, BG | **2**
~~allow user to, while clicking through images, stop and create a new mask associated with the date of that image/~~  | HO, BG, HS | **2**
~~create folder for masked images && masks (w/o images) in ROI script~~ | HO, BG, HS | **2**
~~scale masks to original resolution of the image for later use~~| HO, BG, HS | **3**
~~organize the GitHub repo (remove uneeded scripts and standardize naming conventions, etc.)~~   | HS | **3**
~~matplotlib and interactive matplotlib issues on Mac OS~~  | HS, BG, HO | **3**
~~more prominent and better date show on each image slide~~ | HO | **3**
~~prepare presentation for 6/21~~   | HS, BG, HO | **Other**
figure out our file hosting options: server, google drive, local files, etc.   | AT, WS | **3**
~~finish minimum viable product (Bookdown) first draft, setup Github pages~~ | HS, HO | **3**
~~edit bookdown to support generalized usage~~ | HS, HO, BG | **4**
~~familiarize with ML algorithm used~~ | HO, HS, BG | **5**
~~train and test random forest classifier~~ | HO, HS, BG | **5**


## Future Objectives
Tasks | People | Step
------- | -------- | --------
~~create walkthrough with example files as both proof-of-concept for our data pipeline, and as a walkthrough for future users~~ | XX | **7**
export Jupyter notebook to *.py* files  | XX | **8**


## Notes
While the above steps are roughly in order, we will be working on certain aspects of the project throughout, such as:
  - Keeping all code well-documented and clean
  - Creating Jupyter notebooks for each script with embedded markdown/html that explains each step of the script
  - Determining a final product to make data pipeline easily accessible to average scientist


## Progress
- Figured out how to click through image files with mask applied
- Figured outredrawing ROI and applying new mask to remaining images
- Working on file naming conventions/organizing GitHub


## Repo Structure

README.md

data
- derived
- munged
- raw

scripts
- 01-folder
- 02-folder
- etc.
- dep (dependencies)
- sandbox

bookdown
- index.rmd
- 01.rmd
- .yml files

.gitignore

.Rproj
