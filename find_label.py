#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 12:59:27 2023

This scrpit trys to find the label in 30 phases-nifti file in one patient

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
label_path = "/Users/yiweiji/Desktop/Velocity_calculation/AA4/qflow_3D/aorta_label.nii.gz"

# load label data 
label = nib.load(label_path)

valid_label = []

# save 30 phase of 'aorta_label.nii' as a list of list
#for phase in range(30):
#    phase_data = img.get_fdata()[:,:,phase]
#    label.append(phase_data)
 
# extrac the phase with label > 0
#for i in range (30):
#    if label[i].sum() != 0:
#        valid_label = label[i]
        
# print the shape of the 3D nifti file
#print (type(valid_label))

# don't need to save 30 phases in variable - label
for phase in range(30):
    phase_data = label.get_fdata()[:,:,phase]
    if phase_data.sum() != 0:
        valid_label.append(phase_data)
    print (type(np.array(valid_label)))  # printing shape is meaningless
    
    