## create filelist for xROI 
## created on Oct 5 2020 
## ------------------------

getwd()

#projdir_image <- getwd()
#folder <- "W6 Channel Oct-Dec 2018"

create_filelist <- function(projdir, folder) {
  projdir_image <- projdir
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

write.csv(imagedata, file = paste0(imagedir, "/filelist.csv"), row.names = F, col.names = FALSE)
}



create_filelist(folder = "W6 Channel Oct-Dec 2018", projdir = getwd())


## 
library(xROI)
Launch()
