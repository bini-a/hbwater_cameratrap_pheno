## explore script 

projdir <- getwd()

folder <- "W6 Channel Oct-Dec 2018"

imagedir <- paste0(projdir, "/data_raw/", folder)
imagedata <- data.frame(imagename = list.files(imagedir))
#imagedata$sitename <- substr(imagedata$imagename, 1, 8)
imagedata$year <- substr(imagedata$imagename, 10, 13)
imagedata$month <- substr(imagedata$imagename, 14, 15)
imagedata$day <- substr(imagedata$imagename, 16, 17)
imagedata$hour <- substr(imagedata$imagename, 19, 20)
imagedata$min <- substr(imagedata$imagename, 21, 22)
imagedata$sec <- substr(imagedata$imagename, 23, 24)

write.csv(imagedata, file = paste0(imagedir, "/filelist.csv"), row.names = F)

