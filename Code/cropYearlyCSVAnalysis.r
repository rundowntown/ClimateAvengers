install.packages(c("dplyr", "data.table", "ggplot2"))
library(dplyr)
library(data.table)
library(ggplot2)

# Read all crop data files
dt2020 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2020.csv"))
dt2019 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2019.csv"))
dt2018 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2018.csv"))
dt2017 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2017.csv"))
dt2016 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2016.csv"))
dt2015 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2015.csv"))
dt2014 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2014.csv"))
dt2013 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2013.csv"))
dt2012 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2012.csv"))
dt2011 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2011.csv"))
dt2010 <- as.data.table(read.csv("D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_CropGeoData_2010.csv"))




###### Clean Data ######
# List of crop types to exclude
exclude_crops <- c("Deciduous Forest", "Other Hay/Non Alfalfa", "Grass/Pasture", "Alfalfa", "Sorghum",
                   "Christmas Trees", "Sod/Grass Seed", "Fallow/Idle Cropland", "Clover/Wildflowers",
                   "Triticale", "Tobacco", "Misc Vegs & Fruits", "Millet", "Other Crops", "Mixed Forest", "Evergreen Forest", "Open Water"
                   , "Developed/Open Space", "Woody Wetlands",  "Developed/Low Intensity", "Shrubland", "Developed/Med Intensity", "Herbaceous Wetlands"
                   , "Other Tree Crops",  "Developed/High Intensity", "Barren")

# Filter out the specified crop types
dt2020 <- dt2020[!(CropTypes %in% exclude_crops)]
dt2019 <- dt2019[!(CropTypes %in% exclude_crops)]
dt2018 <- dt2018[!(CropTypes %in% exclude_crops)]
dt2017 <- dt2017[!(CropTypes %in% exclude_crops)]
dt2016 <- dt2016[!(CropTypes %in% exclude_crops)]
dt2015 <- dt2015[!(CropTypes %in% exclude_crops)]
dt2014 <- dt2014[!(CropTypes %in% exclude_crops)]
dt2013 <- dt2013[!(CropTypes %in% exclude_crops)]
dt2012 <- dt2012[!(CropTypes %in% exclude_crops)]
dt2011 <- dt2011[!(CropTypes %in% exclude_crops)]
dt2010 <- dt2010[!(CropTypes %in% exclude_crops)]

# Combine all data.tables into one
combined_dt <- rbindlist(list(dt2020, dt2019, dt2018, dt2017, dt2016, dt2015, dt2014, dt2013, dt2012, dt2011, dt2010))


###### Frequency of each crop type ######
# Calc frequensy for each year
Crop_Freq_2020 <- dt2020 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
Crop_Freq_2019 <- dt2019 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
Crop_Freq_2018 <- dt2018 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
  Crop_Freq_2017 <- dt2017 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
Crop_Freq_2016 <- dt2016 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
Crop_Freq_2015 <- dt2015 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
Crop_Freq_2014 <- dt2014 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
Crop_Freq_2013 <- dt2013 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
Crop_Freq_2012 <- dt2012 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
  Crop_Freq_2011 <- dt2011 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))
Crop_Freq_2010 <- dt2010 %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))

# Convert for ease of use
Crop_Freq_2020 <- data.table(Crop_Freq_2020)
Crop_Freq_2019 <- data.table(Crop_Freq_2019)
Crop_Freq_2018 <- data.table(Crop_Freq_2018)
Crop_Freq_2017 <- data.table(Crop_Freq_2017)
Crop_Freq_2016 <- data.table(Crop_Freq_2016)
Crop_Freq_2015 <- data.table(Crop_Freq_2015)
Crop_Freq_2014 <- data.table(Crop_Freq_2014)
Crop_Freq_2013 <- data.table(Crop_Freq_2013)
Crop_Freq_2012 <- data.table(Crop_Freq_2012)
Crop_Freq_2011 <- data.table(Crop_Freq_2011)
Crop_Freq_2010 <- data.table(Crop_Freq_2010)

# Transform pixel count to acreage
Crop_Freq_2020[, Acres := Count * .222395]
Crop_Freq_2019[, Acres := Count * .222395]
Crop_Freq_2018[, Acres := Count * .222395]
Crop_Freq_2017[, Acres := Count * .222395]
Crop_Freq_2016[, Acres := Count * .222395]
Crop_Freq_2015[, Acres := Count * .222395]
Crop_Freq_2014[, Acres := Count * .222395]
Crop_Freq_2013[, Acres := Count * .222395]
Crop_Freq_2012[, Acres := Count * .222395]
Crop_Freq_2011[, Acres := Count * .222395]
Crop_Freq_2010[, Acres := Count * .222395]



###### Crop Area Over Time #######
# Aggregate or ensure you have the data in the format you need for plotting
agg_data <- combined_dt[, .(Count = .N), by = .(Year, CropTypes)]

# Data for corn and soybeans only
corn_soybeans_data <- agg_data[CropTypes %in% c("Corn", "Soybeans")]

# For plots
custom_dark_theme <- theme(
  plot.background = element_rect(fill = "#121212", color = NA), # muted black background
  panel.background = element_rect(fill = "#121212"), # muted black for the panel
  text = element_text(color = "white"), # white text for readability
  axis.title = element_text(color = "white"), # white axis titles
  axis.text = element_text(color = "white"), # white axis text
  legend.background = element_rect(fill = "#121212"), # muted black for legend background
  legend.text = element_text(color = "white"), # white text for legend
  legend.title = element_text(color = "white"), # white legend titles
  axis.line = element_line(color = "white"), # white axis lines
  panel.grid.major = element_line(color = "grey30"), # darker grid lines
  panel.grid.minor = element_line(color = "grey20"), # even darker minor grid lines
  legend.position = "bottom",
  legend.key = element_blank() # remove the background boxes in legend
)

# Calculate the total area for each crop type
total_area_by_crop <- Crop_Freq_2013[ , .(TotalArea = sum(Count)), by = .(CropTypes)]

# Determine the top 10 crops by area
top_crops <- total_area_by_crop[order(-TotalArea)][1:10, CropTypes]

# Filter the original data to include only the top 10 crops
dt2020_top_crops_lonlat <- dt2013[CropTypes %in% top_crops]

dt2020_top_crops_freq <- dt2020_top_crops_lonlat %>%
  group_by(CropTypes) %>%
  summarise(Count = n()) %>%
  arrange(desc(Count))

fwrite(dt2020_top_crops_lonlat, "D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_top_crops_lonlat_2013.csv", row.names = FALSE )
fwrite(dt2020_top_crops_freq, "D:/Documents/GT/MGT 6203/Project/DataSets/VermontCropData/VT_top_crops_freq_2013.csv", row.names = FALSE )


###### Spatial Analysis ######

# Define custom colors for each crop type
crop_colors <- c(
  "Apples" = "red3",
  "Asparagus" = "darkgreen",
  "Barley" = "goldenrod1",
  "Blueberries" = "blue4",
  "Broccoli" = "green4",
  "Corn" = "yellow2",
  "Cucumbers" = "green3",
  "Dry Beans" = "saddlebrown",
  "Grapes" = "plum1",
  "Herbs" = "darkolivegreen1",
  "Oats" = "khaki4",
  "Peaches" = "mistyrose",
  "Pears" = "yellowgreen",
  "Pop or Orn Corn" = "lightsalmon",
  "Potatoes" = "burlywood1",
  "Pumpkins" = "darkorange",
  "Rye" = "tan4",
  "Soybeans" = "olivedrab",
  "Spring Wheat" = "wheat",
  "Squash" = "goldenrod2",
  "Sweet Corn" = "yellow3",
  "Sweet Potatoes" = "sienna1",
  "Winter Wheat" = "wheat3"
)

# All Crops
data_year <- dt2013
All_Crops_Spatial <- ggplot(data_year, aes(x = Longitude, y = Latitude, color = CropTypes)) +
  geom_point(alpha = 0.5, size = .6) +
  scale_color_manual(values = crop_colors) +
  labs(title = "Spatial Distribution of Crops in Vermont",
       x = "Longitude", y = "Latitude") +
  theme_minimal() +
  custom_dark_theme +
  theme(legend.position = "right")
print(All_Crops_Spatial)


#Wrong Long,Lat: 2013, 2012, 2011