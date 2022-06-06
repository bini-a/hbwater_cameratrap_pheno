# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:46:12 2022

@author: Dell
"""


%matplotlib auto

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons

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







fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

def read_img(path):
    im = cv2.imread(path)
    # change coloring to RGB scale

    # im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    img = np.array(im)
    
    return img[::2,::2]

#### sample image local files
img1  = read_img(r"C:\Users\Dell\Downloads\Hbwtr_w3_20200313_115919.JPG")
img2 = read_img(r"C:\Users\Dell\Downloads\Hbwtr_w3_20200315_115918.JPG")
img3 = read_img(r"C:\Users\Dell\Downloads\11050468.JPG")

plt.subplots_adjust(left = 0.3, bottom = 0.25)

li = [img1, img2, img3]

first_img = ax.imshow(li[0])


class Index:
    ind = 0

    def next(self, event):
        self.ind += 1

        # ax.clear()
        # ax.imshow(li[self.ind])
        
        first_img.set_data(li[self.ind])

        plt.draw()

    def prev(self, event):
        self.ind -= 1
        first_img.set_data(li[self.ind])

        plt.draw()

callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Next')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Previous')
bprev.on_clicked(callback.prev)

plt.show()