#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 15:18:46 2023

This file extracts the code from 'Velocity_Calculator', and export the calculated velocities to json file

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
images_dir = "/Users/yiweiji/Desktop/Velocity_calculation/qflow"
label_path = "/Users/yiweiji/Desktop/Velocity_calculation/AA4/qflow_3D/aorta_label.nii.gz"

image_files_list = sorted(
    glob.glob(os.path.join(images_dir, "*dcm")))

ds = dcm.read_file(image_files_list[0])

# DICOM Headers
protocol_name = ds.ProtocolName
for name in protocol_name.split('_'):
    try:
        int(name)
    except:
        print('')
    else:
        vENC = int(name) # unit: cm/s
        
RR_interval = int(ds.ImageComments.split(' ')[1]) # unit: ms

N_phases = len(image_files_list)

rescale_intercept = ds.RescaleIntercept

rescale_slope = ds.RescaleSlope

pixel_spacing = ds.PixelSpacing
voxel_volume_inplane = pixel_spacing[0] * pixel_spacing[1] / 100 # unit: cm^2

dt = RR_interval / N_phases / 1000 # unit: s

# Load the aorta label and find the phase with valid label
label = nib.load(label_path)

for phase in range(30):
    phase_data = label.get_fdata()[:,:,phase]
    if phase_data.sum() != 0:
        # valid_label.append(phase_data)
        valid_label = phase_data

# Calculation of the velocity, flow and volume in each phase
def vel_flow_calculation(image_path, label):
    # Load in the dcm format data to calculate the velocity
    ds = dcm.dcmread(image_path)
    img = ds.pixel_array
    
    # QC the PC-MRI
    # plt.imshow(img, cmap = 'bone')
    # plt.imshow(label, alpha = 0.3)
    # plt.show()
    
    # Convert the phase valve to velocity in the image
    # Should be ranged between -venc and +venc
    velocities = (np.double(img) + rescale_intercept/2) / abs(rescale_intercept) * rescale_slope * vENC * valid_label.transpose() # unit: cm/s
    
    # print (velocities.shape)
    return velocities

result_velocities = []
# Execute the function
for phase, image_path in enumerate(image_files_list):
   result_velocities.append(vel_flow_calculation(image_path, valid_label))
    
# print (result_velocities)
# print (result_velocities.shape)

# check sample speed within aorta_label
# plt.plot(result_velocities[50])

# Save and export result_velocities in json file
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

np_velocities = {"patient_folder":"AA4_20190614",
    "velocities":result_velocities}

# validation - plot result overlapping with a line
# plt.plot(result_velocities[50])


#plt.imshow(valid_label)
#plt.axvline(x=50)
#plt.show()

json_velocities = json.dumps(np_velocities, cls = NumpyArrayEncoder)

save_file = open("/Users/yiweiji/Desktop/Internship/Code/json_result.json","w")
json.dump(json_velocities,save_file, indent=6)

# with open('C:/Users/Henry/Desktop/CINE_res/Qflow_CINE_LVOT_Intersection_Plane_Info.json', 'w') as fout:
#     json.dump(intersection_list, fout)

print("JSON serialized NumPy array result saved")
# print(json_velocities)



    