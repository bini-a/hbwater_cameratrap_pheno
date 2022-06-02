#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 13:58:43 2022

@author: hectorontiveros
"""


%matplotlib auto
import logging
import numpy as np
import matplotlib

from matplotlib import pyplot as plt
import cv2
from roipoly import roipoly
from PIL import Image
import os 
from PIL import ImageFilter
import imageio
import cv2
import skimage
import numpy as np

from skimage.viewer import ImageViewer
import pandas as pd
from datetime import datetime

logging.basicConfig(format='%(levelname)s ''%(processName)-10s : %(asctime)s '
                           '%(module)s.%(funcName)s:%(lineno)s %(message)s',
                    level=logging.INFO)

# Create and format to obtain pixels
im = cv2.imread(r"C:\Users\Dell\Downloads\Hbwtr_w3_20200313_115919.JPG")
# change coloring to RGB scale
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
img = np.array(im)
# show original image
plt.imshow(img)

# pop up roi window
my_roi = roipoly(color = 'r')
my_roi.display_roi()
# print("after display")

# get mask array
mask = my_roi.get_mask(img)
# print("Mask", my_mask)

# get coordinates of the mask
cords = my_roi.get_roi_coordinates()
# print("cords", cords)

# copy image
image = im.copy()
# mask the image using indexing from mask array
image[mask!=1]=0
# show masked image
plt.imshow(image)

