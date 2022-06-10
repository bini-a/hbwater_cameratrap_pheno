# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:46:12 2022

@author: Dell
"""

import matplotlib as mpl
mpl.use('Qt5Agg')  # backend for windows
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons
import cv2
from roipoly import roipoly
from PIL import Image

#### sample image local folder
import glob
image_folder = glob.glob(r"C:/Users/Dell/Downloads/W1/*")
from matplotlib.widgets import Button, RadioButtons, CheckButtons

fig, ax = plt.subplots()
# plt.subplots_adjust(bottom=0.2)
masked_images_list = []
first_masked_img_axis = None
first_masked_img = None
bnext = None
bprev= None
class Index:
    ind = 0
    def next(self, event):
        self.ind += 1

        # ax.clear()
        # ax.imshow(li[self.ind])

        first_masked_img_axis.set_data(masked_images_list[self.ind])

        plt.draw()

    def prev(self, event):
        self.ind -= 1
        first_masked_img_axis.set_data(masked_images_list[self.ind])

        plt.draw()
def read_img(path):
    im = cv2.imread(path)
    # change coloring to RGB scale
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    img = np.array(im)
    return img[::2,::2]

def mask_items_folder(first_mask, start_img_ind):
    masked_images_list = image_folder[start_img_ind+1:]
    for i in range(len(masked_images_list)):
        masked_images_list[i][first_mask!=1]=0
    return masked_images_list
def show_next_prev():
    global bnext, bprev
    callback = Index()
    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)
    return bnext, bprev
def confirm_roi(event):
    print("Confirmed")
    # global masked_images_list
    print("masked_img", len(masked_images_list))
    # plt.cla()
    first_masked_img.set_title("Show Next images with ROI")

    show_next_prev()


    # fg = plt.gcf()
    # fg.subplots_adjust(left=0.3, bottom=0.25)
    # ax = plt.gca()
    # masked_first = ax.imshow(masked_images_list[5])

def select_roi(start_img_ind):
    global first_masked_img_axis, first_masked_img
    # pop up roi window
    my_roi = roipoly(color = 'r')
    my_roi.display_roi()
    first_mask = my_roi.get_mask(image_folder[start_img_ind])
    copy_img = image_folder[start_img_ind].copy()
    copy_img[first_mask!=1]=0
    # display first image with roi mask
    fg = plt.gcf()
    fg.subplots_adjust(left=0.3, bottom=0.25)
    first_masked_img = plt.gca()
    first_masked_img.set_title("Confirm ROI?")
    first_masked_img_axis = first_masked_img.imshow(copy_img)
    # mask all remaining images
    global masked_images_list
    masked_images_list = mask_items_folder(first_mask, start_img_ind)

    # confirm mask button
    confirm_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    confirm_button = Button(confirm_ax, 'C')
    confirm_button.on_clicked(confirm_roi)
    confirm_button._button = confirm_button

    return first_mask, confirm_button

# read all images
image_folder = [read_img(im) for im in image_folder[:10]]

# first image plot
plt.subplots_adjust(left = 0.3, bottom = 0.25)
ax.set_title("Select ROI")
first_display = ax.imshow(image_folder[1])

# collect roi from image + confirm button
select_roi_ret = select_roi(0)
first_mask = select_roi_ret[0]


# show all masked images


# callback = Index()
# axprev = plt.axes([0.7, 0., 0.1, 0.075])
# axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
# bnext = Button(axnext, 'Next')
# bnext.on_clicked(callback.next)
# bprev = Button(axprev, 'Previous')
# bprev.on_clicked(callback.prev)
# callback = Index()


# curr_axis = plt.gcf()
#
# curr_axis.imshow(image_folder[2])
# plt.draw()


# callback = Index()
# axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
# axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
# bnext = Button(axnext, 'Next')
# bnext.on_clicked(callback.next)
# bprev = Button(axprev, 'Previous')
# bprev.on_clicked(callback.prev)

plt.show()