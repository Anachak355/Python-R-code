
Liu = raster("2019.tif")
plot(Liu)

Liu<-aggregate(Liu, fact=100, fun=modal) #increase cell size from 0,3 to 100 metres


Liu<-as.factor(Liu) # convert to categorical raster

levels(Liu)#inspect levels

res(Liu)

#create a holder for our raster leves (values)

urban <- levels(Liu)[[1]]

#create a vector of strings (words) to assign to each level

urban[,"urban_built"] <- c("nonbuiltup","builtup") 
levels(Liu) <- urban

Liu.cat <- unique(Liu)
Liu.cat
LiuF <- c(0,1)
reclass.mat <- cbind(Liu.cat,LiuF)# create a matrix for reclassification 
reclass.mat#inspect

#builtup binary layer from reclassification matrix
Liu_BU <- reclassify(Liu,reclass.mat) #use the recassify function passing the raster as the first argument and the reclassification matrix as the second.  
plot(Liu_BU)#plot it!

############################################
#patch-level analysis
############################################

#8-neighbour rule
LiuF8 <- clump(Liu_BU, directions=8)

cellStats(LiuF8, max)


# now use the PatchStat() function to compute a range of metrics. Note with large data sets the function works best when the raster is firt converted to a matrix of values.

LiuFstat <- PatchStat(as.matrix(LiuF8), cellsize=0.3)

#list the names of the metrics we have just computed.
names(LiuFstat)

#get the mean of each column (excluding column 1 - ID)

LiuFstat.mean <- colMeans(LiuFstat[,2:ncol(LiuFstat)])
LiuFstat.mean

#plot area frequencies on a log scale
hist(log(LiuFstat$area))

#correlation matrix
round(cor(LiuFstat[,6:12]),2)

#plot correlation across for key metrics

pairs(LiuFstat[,c("area","core.area", "perim.area.ratio", "shape.index")])

############################################
#Class-level quantification
############################################

# check the documentation
?ClassStat

#calculation based on builtup layer
Liucstat <- ClassStat(as.matrix(Liu_BU), cellsize=res(Liu_BU)[[1]])

#let's just return a selection of the results 
Liucstat[,c(2:4,19,37,38)]

#calculation based on Liu layer (all land-cover types)
Liu.cstat <- ClassStat(as.matrix(Liu), cellsize=res(Liu)[[1]])

head(Liu.cstat)

#check against PatchStat calculations:

#mean patch size for builtup layer ('1 ' in original raster)
Liu.cstat[Liu.cstat$class==1, "mean.patch.area"]

LiuFstat.mean["area"]#mean patch size

#correlation matrix
classcorelation <- cor(Liu.cstat[,c(2:4,19,37,38)])#subset of metrics

#plot subset of metrics
pairs(Liu.cstat[,c(2:4,19,37,38)])



#----------------------------------#
#diversity-related metrics
#----------------------------------#

#richness
richness <- length(unique(values(Liu)))
richness

#richness function to calulate richness that removes NAs
richness <- function(x) length(unique(na.omit(x)))

richness(Liu)

# Shannon's diversity index ,D

table(values(Liu))

C <- table(values(Liu))


P <- C / sum(C)

D <- -sum(P * log(P))

D

write.csv(LiuFstat,"D:/cad_ML_24_03_21/Output/Landscape Metrics/Patchlevel_Nivelles_ML2019.csv")
write.csv(Liu.cstat,"D:/cad_ML_24_03_21/Output/Landscape Metrics/Classlevel_Nivelles_ML2019.csv")
write.csv(LiuFstat.mean,"D:/cad_ML_24_03_21/Output/Landscape Metrics/Meanpatch_Nivelles_ML2019.csv")


#SD of patch metrics
LiuFstat.sd <- apply(LiuFstat[,2:ncol(LiuFstat)], 2, sd)
LiuFstat.sd
write.csv(LiuFstat.mean,"D:/cad_ML_24_03_21/Output/Landscape Metrics/SDpatch_Nivelles_ML2019.csv")
write.csv(LiuFstat.mean,"D:/cad_ML_24_03_21/Output/Landscape Metrics/ClassCorrelation_Nivelles_ML2019.csv")
