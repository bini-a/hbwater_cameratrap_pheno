
import logging
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from roipoly import MultiRoi

logging.basicConfig(format='%(levelname)s ''%(processName)-10s : %(asctime)s '
                           '%(module)s.%(funcName)s:%(lineno)s %(message)s',
                    level=logging.INFO)

# Create image
img = cv2.imread("/Users/hectorontiveros/Desktop/fwsp.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Show the image
fig = plt.figure()
plt.imshow(img)
plt.title("Click on the button to add a new ROI")

# Draw multiple ROIs
multiroi_named = MultiRoi(roi_names=['My first ROI', 'My second ROI'])

# Draw all ROIs
plt.imshow(img)
roi_names = []
for name, roi in multiroi_named.rois.items():
    roi.display_roi()
    roi.display_mean(img)
    roi_names.append(name)
plt.legend(roi_names, bbox_to_anchor=(1.2, 1.05))
plt.show()
