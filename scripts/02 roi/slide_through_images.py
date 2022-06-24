import os.path
import re
import matplotlib as mpl
import pandas as pd
from PIL import Image
mpl.use('Qt5Agg')  # backend for windows
from roipoly import RoiPoly
import glob2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.path import Path as MplPath


#### sample image local folder
folder_path = r"C:\Users\Dell\Downloads\W1"
image_folder = glob2.glob(folder_path + "/*")
# print(image_folder)
original_image_folder = None
date_list = []
# date_pattern = "\d{8}"  # eg 12-12-2020
date_dict= {}

class ImageFile:

    """ GET ORIGINAL FILE PATH, DATE"""

    def __init__(self, filename):
        self.path = filename
        self.image_name = filename.split("\\")[-1]
        self.date = self.get_date()
        self.mm, self.dd, self.yy = self.date.split("/")
        self.mask_id = None
        # print("TYPE of mm", self.mm,self.yy, self.get_water_year())

        # self.original_image = self.read_img_orig()
        # self.sliced_image = self.read_img_sliced()
    def get_date(self):
        date_pattern = "\d{8}"  # eg 12-12-2020
        # print(self.path)
        date = re.search(date_pattern, self.path).group(0)
        dd, mm, yy = date[-2:], date[-4:-2],date[-8:-4]
        date= mm + '/' + dd + '/' + yy
        return date
    def get_water_year(self):
        if self.mm>="10" or self.mm<="12":
            return int(self.yy[-2:]) +1
        else:
            return int(self.yy[-2:])
    def file_path(self):
        return self.path
    def read_img_orig(self):
        img = Image.open(self.path)
        img = np.asarray(img)
        return img
    def read_img_sliced(self):
        img = self.read_img_orig()
        return img[::2, ::2]

def read_img(path, orig = False):
    # im = cv2.imread(path)
    # change coloring to RGB scale
    # im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    img = Image.open(path)
    img = np.asarray(img)
    return img[::2, ::2]

image_file_object_list = []
# for filename in image_folder[:10]:
s = image_folder[:10] + image_folder[-10:]
for filename in  s:
    filetype = filename[-4:]
    if filetype.lower() != ".jpg":
        continue
    curr_IF = ImageFile(filename)
    image_file_object_list.append(curr_IF)

# sort by year, then month, then day
image_file_object_list = sorted(image_file_object_list, key = lambda x:(x.yy, x.mm, x.dd))
image_file_object_list = np.array(image_file_object_list)

masked_images_list = None
curr_poly_verts_list = None
original_masked_images_list= None
start_img_ind = 0
curr_poly_verts = None
curr_mask = None
curr_masked_img_axis = None
curr_masked_img = None
bnext = None
bprev = None
restart_masking_button = None
my_roi = RoiPoly(color='k', show_fig=False)
confirm_button = None
poly_verts_list = None
# plot width and height
w = 6
h = 6

def get_mask_poly_verts(image, poly_verts, on_original=False):
    if len(np.shape(image)) == 3:
        ny, nx, nz = np.shape(image)
    else:
        ny, nx = np.shape(image)
    if on_original:
        poly_verts = [(2*x, 2*y) for (x,y) in poly_verts]
    x, y = np.meshgrid(np.arange(nx), np.arange(ny))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x, y)).T
    roi_path = MplPath(poly_verts)
    mask = roi_path.contains_points(points).reshape((ny, nx))
    return mask
class Index:
    ind = 0
    # def get_curr_index(self):
    #     return self.ind
    def index_in_range(self):
        curr_ind = self.ind
        if curr_ind<0 or curr_ind>= len(image_folder):
            return False
        return True
    def get_masked_img(self):
        curr_obj = image_file_object_list[self.ind]
        im = curr_obj.read_img_sliced().copy()
        im_mask = get_mask_poly_verts(im, poly_verts_list[self.ind])
        im[im_mask != 1] = 0
        return im
    def next(self, event):
        # print(self.index_in_range())
        self.ind += 1

        if not self.index_in_range():
            self.ind-=1
            return
        im = self.get_masked_img()
        curr_masked_img_axis.set_data(im)
        curr_masked_img.set_title("Click next or draw new ROI for Date: {}".format(image_file_object_list[self.ind].get_date()))
        plt.draw()

    def prev(self, event):
        self.ind -= 1
        if not self.index_in_range():
            self.ind+=1
            return
        im = self.get_masked_img()
        curr_masked_img_axis.set_data(im)
        curr_masked_img.set_title("Click next or draw new ROI for Date: {}".format(image_file_object_list[self.ind].get_date()))
        plt.draw()


def mask_items_folder():
    for i in range(start_img_ind, len(image_file_object_list)):
        # curr_image = image_file_object_list[i].read_img_sliced().copy()
        # curr_image[curr_mask != 1] = 0
        # masked_images_list[i] = curr_image
        poly_verts_list[i] = curr_poly_verts


def make_new():
    global my_roi, confirm_button, curr_masked_img_axis, curr_masked_img, curr_mask, start_img_ind, restart_masking_button, curr_poly_verts
    fg_2 = plt.gcf()
    fg_2.subplots_adjust(left=0.3, bottom=0.25)
    fg_2.set_size_inches(w, h, forward=True)

    curr_ind = callback.ind
    # change the content of image on curr axis
    curr_masked_img = plt.gca()
    curr_obj = image_file_object_list[curr_ind]
    curr_masked_img.set_title("Confirm ROI? Date: {}".format(curr_obj.get_date()))
    curr_masked_img_axis = curr_masked_img.imshow(curr_obj.read_img_sliced())
    my_roi = RoiPoly(color='r', close_fig=False)

    while not my_roi.dbl_clicked:
        plt.pause(0.01)

    # print(my_roi_2.x, my_roi_2.y)

    cp = curr_obj.read_img_sliced().copy()
    curr_mask, curr_poly_verts = my_roi.get_mask(cp)
    cp[curr_mask != 1] = 0
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
    # print("Restart started")
    curr_ind = callback.ind
    # print("Calling select_roi")
    plt.clf()
    _ = make_new()


def finish_masking(event):
    global poly_verts_list
    # save all data/ close plot

    poly_verts_maskID_list = [0]*len(poly_verts_list)
    poly_verts_unique_list = []
    mask_id = -1
    for i in range(len(poly_verts_list)):
        if mask_id==-1 or poly_verts_list[i-1]!=poly_verts_list[i]:
            mask_id+=1
            poly_verts_unique_list.append(poly_verts_list[i])
        poly_verts_maskID_list[i]= mask_id
        image_file_object_list[i].mask_id = mask_id


    print(poly_verts_list)
    print(poly_verts_unique_list)
    print(poly_verts_maskID_list)
    print([i.mask_id for i in image_file_object_list]==poly_verts_maskID_list)
    # # mask_id -> actual mask
    mask_df = pd.DataFrame(list(zip(poly_verts_unique_list)), columns = ["mask"])
    mask_df.index.name = "mask_id"
    print(mask_df)
    # save mask df
    mask_df_dst = folder_path + "/" + "mask_df.csv"
    # mask_df.to_csv(mask_df_dst)

    # date -> mask_id -> file name

    image_mask_id_df = pd.DataFrame([(i.date, i.mask_id, i.file_path(), i.get_water_year(),ind, poly_verts_list[ind] ) for ind, i in enumerate(image_file_object_list)],
                                    columns=["Date", "mask_id","file_path", "WY","list_index", "poly_verts"])
    image_mask_id_df[["mask_id","poly_verts"]].drop_duplicates(subset=["mask_id"]).to_csv(folder_path+"/"+"image_mask.csv", index=False)
    image_mask_id_df.set_index("Date", inplace=True)
    print(len(image_file_object_list))
    print(image_mask_id_df.head())
    x = image_mask_id_df.reset_index()[["mask_id","poly_verts"]]
    copy_df = image_mask_id_df.reset_index().copy()
    copy_df.set_index("WY", inplace=True)
    print(copy_df.head())
    # image_mask_id_dst = folder_path + "/" + "copy_df.csv"
    # copy_df.to_csv(image_mask_id_dst)

    list_wy = list(copy_df.index.unique())
    print("START SAVING")
    for water_year in list_wy:
        wy_dest = folder_path + "/" + "WY" + str(water_year)

        if not os.path.exists(wy_dest):
            os.mkdir(wy_dest)
        # destination created loop through index of image_file_objects and save original images with original mask
        df = copy_df[copy_df.index == water_year]
        date_mask_df = df.reset_index()[["Date","mask_id"]]
        date_mask_df.to_csv(wy_dest+"/"+"date_mask.csv")
        for index, row in df.iterrows():
            wy_i = row["list_index"]
            curr_file_path = row["file_path"]
            # save to dest original
            curr_imageFile_object = image_file_object_list[wy_i]
            curr_file_name = curr_imageFile_object.image_name
            curr_original_image = curr_imageFile_object.read_img_orig().copy()
            curr_original_mask = get_mask_poly_verts(curr_original_image, poly_verts_list[wy_i], on_original=True)
            curr_original_image[curr_original_mask!=1] = 0
            curr_img_save_dest = wy_dest+"/"+curr_file_name
            # save curr_original_image
            Image.fromarray(np.array(curr_original_image)).save(curr_img_save_dest)
    print("FINISHED SAVING")
    plt.close()


def show_next_prev():
    global bnext, bprev, restart_masking_button, finish_masking_button

    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)
    restart_masking_ax = plt.axes([0.1, 0.05, 0.3, 0.075])
    restart_masking_button = Button(restart_masking_ax, "Restart masking")
    restart_masking_button.on_clicked(restart_masking)
    finish_masking_ax = plt.axes([0.1, 0.15, 0.3, 0.075])
    finish_masking_button = Button(finish_masking_ax, "Finish masking")
    finish_masking_button.on_clicked(finish_masking)
    return bnext, bprev, restart_masking_button, finish_masking_button


def confirm_roi(event):
    # print("Confirmed")

    # mask all images starting from start_img_ind index
    mask_items_folder()

    curr_masked_img.set_title("Choose next or redraw ROI for {}".format(image_file_object_list[start_img_ind].date))
    # button to show next and prev masked images
    _ = show_next_prev()


def show_first_image(start_index):
    # display first image with roi mask

    global curr_masked_img_axis, curr_masked_img
    curr_masked_img = plt.gca()

    curr_masked_img.set_title("Select ROI  Date: {}".format(image_file_object_list[start_index].date))
    curr_masked_img_axis = curr_masked_img.imshow(image_file_object_list[start_index].read_img_sliced())
    # print("show first image END")


def select_roi(start_img_ind):

    global curr_masked_img_axis, curr_masked_img, curr_mask, image_folder, masked_images_list, my_roi, curr_mask, curr_poly_verts
    # print("show first image start")
    show_first_image(start_img_ind)
    # pop up roi window
    my_roi = RoiPoly(color='r', close_fig=False)
    # my_roi.display_roi()
    # print("End displaying roi")
    plt.close(my_roi.fig)
    copy_img = image_file_object_list[start_img_ind].read_img_sliced().copy()
    curr_mask, curr_poly_verts = my_roi.get_mask(copy_img)
    copy_img[curr_mask != 1] = 0
    # display first image with roi mask
    fg = plt.gcf()
    fg.subplots_adjust(left=0.3, bottom=0.25)
    fg.set_size_inches(w, h, forward=True)

    # change the content of image on curr axis
    curr_masked_img = plt.gca()
    curr_masked_img.set_title("Confirm ROI? Date: {}".format(image_file_object_list[start_img_ind].date))
    curr_masked_img_axis = curr_masked_img.imshow(copy_img)

    # confirm mask button
    confirm_ax = plt.axes([0.81, 0.05, 0.1, 0.075])
    confirm_button = Button(confirm_ax, 'Confirm')
    confirm_button.on_clicked(confirm_roi)
    confirm_button._button = confirm_button

    return curr_mask, confirm_button




# print("LEN", len(image_folder))
callback = Index()

# make masked images list
masked_images_list = [0]*len(image_file_object_list)
poly_verts_list = [0]*len(image_file_object_list)
original_masked_images_list = [0]*len(image_file_object_list)
# first plot
fg = plt.gcf()
fg.subplots_adjust(left=0.35, bottom=0.25)
fg.set_size_inches(w, h, forward=True)

# collect roi from image + confirm button
select_roi_ret = select_roi(start_img_ind)
plt.show()