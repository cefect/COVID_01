## create matrix for counties starting social distancing based on South Korea R0 reductions
##we're actually hardcoding this, but here's a dummy file. 
## R0 in SK .6-1.3, mid 2-3
library(dplyr)

# West coast
county.status <- read.csv(paste0(foldername,'geodata.csv'))
dates <- seq.Date(as.Date(ti_str), as.Date(tf_str), 1)

NPI <- as.data.frame(matrix(0, dim(county.status)[1],length(dates)))
colnames(NPI) <- as.Date(dates)
rownames(NPI) <- county.status$geoid
