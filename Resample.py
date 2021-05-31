# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 13:29:10 2021

@author: Anasua
"""

import geopandas
from osgeo import gdal


PS4= gdal.Open("bel_ppp_16.tif")
#array = Landscan.GetRasterBand(1).ReadAsArray()
#plt.imshow(array)
#plt.colorbar()


Landscan_resample = gdal.Translate("Population_Count_2016.tif",PS4,xRes=100,yRes=-100,
                                resampleAlg="bilinear",outputSRS="EPSG:31370",creationOptions=["COMPRESS=LZW"])
#array = Landscan_resample.GetRasterBand(1).ReadAsArray()
#plt.imshow(array)
#plt.colorbar()


