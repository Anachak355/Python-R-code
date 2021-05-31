
# import matplotlib.pyplot as plt
# plt 用于显示图片
# import matplotlib.image as mpimg # mpimg 用于读取图片
# import torch
# import torchvision
# import torchvision.transforms as transforms
# import matplotlib.pyplot as plt
#import numpy as np
#from torch.autograd import Variable
#import torch.nn as nn
#import torch.nn.functional as F
#import torch.optim as optim
#from PIL import Image
from osgeo import gdal
import os
#from sklearn.model_selection import train_test_split
#import copy

class Grid:
    #读图像文件
    def read_img(self,filename):
        dataset=gdal.Open(filename)      #open a file

        self.im_width = dataset.RasterXSize    #Number of columns of the grid matrix
        self.im_height = dataset.RasterYSize   #Raster matrix rows
        self.im_bands = dataset.RasterCount

        self.im_geotrans = dataset.GetGeoTransform()  #Affine matrix
        self.im_proj = dataset.GetProjection() #Map projection information
        self.im_data = dataset.ReadAsArray(0,0,self.im_width,self.im_height) #Write the data as an array, corresponding to the grid matrix

        del dataset
        return self.im_proj,self.im_geotrans,self.im_data

    #Write a file, take writing as tif as an example
    def write_img(self,filename,im_proj,im_geotrans,im_data):
        #gdalData types include
        #gdal.GDT_Byte,
        #gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
        #gdal.GDT_Float32, gdal.GDT_Float64

        #Judging the data type of raster data
        if 'int8' in im_data.dtype.name:
            datatype = gdal.GDT_Byte
        elif 'int16' in im_data.dtype.name:
            datatype = gdal.GDT_UInt16
        elif 'float32' in im_data.dtype.name:
            datatype = gdal.GDT_Float32
        else:
            datatype = gdal.GDT_Float64

        #Judgment of reading group dimension
        if len(im_data.shape) == 3:
            im_bands, im_height, im_width = im_data.shape
        else:
            im_bands, (im_height, im_width) = 1,im_data.shape

        
#Create a file
        driver = gdal.GetDriverByName("GTiff") #Data driver type, because how much memory space is needed to calculate
        dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

        dataset.SetGeoTransform(im_geotrans)              #Write affine transformation parameters
        dataset.SetProjection(im_proj)                    #Write projection

        if im_bands == 1:
            dataset.GetRasterBand(1).WriteArray(im_data)  #Write array data
        else:
            for i in range(im_bands):
                dataset.GetRasterBand(i+1).WriteArray(im_data[i])

        del dataset


    def crop(self, minC, maxC, minX, maxX, minY, maxY):
        if self.im_bands == 1:
            cropdata = self.im_data[minY: maxY, minX: maxX]
        else:
            cropdata = self.im_data[minC: maxC, minY: maxY, minX: maxX]
        CropGeoTrans = list(self.im_geotrans)
        CropGeoTrans[0] = self.im_geotrans[0] + minX * self.im_geotrans[1] + minY * self.im_geotrans[2]
        CropGeoTrans[3] = self.im_geotrans[3] + minX * self.im_geotrans[4] + minY * self.im_geotrans[5]
        return cropdata, CropGeoTrans, self.im_proj






if __name__ == "__main__":
    rsbs_dir = "D:\\Parcel\\Tiling_800\\test"
    resolution = 0.3
    sampsize = 800 #width and height of the sample patch
    scount = 0
    sampnumc = 1
    sampnumr = 30
    # sampnum*sampnum
    # Austin Chicago Vienna : col3000 * row3000
    # Kitsap: Kitsap_4b_mos_clip1: col3000 * row2500 / Kitsap_4b_mos_clip2: col1500 * row1000 / Ktisap_gt2_rsp / Ktisap_gt1_rsp (the order of filename is reversed)
    # Tyrol: Tyrol1-36 / Tyrol1_gt_rsp: col500 * row500

    # orgimage_name = 'D:\\DSC\\planetscope\\Kitsap\\Kitsap_4b_mos_clip2.tif'
    # grdtrh_name = 'D:\\DSC\\planetscope\\Kitsap\\Kitsap_gt1_rsp.tif'

    orgimage_name = "D:\\Parcel\\Rasterise\\2_2m\\Ras_Builtup_2016.tif"

    ################################### input training raster
    ### [channel,upleftY:lowrightY,upleftX:lowrightX]
    Train = Grid()
    proj, geotrans, data = Train.read_img(orgimage_name)  # Read data
    startx = 0
    starty = 0
    count = scount



    for i in range(sampnumc):  # col
        starty = 0
        for j in range(sampnumr):  # row
            cropdata, CropGeoTrans, proj = Train.crop(0, 4, startx, startx + sampsize, starty, starty + sampsize)
            str1 = str(count) + '.tif'
            count += 1
            print(str1)
            print(cropdata.shape)
            print(startx, starty)
            Train.write_img(os.path.join(rsbs_dir, str1), proj, CropGeoTrans, cropdata)  # 写数据

            # starty += int( (Train.im_height - sampsize) / (sampnum - 1) )
            starty += int(sampsize)
        # startx += int((Train.im_width - sampsize) / (sampnum - 1))
        startx += int(sampsize)


