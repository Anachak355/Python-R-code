# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 03:07:27 2021

@author: Anasua
"""

import rasterio

with rasterio.open("D:\\cad_ML_24_03_21\\Data Prep\\Nivelles\\2016.tif") as src:
    
    array1 = src.read()
    
    
   
with rasterio.open("D:\\cad_ML_24_03_21\\Data Prep\\Nivelles\\2010.tif") as src:
    array2 = src.read()
    
    array_result = array1-array2

with rasterio.open("Difference_10_16.tif",'w',**src.meta) as dst:
    dst.write(array_result)