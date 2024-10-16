## renaming script from google drive, already run 

library(googledrive)
drive_auth()
shared_ID <- shared_drive_find(n_max = 30)[1,]$id
w6_train <- drive_find(n_max = 30, shared_drive = shared_ID, pattern = "W6_train")[1,]$id #find this data file
w1_train <- drive_find(n_max = 1000, shared_drive = shared_ID, pattern = "W1_train")[1,]$id
w1_train
#images_folder <- drive_ls(as_id(w6_train), recursive = T, pattern = "*.jpg|JPG") 
images_folder <- drive_ls(as_id(w1_train), recursive = T, pattern = "*.jpg|JPG") #don't print, it's too many files
length(images_folder$name) #got images with jpg extensions


images_folder[1,]$name

one_image <- drive_find(pattern = "Hbwtr_w6_20201106_115941", n_max = 30)
one_image

drive_rename(one_image, name = paste0("invert_", one_image$name), )

for(i in 1:length(images_folder$name)){
    if(grepl(images_folder[i,]$name, pattern = "invert")){
        print(paste("skipped", images_folder[i,]$name))
    }else{
        drive_rename(images_folder[i,], name = paste0("invert_", images_folder[i,]$name))
    }
   
}
grepl("invert_hbwtr_02.jpg", pattern = "invert" )

 drive_rename(one_image, name = paste0("invert_", one_image$name))