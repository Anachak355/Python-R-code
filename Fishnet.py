# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 00:41:56 2021

@author: Anasua
"""

import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np
points = gpd.read_file("D:\\Belgium\\sample_Test\\ST_Leuven.shp")
xmin,ymin,xmax,ymax =  points.total_bounds
width = 200
height = 100
rows = int(np.ceil((ymax-ymin) /  height))
cols = int(np.ceil((xmax-xmin) / width))
XleftOrigin = xmin
XrightOrigin = xmin + width
YtopOrigin = ymax
YbottomOrigin = ymax- height
polygons = []
for i in range(cols):
    Ytop = YtopOrigin
    Ybottom =YbottomOrigin
    for j in range(rows):
        polygons.append(Polygon([(XleftOrigin, Ytop), (XrightOrigin, Ytop), (XrightOrigin, Ybottom), (XleftOrigin, Ybottom)])) 
        Ytop = Ytop - height
        Ybottom = Ybottom - height
    XleftOrigin = XleftOrigin + width
    XrightOrigin = XrightOrigin + width

grid = gpd.GeoDataFrame({'geometry':polygons})
grid.set_crs("EPSG:31370")
grid.to_file("gridgeodanda.shp")