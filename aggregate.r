CAD = raster("CAD_2019.tif")
CAD_aggregate = aggregate(CAD,fact=334,fun=sum,expand=TRUE)
CAD_aggregate  <- CRS("+init=esri:31370")
#plot(CAD_aggregate)
writeRaster(CAD_aggregate, filename="D:/UDMS/Aggregate/CAD_2019/Nivelles/100m_N.tif", 
              format='GTiff', overwrite=TRUE)
