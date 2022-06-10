## create filelist for xROI 
## created on Oct 5 2020 
## ------------------------

# test

getwd()

projdir_image <- getwd()
folder <- "W6 GC Channel 3-16-20 thru 11-5-20" #testing

create_filelist <- function(projdir_image, folder) {
  imagedir <- paste0(projdir_image, "/data_raw/", folder)
  imagedata <- data.frame(imagename = list.files(imagedir, pattern = "*.JPG"))
  #imagedata$sitename <- substr(imagedata$imagename, 1, 8)
  imagedata$year <- as.numeric(substr(imagedata$imagename, 10, 13))
  imagedata$month <- as.numeric(substr(imagedata$imagename, 14, 15))
  imagedata$day <- as.numeric(substr(imagedata$imagename, 16, 17))
  imagedata$hour <- as.numeric(substr(imagedata$imagename, 19, 20))
  imagedata$min <- as.numeric(substr(imagedata$imagename, 21, 22))
  imagedata$sec <- as.numeric(substr(imagedata$imagename, 23, 24))
  
  colnames(imagedata) <- NULL

write.csv(imagedata, file = paste0(imagedir, "/filelist.csv"), row.names = F)
}

thell_proj <- "C:/Users/Thell/Documents/Duke University/Research/_HBEF/CameraTrapAnalysis/hbwater_cameratrap_pheno"


create_filelist(folder = "W3 GC Channel 2-5-19 thru 12-31-19", projdir = thell_proj)


## 
library("xROI")

xROI::Launch()
