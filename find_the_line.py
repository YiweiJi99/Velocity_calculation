#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 16:02:53 2023

This file is Step1: open nii file and fit the line

@author: yiweiji
"""

# import libraries 
import os
import nibabel as nib
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from nibabel.testing import data_path
import json
import pandas as pd
import matplotlib.pyplot as plt
import pydicom as dcm

# open DCM image
dcm_path = '/Users/yiweiji/Desktop/Internship/Image_processing/Data_CMR_Qflow_CINE_LVOT/AA4_20190614/Series0015_Qflow_merged_Other/Phase (0001).dcm'
# Load the images
ds = dcm.dcmread(dcm_path)
dcm_img = ds.pixel_array
plt.imshow(dcm_img, cmap = 'bone')
plt.show()


# plot the line through centriod
f = open ('/Users/yiweiji/Desktop/Internship/Image_processing/Qflow_CINE_LVOT_Intersection_Plane_Info.json')
coordinates = json.load(f)
df_coordinates = pd.DataFrame(coordinates)

# plot the intersect_points in image of the first patient
#inter_point = df_coordinates.loc[0]["intersect_points_3CH"] # "intersect_points_Qflow" or 'intersect_points_3CH'
#plt.plot(inter_point[0],inter_point[1],color='r')
#plt.show()

inter_point_Qflow = df_coordinates.loc[1]["intersect_points_Qflow"]
inter_point_3CH = df_coordinates.loc[1]["intersect_points_3CH"]
patient = df_coordinates.loc[1]["patient_folder"]

point1 = inter_point_Qflow[0]
point2 = inter_point_Qflow[-1]
plt.plot([point1[0], point2[0]], [point1[1], point2[1]]) # inter_point_3CH[0],inter_point_3CH[1]




