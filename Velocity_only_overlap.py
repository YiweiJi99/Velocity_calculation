#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:18:46 2023

This file trys to validate if the label on 3D is overlaped with dcm images.
This step is necessary for velocity calculation.

@author: yiweiji
"""

import nibabel as nib
import pydicom as dcm
import matplotlib.pyplot as plt

dcm_path = '/Users/yiweiji/Desktop/Internship/Image_processing/Data_CMR_Qflow_CINE_LVOT/AA42_20190730/Series0016_Qflow_merged_Other/Phase (0013).dcm'
nii_path = '/Users/yiweiji/Desktop/Internship/Image_processing/Data_CMR_Qflow_CINE_LVOT_nifti/AA42_20190730/qflow_3D/aorta_label.nii.gz'
# Load the images
ds = dcm.dcmread(dcm_path)
dcm_img = ds.pixel_array

nifti_img = nib.load(nii_path)
valid_label = []
# nifti_img_transposed = nifti_img.squeeze(-1).transpose()  # for 1 phase
for phase in range(30):
    phase_data = nifti_img.get_fdata()[:,:,phase]
    if phase_data.sum() != 0:
        valid_label.append(phase_data)
        nifti_img_transposed = phase_data.transpose()

plt.imshow(dcm_img, cmap = 'bone')
plt.imshow(nifti_img_transposed, alpha = 0.2)
plt.show()


# Plot both images together
# nib.plot_anat([dcm_img, nifti_img], title='DCM and Nifti Image',
#               cut_coords=[0, 0, 0], annotate=True)

# Load the images
#dcm_img = dcm.dcmread('/Users/yiweiji/Desktop/Velocity_calculation/Image (0010).dcm')
#nifti_img = nib.load('/Users/yiweiji/Desktop/Velocity_calculation/aorta_label.nii')
