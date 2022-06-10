#!/usr/bin/env python
# coding: utf-8

# # Camera Trap to Random Forests in Python

import pandas as pd
import numpy as np
import seaborn as sns
import json
from datetime import datetime as dt


# ### CSV

# Bring in the CSV data. The data is also available in JSON, which may actually be the most intuitive and efficient structure to unpack from in the long run.

csv_df = pd.read_csv('snowcam_training.csv')

csv_df.head()

# ### Wrangle the Data

# unpack 'region_attributes' column data to produce **class** variable

# image_class is a list- built to accept the
# modified 'region_attribute' data
image_class = []

# created by the for loop below
for i in range(len(csv_df['region_attributes'])):

    # convert the strings of json data into python dictionaries
    json_item = json.loads(csv_df['region_attributes'][i])

    # if data is not empty dictionary
    if json_item:

        # extract the name of the key, as a string in a list
        image_type = list(json_item['attribute'].keys())

        # if dictionary entry is not empty list
        if image_type:
            image_type = image_type[0]

        # leave None for empty values
        else:
            image_type = None
    else:
        image_type = None

    # add value to image_class
    image_class.append(image_type)

# make image_class a column of our dataframe
csv_df['class'] = image_class


# unpack 'region_shape' column data to produce **name** , **x** coordinate, **y** coordinate, **width** and **height** data

# unpack 'region_shape_attributes' into string of desired data
# leaving 'None' for empty values

# create dictionary to accept region shape data
region_shapes = {
    'name': [],
    'x': [],
    'y': [],
    'width': [],
    'height': [],
    }

# loop thru region attribute data
for i in range(len(csv_df['region_shape_attributes'])):
    # convert json strings to python dictionaries
    json_item = json.loads(csv_df['region_shape_attributes'][i])

    # loop thru the dictionary keys
    for attr in region_shapes.keys():
        # if JSON item contains data
        if json_item:
            # pull data item
            region_attr = json_item[attr]
            # append to that attribute's list in dictionary
            region_shapes[attr].append(region_attr)
        else:
            # otherwise, append None to appropriate list
            region_shapes[attr].append(None)

# create columns of this data in dataframe
for variable in region_shapes.keys():
    csv_df[variable] = region_shapes[variable]


# extract data frome the file name to produce **system**, **watershed**, **date**, and **pic_id** data
# dictionary of filename data
filename_data = {
    'system': [],
    'watershed': [],
    'date': [],
    'pic_id': [],
}

# loop through filename string
for i in range(len(csv_df['filename'])):
    # split contents by underscore
    file_items = csv_df['filename'][i].split('_')

    # add system column for 'hbwtr'
    filename_data['system'].append(file_items[1])
    # add watershed olumn, 'w1', 'w2', etc.
    filename_data['watershed'].append(file_items[2])
    # add date column
    filename_data['date'].append(
                                # modify integer date to date format, MM/DD/YYYY
                                dt.strptime(file_items[3], '%Y%m%d').strftime('%m/%d/%Y')
                                )
    # add picture id number
    filename_data['pic_id'].append(file_items[4])

# create columns of this data in dataframe
for variable in filename_data.keys():
    csv_df[variable] = filename_data[variable]


# adding calculated variables, for now, **area** and **aspect ratio**

# create polygon_area column
calculations = {
    'area': [],
    'aspect_ratio': []
}

# loop through dataframe
for i in range(len(csv_df['filename'])):
    # params
    height = csv_df['height'][i]
    width = csv_df['width'][i]

    # calcs
    area =  height * width
    aspect_ratio = height/width

    calculations['area'].append(area)
    calculations['aspect_ratio'].append(aspect_ratio)

# create columns of this data in dataframe
for variable in calculations.keys():
    csv_df[variable] = calculations[variable]

# make list to reorder columns
cols = csv_df.columns.tolist()
new_cols = cols[:1] + cols[13:16] + cols[7:13] + cols[16:17] + cols[1:7] + cols[17:]

csv_df = csv_df[new_cols]

# data download below, before modeling code

# 1: Download Full Dataframe
# csv_df.to_csv('camera_data_raw.csv')

# 2: Curated Dataframe (recommended)
csv_df = csv_df.drop(columns=['file_size', 'file_attributes', 'region_shape_attributes', 'region_attributes'])
csv_df.to_csv('camera_data.csv')

# 3: Random Forest prep dataframe
# drop all categorical data (except class, for now)
csv_df = csv_df.drop(
                columns=['filename', 'system', 'watershed',
                         'date', 'name', 'pic_id',]
                )
# drop all None values
csv_df = csv_df.fillna(value=np.nan)
csv_df = csv_df.dropna()

# ## Train Test Split
# split up the data into training set and test set

from sklearn.model_selection import train_test_split

X = csv_df.drop('class',axis=1)
y = csv_df['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30)

# ## Random Forest
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report,confusion_matrix

rfc = RandomForestClassifier(n_estimators=100)
rfc.fit(X_train, y_train)

rfc_pred = rfc.predict(X_test)

# report model statistics
print(confusion_matrix(y_test,rfc_pred))
print(classification_report(y_test,rfc_pred))
