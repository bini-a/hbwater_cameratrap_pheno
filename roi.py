#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 13:58:43 2022

@author: hectorontiveros
"""

%matplotlib auto
import logging
import numpy as np
from matplotlib import pyplot as plt
import cv2
from roipoly import roipoly
from PIL import Image

logging.basicConfig(format='%(levelname)s ''%(processName)-10s : %(asctime)s '
                           '%(module)s.%(funcName)s:%(lineno)s %(message)s',
                    level=logging.INFO)

# Create and format to obtain pixels
im = cv2.imread("/Users/hectorontiveros/Desktop/fwsp.jpg")
im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
img = np.array(im)
plt.imshow(img)

print("bigb")

my_roi = roipoly(color = 'r')
my_roi.display_roi()
mask = my_roi.get_mask(img)
cords = my_roi.get_roi_coordinates()
mask1 = np.array(mask)
#image = cv2.add(img, img, mask =mask1)


plt.imshow(mask)
#print(cords)