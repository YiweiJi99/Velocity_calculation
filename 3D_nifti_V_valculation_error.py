#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 12:59:27 2023

This scrpit trys to transform the nifti file into 3D numpy array
without label

@author: yiweiji
"""

import os
import glob
import nibabel as nib
import matplotlib.pyplot as plt
import pydicom as dcm
import numpy as np
import json
from json import JSONEncoder

# Qflow and Aorta Labels Input Directory and Paths
# images_dir = "/Users/yiweiji/Desktop/Velocity_calculation/AA4/qflow_3D"
image_path = "/Users/yiweiji/Desktop/Velocity_calculation/AA4/qflow_3D/00.nii.gz"

# image_files_list = glob.glob(os.path(images_dir, "*nii"))  ### error!
# load nifti image data 
image_data = nib.load(image_path).get_fdata()

# print the shape of the 3D nifti file
print (image_data.shape)


# rescale_intercept = image_data.RescaleIntercept
# rescale_slope = image_data.RescaleSlope
# Calculation of the velocity, flow and volume in each phase
def vel_flow_calculation(image_path,image_data):
    # Load in the dcm format data to calculate the velocity
    img = image_data.pixel_array
    
    # QC the PC-MRI
    # plt.imshow(img, cmap = 'bone')
    # plt.imshow(label, alpha = 0.3)
    # plt.show()
    
    # Convert the phase valve to velocity in the image
    # Should be ranged between -venc and +venc
    velocities = np.double(img) * image_data # unit: cm/s
    
    print (velocities.shape)
    return velocities

# Execute the function
result_velocities = vel_flow_calculation(image_path, image_data)