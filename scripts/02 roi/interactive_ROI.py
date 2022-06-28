
# import libraries
import os.path
import re
import matplotlib as mpl
import pandas as pd
from PIL import Image
from roipoly import RoiPoly
import glob2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.path import Path as MplPath

mpl.use('Qt5Agg')  # matplotlib backend for windows

# initialize global variables
start_img_ind = 0  # starting image index
curr_poly_verts = None  # a list of  coordinates from a current ROI selection
curr_mask = None  # current mask
img_display = None  # matplotlib fig
img_display_axis = None  # matplotliib axis

# matplotlib buttons
# For these buttons to remain responsive, references must be kept
next_button = None
prev_button = None
restart_masking_button = None
finish_masking_button = None
confirm_button = None

my_roi = RoiPoly(color='k', show_fig=False)
# plot width and height
w = 6
h = 6


class ImageFile:
    """ Image File class to save file path, file name, date, mask_id"""

    def __init__(self, filename):
        self.path = filename
        self.image_name = filename.split("\\")[-1]
        self.date = self.get_date()
        self.mm, self.dd, self.yy = self.date.split("/")
        self.mask_id = None

    def get_date(self):
        """
        extracts date pattern (MM/DD/YY) from file name (eg. Hbwtr_w3_20200315_115918.JPG)
        :return: date
        """
        date_pattern = "\d{8}"  # eg 12-12-2020
        date = re.search(date_pattern, self.path).group(0)
        dd, mm, yy = date[-2:], date[-4:-2], date[-8:-4]
        date = mm + '/' + dd + '/' + yy
        return date

    def get_water_year(self):
        """
        extracts water year from dates
        """
        if self.mm >= "10" or self.mm <= "12":
            return int(self.yy[-2:]) + 1
        return int(self.yy[-2:])

    def read_img_orig(self):
        """
        reads image path and returns original image(np.array)
        """
        return np.asarray(Image.open(self.path))

    def read_img_sliced(self):
        """
        reads image path and returns sliced image(np.array) for faster display
        select every other row and columns and return sliced image
        """
        img = self.read_img_orig()
        return img[::2, ::2]


class CallBack:
    """
    Class that allows sliding through images and display original images and masked images
    """
    index = 0  # this holds the current index of image

    def next(self, event):
        """
        :param event: event callback for matplotlib button
        Slide to the next image in folder and display it
        """
        self.index += 1
        if not self.index_in_range():
            print("Reached End of Folder")
            self.index -= 1
            return
        im = self.get_masked_img()
        img_display.set_data(im)
        img_display_axis.set_title(
            "Click next or draw new ROI for Date: {}".format(image_file_list[self.index].get_date()))
        plt.draw()

    def prev(self, event):
        """
        :param event: event callback for matplotlib button
        Slide to the previous image in folder and display it
        """
        self.index -= 1
        if not self.index_in_range():
            print("Reached Start of Folder")
            self.index += 1
            return

        im = self.get_masked_img()
        img_display.set_data(im)
        img_display_axis.set_title(
            "Click next or draw new ROI for Date: {}".format(image_file_list[self.index].get_date()))
        plt.draw()

    def index_in_range(self):
        """
        Check if the index is within range of image_file_list
        """
        curr_ind = self.index
        if curr_ind < 0 or curr_ind >= len(image_file_list):
            return False
        return True

    def get_masked_img(self):
        """
        Apply mask from poly_verts_list and return masked image
        """
        if self.index_in_range():
            curr_obj = image_file_list[self.index]
            im = curr_obj.read_img_sliced().copy()
            im_mask = get_mask_poly_verts(im, poly_verts_list[self.index])
            return apply_mask(im, im_mask)
        print("OUT OF RANGE")


def start_roi_selection(start_img_ind):
    """
    :param start_img_ind: start index
    :return: curr_mask, confirm_button
    Displays image of start_index, allows user to select ROI and confirm selection
    """

    global img_display, img_display_axis, curr_mask, my_roi, curr_mask, curr_poly_verts
    show_first_image(start_img_ind)

    # pop up roi window
    my_roi = RoiPoly(color='r', close_fig=False)
    plt.close(my_roi.fig)

    # create a mask using ROI selected by user
    copy_img = image_file_list[start_img_ind].read_img_sliced().copy()
    curr_mask, curr_poly_verts = my_roi.get_mask(copy_img)
    copy_img = apply_mask(copy_img, curr_mask)
    # display image with roi mask
    fg = plt.gcf()
    fg.subplots_adjust(left=0.3, bottom=0.25)
    fg.set_size_inches(w, h, forward=True)

    # change the content of image on image display axis
    img_display_axis = plt.gca()
    img_display_axis.set_title("Confirm ROI? Date: {}".format(image_file_list[start_img_ind].date))
    img_display = img_display_axis.imshow(copy_img)

    # create confirm mask button
    confirm_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    confirm_button = Button(confirm_ax, 'Confirm')
    confirm_button.on_clicked(confirm_roi)
    confirm_button._button = confirm_button

    return curr_mask, confirm_button


def show_first_image(start_index):
    """display the very first image"""
    global img_display, img_display_axis
    img_display_axis = plt.gca()
    img_display_axis.set_title("Select ROI  Date: {}".format(image_file_list[start_index].date))
    img_display = img_display_axis.imshow(image_file_list[start_index].read_img_sliced())


def confirm_roi(event):
    """
    Callback event for confirm button
    If users select ROI and hit confirm, save the poly_verts and apply it to the rest of images
    Then, start showing next and previous buttons
    """

    # save current mask's poly_verts starting from start_img_ind index
    for i in range(start_img_ind, len(image_file_list)):
        poly_verts_list[i] = curr_poly_verts

    img_display_axis.set_title("Choose next or redraw ROI for {}".format(image_file_list[start_img_ind].date))
    # button to show next and prev masked images
    _ = show_next_prev()


def show_next_prev():
    """
    Create next, previous, restart and finish buttons
    return: references for all these buttons
    """
    global next_button, prev_button, restart_masking_button, finish_masking_button

    ax_prev, ax_next = plt.axes([0.7, 0.05, 0.1, 0.075]), plt.axes([0.81, 0.05, 0.1, 0.075])
    prev_button, next_button = Button(ax_prev, 'Previous'), Button(ax_next, 'Next')
    prev_button.on_clicked(callback.prev)
    next_button.on_clicked(callback.next)
    restart_masking_ax, finish_masking_ax = plt.axes([0.1, 0.05, 0.3, 0.075]), plt.axes([0.1, 0.15, 0.3, 0.075])
    restart_masking_button = Button(restart_masking_ax, "Restart masking")
    finish_masking_button = Button(finish_masking_ax, "Finish masking")
    restart_masking_button.on_clicked(restart_masking)
    finish_masking_button.on_clicked(finish_masking)
    return next_button, prev_button, restart_masking_button, finish_masking_button


def restart_masking(event):
    """
    :param event: Callback event when user restarts masking
    Clears plot and begin a new ROI masking session
    """
    global my_roi, confirm_button, restart_masking_button, img_display, img_display_axis, start_img_ind, curr_mask, curr_poly_verts

    # clear plot
    plt.clf()
    # create new plot
    fg_2 = plt.gcf()
    fg_2.subplots_adjust(left=0.3, bottom=0.25)
    fg_2.set_size_inches(w, h, forward=True)

    # change the content of image on curr axis
    img_display_axis = plt.gca()
    if not callback.index_in_range():
        print("OUT OF RANGE")
        return
    curr_ind = callback.index
    curr_obj = image_file_list[curr_ind]
    img_display_axis.set_title("Confirm ROI? Date: {}".format(curr_obj.get_date()))
    img_display = img_display_axis.imshow(curr_obj.read_img_sliced())
    # display new ROI pop up
    my_roi = RoiPoly(color='r', close_fig=False)

    # wait until the user finishes selecting ROI
    while not my_roi.finished_clicking:
        plt.pause(0.01)

    # mask current image and display
    cp = curr_obj.read_img_sliced().copy()
    curr_mask, curr_poly_verts = my_roi.get_mask(cp)
    cp = apply_mask(cp, curr_mask)
    start_img_ind = curr_ind
    img_display = img_display_axis.imshow(cp)

    # Create a confirm mask button for new session
    confirm_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    confirm_button = Button(confirm_ax, 'Confirm')
    confirm_button.on_clicked(confirm_roi)
    confirm_button._button = confirm_button

    # Create a restart mask button for new session
    restart_masking_ax = plt.axes([0.1, 0.05, 0.3, 0.075])
    restart_masking_button = Button(restart_masking_ax, "Restart masking")
    restart_masking_button.on_clicked(restart_masking)

    plt.draw()


def finish_masking(event):
    """
        :param event: Callback event for finish masking button
        save dataframe linking mask_id to actual mask  (mask_df)
        create water year folders
        save dataframe linking date to mask_id (date_mask_df)
        apply masks on original images and save them in their respective water year folders
        close plot
    """
    global poly_verts_list

    # collect unique poly_verts and assign mask_ids to them
    poly_verts_unique_list = []
    mask_id = -1
    for i in range(len(poly_verts_list)):
        if mask_id == -1 or poly_verts_list[i - 1] != poly_verts_list[i]:
            mask_id += 1
            poly_verts_unique_list.append(poly_verts_list[i])
        # assign mask_ids to all ImageFile objects
        image_file_list[i].mask_id = mask_id

    # Save a mask_df data frame with columns mask_id-> actual mask(poly_verts) and save it
    mask_df = pd.DataFrame(list(zip(poly_verts_unique_list)), columns=["poly_verts"])
    mask_df.index.name = "mask_id"
    mask_df_dst = folder_path + "/" + "mask_df.csv"
    mask_df.to_csv(mask_df_dst)
    # print(mask_df.head())
    print("mask_df saved to this folder {}".format(folder_path))

    # collect all information from ImageFile Objects
    image_file_info = pd.DataFrame(
        [(i.date, i.mask_id, i.path, i.get_water_year(), ind, poly_verts_list[ind]) for ind, i in
         enumerate(image_file_list)],
        columns=["Date", "mask_id", "file_path", "WY", "list_index", "poly_verts"])
    image_file_info.set_index("WY", inplace=True)
    # print(image_file_info.head())

    # list of water years
    list_wy = list(image_file_info.index.unique())
    print("STARTED SAVING")
    print("Saving takes about 1 second per an image file")

    for water_year in list_wy:
        # Create folders for each water year
        wy_dest = folder_path + "/" + "WY" + str(water_year)
        if not os.path.exists(wy_dest):
            os.mkdir(wy_dest)
        # loop through index of image_file_objects and save original images with their mask
        df = image_file_info[image_file_info.index == water_year]

        # save a date_mask dataframe with columns date-> mask_id -> file name
        date_mask_df = df.reset_index()[["Date", "mask_id"]].set_index("Date")
        date_mask_df.to_csv(wy_dest + "/" + "date_mask.csv")
        print("date_mask.csv saved to the folder {}".format(wy_dest))

        # mask images within a selected water_year
        for index, row in df.iterrows():
            folder_index = row["list_index"]
            curr_file_path = row["file_path"]

            # save masked image to WY destination
            curr_obj = image_file_list[folder_index]
            curr_file_name = curr_obj.image_name
            curr_original_image = curr_obj.read_img_orig().copy()
            curr_original_mask = get_mask_poly_verts(curr_original_image, poly_verts_list[folder_index],
                                                     on_original=True)
            curr_original_image = apply_mask(curr_original_image, curr_original_mask)
            curr_img_save_dest = wy_dest + "/" + curr_file_name

            # save curr_original_image
            Image.fromarray(np.array(curr_original_image)).save(curr_img_save_dest)

    print("FINISHED SAVING")
    plt.close()


def apply_mask(im, mask):
    """
    :param im: image np.array
    :param mask: np.array of the same size to mask
    :return: return masked image
    """
    im[mask != 1] = 0
    return im


def get_mask_poly_verts(image, poly_verts, on_original=False):
    """
    :param image: np.array of image
    :param poly_verts: list of  coordinates from ROI selection
    :param on_original: boolean indicating if the mask is applied to original or sliced image
    :return: image mask that can be applied to image
    """
    if len(np.shape(image)) == 3:
        ny, nx, nz = np.shape(image)
    else:
        ny, nx = np.shape(image)
    # if mask is applied to original, each coordinate is multiplied by 2
    if on_original:
        poly_verts = [(2 * x, 2 * y) for (x, y) in poly_verts]

    x, y = np.meshgrid(np.arange(nx), np.arange(ny))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x, y)).T
    roi_path = MplPath(poly_verts)
    mask = roi_path.contains_points(points).reshape((ny, nx))
    return mask


# Sample Image Local Watershed Folder (eg. W1)
folder_path = r"C:\Users\Dell\Downloads\W1"

# Read paths to all the images into image_folder list
image_folder = glob2.glob(folder_path + "/*")

# Loop over all image files, Create ImageFile objects and save to image_file_list
image_file_list = []
for filename in image_folder[:50]:
    filetype = filename[-4:]
    # Check if the file name ends with ".JPG" or ".jpg"
    if filetype.lower() != ".jpg":
        continue
    curr_IF = ImageFile(filename)
    image_file_list.append(curr_IF)

# sort by year, then month, then day
image_file_list = np.array(sorted(image_file_list, key=lambda x: (x.yy, x.mm, x.dd)))

# initialize CallBack class
callback = CallBack()

# create poly_verts_list
poly_verts_list = [0] * len(image_file_list)

# first plot
fg = plt.gcf()
fg.subplots_adjust(left=0.35, bottom=0.25)
fg.set_size_inches(w, h, forward=True)

# collect roi from image + confirm button
select_roi_ret = start_roi_selection(start_img_ind)

plt.show()
