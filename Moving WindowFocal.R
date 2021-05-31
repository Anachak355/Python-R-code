CAD <- raster("2019.tif")
CAD<-aggregate(CAD, fact=10, fun=modal) #increase cell size from 0,3 to 3 metres


CAD<-as.factor(CAD)# convert to categorical raster

levels(CAD)#inspect levels

res(CAD)

#create a holder for our raster leves (values)

urban <- levels(CAD)[[1]]

#create a vector of strings (words) to assign to each level

urban[,"urban_built"] <- c("nonbuiltup","builtup") 
levels(urban) <- urban

urban.cat <- unique(CAD)
urban.cat
urbanF <- c(0,1)
reclass.mat <- cbind(urban.cat,urbanF)# create a matrix for reclassification 
reclass.mat#inspect

#builtup binary layer from reclassification matrix
urban_BU <- reclassify(CAD,reclass.mat) #use the recassify function passing the raster as the first argument and the reclassification matrix as the second.  
plot(urban_BU)


#focal buffer matrix for moving windows
buffer.radius <- 800
fw.100m <- focalWeight(urban_BU, buffer.radius, 'rectangle')#buffer in CRS units

#inspect the focalWeight object
fw.100m

#re-scale weight matrix to 0,1
fw.100m <- ifelse(fw.100m > 0, 1, 0)

#inspect the re-scaled object
fw.100m

#forest cover moving window; number of cells
urban.30m <- focal(urban_BU, w=fw.100m,fun='sum',na.rm=T)
plot(urban.30m)

#proportion of forest
urban.prop.30m <-urban.30m/sum(fw.100m) #proportion: divide by buffer size
plot(urban.prop.30m)

#weight matrix for a Gaussian kernel
focalGauss<-focalWeight(urban_BU, c(50,800), type = "Gauss")
plot(focalGauss)


writeRaster(urban.30m,'D:/cad_ML_24_03_21/Output/MovingWindow/UrbanWindow_ML2019Nivelles_3m_800m.tif',options=c('TFW=YES'))
