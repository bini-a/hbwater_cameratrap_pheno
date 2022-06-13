# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 14:46:12 2022

@author: Dell
"""

import logging

logger = logging.getLogger(__name__)
import os
import matplotlib as mpl

mpl.use('Qt5Agg')  # backend for windows

# TODO  confrim button-overlaying next button, change date extraction using regular expression, last and first item of folder

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, RadioButtons, CheckButtons
import cv2
from roipoly import RoiPoly
import glob2

import sys
import logging
import warnings

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.widgets import Button

#### sample image local folder
image_folder = glob2.glob(r"C:/Users/Dell/Downloads/W1/*")
date_list = []
for date in image_folder:
    date_list.append(date[-19:-11])
f_date = date_list[0]
# print(f_date)
# print("Date List", date_list)
# print("Image Folder ", image_folder)
"""Draw polygon regions of interest (ROIs) in matplotlib images,
similar to Matlab's roipoly function.
"""

import sys
import logging
import warnings

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.widgets import Button

logger = logging.getLogger(__name__)

warnings.simplefilter('always', DeprecationWarning)

masked_images_list = None
start_img_ind = 0
curr_mask = None
curr_masked_img_axis = None
curr_masked_img = None
bnext = None
bprev = None
restart_masking_button = None
my_roi = RoiPoly(color='r', show_fig=False)
confirm_button = None


class Index:
    ind = 0

    def get_curr_index(self):
        return self.ind

    def next(self, event):
        self.ind += 1
        # ax.clear()
        # ax.imshow(li[self.ind])
        curr_masked_img_axis.set_data(masked_images_list[self.ind])
        curr_masked_img.set_title("Next selected, click next or draw new ROI for Date: {}".format(date_list[self.ind]))
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        # print("EQUAL?", image_folder==masked_images_list)
        curr_masked_img_axis.set_data(masked_images_list[self.ind])
        curr_masked_img.set_title(
            "Previous selected, click next or draw new ROI for Date: {}".format(date_list[self.ind]))
        print(self.get_curr_index())
        plt.draw()

    # def restart(self,event):
    #     plt.clf()
    #     curr_masked_img = plt.gca()
    #     curr_masked_img.set_title("Confirm ROI?")
    #     curr_masked_img_axis = curr_masked_img.imshow(image_folder[self.ind])
    #     # curr_masked_img_axis.set_data(image_folder[self.ind])
    #     # plt.draw()
    def show_original(self, event):
        print("Showing original + ROI line")

        curr_masked_img_axis.set_data(image_folder[self.ind])
        plt.draw()


def read_img(path):
    im = cv2.imread(path)
    # change coloring to RGB scale
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    img = np.array(im)
    return img[::2, ::2]


def mask_items_folder():
    # print("2. EQUAL?", image_folder[0] == masked_images_list[0])

    # print("Started masking")
    # print("mask_length",len(masked_images_list))
    for i in range(start_img_ind, len(masked_images_list)):
        curr_image = image_folder[i].copy()
        curr_image[curr_mask != 1] = 0

        masked_images_list[i] = curr_image
    # print("Finished masking starting from index", start_img_ind)
    # print("3. EQUAL?", image_folder==masked_images_list)


def make_new():
    global my_roi, confirm_button, curr_masked_img_axis, curr_masked_img, curr_mask, start_img_ind, restart_masking_button

    fg_2 = plt.gcf()
    fg_2.subplots_adjust(left=0.3, bottom=0.25)
    curr_ind = callback.get_curr_index()
    # change the content of image on curr axis
    curr_masked_img = plt.gca()
    curr_masked_img.set_title("Confirm ROI? Date: {}".format(date_list[curr_ind]))
    curr_masked_img_axis = curr_masked_img.imshow(image_folder[curr_ind])
    my_roi_2 = RoiPoly(color="r", close_fig=False)
    ### wait 5 or double click
    # plt.pause(5)
    while not my_roi_2.dbl_clicked:
        plt.pause(0.01)
    # my_roi_2.display_roi()
    # plt.close(my_roi_2.fig)
    print(my_roi_2.x, my_roi_2.y)
    #
    curr_mask = my_roi_2.get_mask(image_folder[curr_ind])
    cp = image_folder[curr_ind].copy()
    cp[curr_mask != 1] = 0
    # c_img = plt.gca()
    start_img_ind = curr_ind
    curr_masked_img_axis = curr_masked_img.imshow(cp)

    # confirm mask button
    confirm_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    confirm_button = Button(confirm_ax, 'Confirm')
    confirm_button.on_clicked(confirm_roi)
    confirm_button._button = confirm_button

    restart_masking_ax = plt.axes([0.1, 0.05, 0.3, 0.075])
    restart_masking_button = Button(restart_masking_ax, "Restart masking")
    restart_masking_button.on_clicked(restart_masking)

    plt.draw()
    return confirm_button


def restart_masking(event):
    print("Restart started")
    # fg = plt.figure()
    curr_ind = callback.get_curr_index()
    print("Calling select_roi")
    global curr_masked_img_axis, curr_masked_img, curr_mask
    plt.clf()
    _ = make_new()


def show_next_prev():
    global bnext, bprev, restart_masking_button
    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)
    restart_masking_ax = plt.axes([0.1, 0.05, 0.3, 0.075])
    restart_masking_button = Button(restart_masking_ax, "Restart masking")
    restart_masking_button.on_clicked(restart_masking)
    return bnext, bprev, restart_masking_button


def confirm_roi(event):
    print("Confirmed")

    # mask all images starting from start_img_ind index
    mask_items_folder()

    # plt.cla()
    curr_masked_img.set_title("Choose next or redraw ROI for {}".format(f_date))
    # button to show next and prev masked images
    _ = show_next_prev()


def show_first_image(start_index):
    # display first image with roi mask

    global curr_masked_img_axis, curr_masked_img
    curr_masked_img = plt.gca()

    curr_masked_img.set_title("Select ROI  Date: {}".format(f_date))
    curr_masked_img_axis = curr_masked_img.imshow(image_folder[start_index])
    print("show first image END")


def select_roi(start_img_ind):
    global curr_masked_img_axis, curr_masked_img, curr_mask, image_folder, masked_images_list, my_roi, curr_mask
    print("show first image start")
    show_first_image(start_img_ind)
    # pop up roi window
    my_roi = RoiPoly(color='r', close_fig=False)
    print("Trying to display roi")
    # my_roi.display_roi()
    print("End displaying roi")
    plt.close(my_roi.fig)
    # curr_masked_img = plt.gca()
    # curr_masked_img.set_title("Confirm ROI? Date: {}".format(f_date))
    # curr_masked_img_axis = curr_masked_img.imshow(image_folder[start_img_ind])
    curr_mask = my_roi.get_mask(image_folder[start_img_ind])
    copy_img = image_folder[start_img_ind].copy()
    copy_img[curr_mask != 1] = 0
    # display first image with roi mask
    fg = plt.gcf()
    fg.subplots_adjust(left=0.3, bottom=0.25)

    # change the content of image on curr axis
    curr_masked_img = plt.gca()
    curr_masked_img.set_title("Confirm ROI? Date: {}".format(f_date))
    curr_masked_img_axis = curr_masked_img.imshow(copy_img)

    # confirm mask button
    confirm_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    confirm_button = Button(confirm_ax, 'Confirm')
    confirm_button.on_clicked(confirm_roi)
    confirm_button._button = confirm_button

    return curr_mask, confirm_button


callback = Index()

# read all images
image_folder = [read_img(im) for im in image_folder[:10]]

masked_images_list = image_folder.copy()
fg = plt.gcf()
fg.subplots_adjust(left=0.35, bottom=0.25)
# collect roi from image + confirm button
select_roi_ret = select_roi(start_img_ind)
_ = select_roi_ret[0]

plt.show()
