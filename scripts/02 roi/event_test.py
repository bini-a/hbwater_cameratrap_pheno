%matplotlib auto
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import logging
from roipoly import RoiPoly
from PIL import Image
import os 
from PIL import ImageFilter
import imageio
import cv2
import skimage
import numpy as np


#plt.subplots_adjust(bottom=0.2)

logging.basicConfig(format='%(levelname)s ''%(processName)-10s : %(asctime)s '
                           '%(module)s.%(funcName)s:%(lineno)s %(message)s',
                    level=logging.INFO)

imgs = []
masked_imgs = []
for fp in (sorted(os.listdir("/Users/hectorontiveros/Desktop/WCTEST/"))):
    imgs.append(cv2.imread('/Users/hectorontiveros/Desktop/WCTEST/{0}'.format(fp),1))
imgs.pop(0)
for y in range(len(imgs)):
    imgs[y] = cv2.cvtColor(imgs[y], cv2.COLOR_BGR2RGB)
first_img = imgs[0].copy()

fig, ax_roi = plt.subplots()
ax_roi.set_title('Image 1 of {} in folder, create first ROI'.format(len(imgs)))
fi = ax_roi.imshow(first_img)
first_roi = RoiPoly(color = 'k')
first_roi.display_roi()
first_mask = first_roi.get_mask(first_img)
for im in imgs:
    im[first_mask != 1] = 0
    masked_imgs.append(im)
plt.close(fig)
fig1, ax_mask = plt.subplots()    
first_masked_img = masked_imgs[0]
ax_mask.set_title('Masked Image 1 of {} in folder'.format(len(masked_imgs)))
mi = ax_mask.imshow(first_masked_img)
class Index:
    ind = 0
    def next(self, event):
        self.ind += 1
        ax_mask.set_title('Masked Image {} of {} in folder'.format(self.ind+1, len(imgs)))
        mi.set_data(masked_imgs[self.ind])
        plt.draw()


    def prev(self, event):
        self.ind -= 1
        ax_mask.set_title('Image {} of {} in folder'.format(self.ind+1, len(imgs)))
        mi.set_data(masked_imgs[self.ind])
        plt.draw()

callback = Index()
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
#axfirst_roi = plt.axes([0.59, 0.05, 0.1, 0.075])
next_button = Button(axnext, 'Next')
next_button.on_clicked(callback.next)
prev_button = Button(axprev, 'Previous')
prev_button.on_clicked(callback.prev)
#bfirst_roi = Button(axfirst_roi, "Roi")
#bfirst_roi.on_clicked(callback.first_roi)

plt.show()