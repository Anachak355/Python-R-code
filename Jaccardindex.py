# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 09:08:46 2021

@author: Anasua
"""

import numpy as np
from osgeo import gdal,ogr


def jaccard_binary(x,y):
    """A function for finding the similarity between two binary vectors"""
    intersection = np.logical_and(x, y)
    union = np.logical_or(x, y)
    similarity = intersection.sum() / float(union.sum())
    return similarity


raster1 = gdal.Open("2019.tif")
x = raster1.ReadAsArray()

raster2 = gdal.Open("2016.tif")
y = raster2.ReadAsArray()

raster3 = gdal.Open("2010.tif")
z = raster3.ReadAsArray()

raster4 = gdal.Open("2000.tif")
a = raster4.ReadAsArray()

raster5 = gdal.Open("CAD_2019.tif")
b = raster5.ReadAsArray()


#jaccard index and distance between x and b
Jaccard_Index_xb = jaccard_binary(x,b)
Jaccard_distance_xb = 1 - Jaccard_Index_xb


#jaccard index and distance between y and z
Jaccard_Index_yz = jaccard_binary(y,z)
Jaccard_distance_yz = 1 - Jaccard_Index_yz


#jaccard index and distance between z and a
Jaccard_Index_za = jaccard_binary(z,a)
Jaccard_distance_za = 1 - Jaccard_Index_za

#jaccard index and distance between b and y
Jaccard_Index_by = jaccard_binary(b,y)
Jaccard_distance_by = 1 - Jaccard_Index_by



#Printing the results
print(' Similarity between Liu and CAD_2019 is', Jaccard_Index_xb, 
          '\n Similarity between 2016 and 2010 is ', Jaccard_Index_yz, 
              '\n Similarity between 2010 and 2000 is ', Jaccard_Index_za,
              '\n Similarity between CAD_2019 and 2016 is ', Jaccard_Index_by)

print(' Jaccard Distance between Liu and CAD_2019 is', Jaccard_distance_xb, 
              '\n Jaccard Distance  between 2016 and 2010 is ', Jaccard_distance_yz, 
              '\n Jaccard Distance  between 2010 and 2000 is ', Jaccard_distance_za,
                  '\n Jaccard Distance  between CAD_2019 and 2016 is ', Jaccard_distance_za)
             