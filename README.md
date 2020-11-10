# hbwater_cameratrap_pheno
Aquatic camera trap photos for HB Water

## folder structure 
* data der = derrived files from Python and xROI
* data raw = raw data files from Abena's renaming and analysis 

## analysis steps 
1. load images for one watershed into "data raw" with file name 
2. create filelist using R script 
3. create ROIs using xROI
4. created inverted masked images for image analysis (python script) 
5. classify pixels in image using image annotator 
6. run random forest model
