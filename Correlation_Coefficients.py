# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 23:28:39 2021

@author: Anasua
"""

import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt
from osgeo import gdal
import numpy as np
import scipy.stats
from sklearn import metrics
from sklearn.linear_model import LogisticRegression

raster1 = gdal.Open("D:\\cad_ML_24_03_21\\Output\MovingWindow\\NIvelles\\UrbanWindow_CAD2019Nivelles_3m_400m.tif")
array1 = raster1.ReadAsArray()
actual_2019 = array1.flatten() 

raster2 = gdal.Open("D:\\cad_ML_24_03_21\\Output\MovingWindow\\NIvelles\\UrbanWindow_ML2019Nivelles_3m_400m.tif")
array2 = raster2.ReadAsArray()
predicted_2019 = array2.flatten()


plt.plot(actual_2019,predicted_2019,'o')
m,b = np.polyfit(actual_2019,predicted_2019,1)
plt.plot(actual_2019,m*actual_2019+b)


#confusion_matrix =pd.crosstab(actual_2019, predicted_2019, rownames=['Actual'], colnames=['Predicted'],margins=True)

pearson = scipy.stats.pearsonr(actual_2019, predicted_2019) 
print(pearson)

spearman = scipy.stats.spearmanr(actual_2019,predicted_2019)
print(spearman)

kendalls = scipy.stats.kendalltau(actual_2019,predicted_2019)
print(kendalls)

correlation_matrix = np.corrcoef(actual_2019,predicted_2019)
correlation_matrix

plt.plot(spearman,kendalls)
plt.show()

linear_regression = scipy.stats.linregress(actual_2019,predicted_2019)
linear_regression

#Coefficient of determination (R-squared):

print(f"R-squared: {linear_regression.rvalue**2:.6f}")


#MAE
print(metrics.mean_absolute_error(actual_2019,predicted_2019))

#MSE
print(metrics.mean_squared_error(actual_2019,predicted_2019))

#RMSE
print(np.sqrt(metrics.mean_squared_error(actual_2019,predicted_2019)))


