## create filelist for xROI 
## created on Oct 5 2020 
## ------------------------

# test

#get google drive photos

library(googledrive)
drive_auth()
drive_find(n_max = 30)

shared_ID <- shared_drive_find(n_max = 30)[1,]$id
drive_find(pattern = "labeled_image_files", n_max = 30, shared_drive = shared_ID) #find this data file
(input_data_folder <- drive_ls(as_id("19DyxgtprkcqbDBuKmMioJg6B86oXDa9K")))
images_folder <- drive_ls(as_id("1B5DN4tE4i-WF-ZikgN3DTnUDNx8xYEAL")) #don't print, it's too many files
images_folder$name

#df = data.frame(x = images_folder$name[1:10])
projdir_image <- getwd()
folder <- "W6 GC Channel 3-16-20 thru 11-5-20" #testing


create_filelist_internal <- function(image_name){
  imagedata <- data.frame(imagename = image_name)
  imagedata$year <- as.numeric(substr(imagedata$imagename, 10, 13))
  imagedata$month <- as.numeric(substr(imagedata$imagename, 14, 15))
  imagedata$day <- as.numeric(substr(imagedata$imagename, 16, 17))
  imagedata$hour <- as.numeric(substr(imagedata$imagename, 19, 20))
  imagedata$min <- as.numeric(substr(imagedata$imagename, 21, 22))
  imagedata$sec <- as.numeric(substr(imagedata$imagename, 23, 24))
  imagedata$date <- as.Date(substr(imagedata$imagename, 10, 17), format = "%Y%m%d")
  return(imagedata)
}

w1 <- create_filelist_internal(images_folder$name)
w6 <- create_filelist_internal(images_folder$name)
head(w1)
w6$val <- 1

w6_filled <- merge(data.frame(date = seq.Date(min(w6$date, na.rm = TRUE), max(w6$date, na.rm = TRUE), by = "day")), w6, all.x = TRUE) 
view(w1_filled)

library(dplyr)

dups = w6 %>% 
group_by(date) %>%
filter(year %in% c(2020,2021)) %>%
summarise(n = length(date)) %>%
filter(n >1)

dups = w1 %>% 
group_by(date) %>%
filter(year %in% c(2020,2021)) %>%
summarise(n = length(date)) %>%
filter(n >1)

#This is the original create list files for xROI
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
#install.packages("")
library(sf)

xROI::Launch()
