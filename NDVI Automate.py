#!/usr/bin/env python
# coding: utf-8

# In[4]:


import rasterio
import glob
import os
import numpy


# In[5]:


Path = 'D:\\Planetscope\\'
os.chdir('D:\\Planetscope\\')
Path1 = glob.glob("*_PSScene4Band_Explorer")
print(Path1)
len(Path1)


# In[10]:


for i in Path1[0:len(Path1)]:
    Path2 = i + '\\files\\PSScene4Band\\' + i[:20] + '\\analytic_sr_udm2\\'
    os.chdir(Path + Path2)
    Filnam = glob.glob('*_3B_AnalyticMS_SR.tif')
    for j in Filnam[0:len(Filnam)]:
        X = rasterio.open(j)
        RED = X.read(3).astype(rasterio.float64)
        NIR = X.read(4).astype(rasterio.float64)
        NDVI = (NIR-RED)/(NIR+RED)
        with rasterio.Env():
    
            profile = X.profile
   
            profile.update(
              dtype=rasterio.float64,
              count=1,
              compress='lzw')
            with rasterio.open('D:\\Planet_Bel_output_30122020\\ndvi_test\\N_' + str(j) , 'w', **profile) as dst:
              dst.write(NDVI.astype("float64"), 1) 
   


# In[ ]:





# In[ ]:





# In[ ]:




