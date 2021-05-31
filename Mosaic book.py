# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 18:20:00 2021

@author: Anasua
"""

from osgeo import gdal,os
import glob
import matplotlib.pyplot as plt
import math
import numpy

def get_extent(fn):
 '''Returns min_x, max_y, max_x, min_y'''
 ds = gdal.Open(fn)
 gt = ds.GetGeoTransform()
 return (gt[0], gt[3], gt[0] + gt[1] * ds.RasterXSize,
 gt[3] + gt[5] * ds.RasterYSize)

#Calculate output extent from all inputs
infiles=glob.glob("*.tif")
min_x, max_y, max_x, min_y = get_extent(infiles[0])
for fn in infiles[1:]:
    minx, maxy, maxx, miny = get_extent(fn)
    min_x = min(min_x, minx)
    max_y = max(max_y, maxy)
    max_x = max(max_x, maxx)
    min_y = min(min_y, miny) 

#Calculate dimensions
in_ds = gdal.Open(infiles[0])
gt = in_ds.GetGeoTransform()
rows = math.ceil((max_y - min_y) / -gt[5])
columns = math.ceil((max_x - min_x) / gt[1]) 


#Create output
driver = gdal.GetDriverByName('gtiff')
out_ds = driver.Create("D:\Planetscope_preprocessing\Planet_Bel_output_30122020\Liu\Mosaic_uncompV2.tif", columns, rows)
out_ds.SetProjection(in_ds.GetProjection())
out_band = out_ds.GetRasterBand(1)




#Calculate new geotransform
gt = list(in_ds.GetGeoTransform())
gt[0], gt[3] = min_x, max_y
#gt[1],gt[5] = 0.3,-0.3
out_ds.SetGeoTransform(gt) 
lt=out_ds.GetGeoTransform()

#offsets
Xoff = int((gt[0] - lt[0])/lt[1]) # cols to skip
Yoff = int((gt[3] - lt[3])/lt[5]) # rows to skip



#Get output offsets
for fn in infiles:
    in_ds = gdal.Open(fn)
    trans = gdal.Transformer(in_ds, out_ds, [])
    success, xyz = trans.TransformPoint(False,0,0)
    x, y, z = map(int, xyz)
    #zeros=numpy.zeros((columns,rows),dtype=numpy.uint8)
    data = in_ds.GetRasterBand(1).ReadAsArray()
    out_band.WriteArray(data, x, y)
     
del in_ds, out_band, out_ds

#raster= gdal.Open('Mosaic_uncomp.tif')
#ds=gdal.Translate("Liu_mosaic.tif",raster, outputSRS= 'EPSG:32631', creationOptions=["COMPRESS=LZW"])