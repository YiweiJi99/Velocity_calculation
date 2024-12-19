#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 16:02:53 2023

@author: yiweiji
"""
# This file is Step1: open nii file and fit the line
# This file puts a random line on image, next step is try to calculate the velocity

# import libraries 
import os
import nibabel as nib
import scipy.ndimage as ndi
import matplotlib.pyplot as plt
from nibabel.testing import data_path
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# open 2D image
example_file = os.path.join(data_path,'/Users/yiweiji/Desktop/Velocity_calculation/00.nii')
img = nib.load(example_file)
img = img.get_fdata()
# plt.imshow(ndi.rotate(img,90)) # rotate image
plt.imshow(img)

# draw a line from (0,132) to (192,0)
x_line = np.array(range(0,192,1))
y_line = np.array(range(192,0,-1))

# plot the intersect_points in image of the first patient
#inter_point = df_coordinates.loc[0]["intersect_points_3CH"] # "intersect_points_Qflow" or 'intersect_points_3CH'
#plt.plot(inter_point[0],inter_point[1],color='r')
#plt.show()

plt.plot(x_line,y_line)
plt.show()