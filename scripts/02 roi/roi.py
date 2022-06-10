#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 13:58:43 2022

@author: hectorontiveros
"""
import matplotlib as mpl

mpl.use('Qt5Agg')  # or can use 'TkAgg', whatever you have/prefer

import logging
import numpy as np
import matplotlib.pyplot as plt
import cv2
from roipoly import roipoly
from PIL import Image
from PIL import ImageFilter
import imageio
from skimage.viewer import ImageViewer
import pandas as pd
from datetime import datetime

logging.basicConfig(format='%(levelname)s ''%(processName)-10s : %(asctime)s '
                           '%(module)s.%(funcName)s:%(lineno)s %(message)s',
                    level=logging.INFO)


# Create and format to obtain pixels
im = cv2.imread(r"/Users/henrysun_1/Downloads/Test/07170143.JPG")
# change coloring to RGB scale
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
img = np.array(im)
# show original image
plt.imshow(img)

# pop up roi window
my_roi = roipoly(color='r')
my_roi.display_roi()
# print("after display")

# get mask array
print(np.shape(img))
img = img[:, :, 0]
# Converts image to 2d array - necessary on Henry's mac where the 3d image threw a ValueError
# with too many layers to unpack

print(np.shape(img))
mask = my_roi.get_mask(img)
# print("Mask", my_mask)

#
# # get coordinates of the mask
# cords = my_roi.get_roi_coordinates()
# # print("cords", cords)
'''
The above code did not work on Henry's mac (AttributeError) and was not resolved
'''


# copy image
image = im.copy()
# mask the image using indexing from mask array
image[mask != 1] = 0
# # show masked image
plt.imshow(image)
plt.show()
