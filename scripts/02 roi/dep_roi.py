import re
import matplotlib as mpl
import os.path
import pandas as pd
from PIL import Image

mpl.use('Qt5Agg')  # backend
import cv2
from roipoly import RoiPoly
import glob2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from collections import OrderedDict
from matplotlib.path import Path as MplPath