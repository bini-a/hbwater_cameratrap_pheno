## see what kind of data we have: 

list.files()
input_list <- list()
for(i in 1:6){
  input_list[[i]] <- read.csv(list.files("data/training_data/input_data/", 
                                         "*.csv", full.names = T)[i])
}

input_list[[1]]

input <- data.table::rbindlist(input_list)

library(dplyr)

input_summary <- input %>% mutate(ws = ifelse(grepl("w6", filename), "w6", "w1")) %>% group_by(ws, region_attributes) %>% summarise(n = length(region_attributes))

grepl(pattern = "w6", input$filename,)

library(ggplot2)

ggplot(data = input_summary %>% filter(n>10)) + geom_bar(aes(x = region_attributes, y = n), stat = "identity") + facet_grid(~ws) + theme_bw() + theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) + coord_flip()

input %>% mutate(date = as.Date(substr(input$filename, 17, 17+7), 
                                format = "%Y%m%d"), 
                 ws = ifelse(grepl("w6", filename), "w6", "w1")) %>% select(ws, date) %>% distinct() %>% mutate(n = 1) %>% 
  ggplot() + geom_bar(aes(x = lubridate::month(date), y = n), stat = "identity") + facet_grid(~ws) + labs(x = "month") + theme_bw()


as.Date(unique(substr(input$filename, 17, 17+7)), format = "%Y%m%d") 
