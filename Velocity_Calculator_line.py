# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 18:05:31 2022

Calculate the Velocity Time Integral (VTI) of phase contrast MRI 
    - Use DICOM format data ONLY (NIFTI format image intensity is not correct)

@author: Henry
"""

import os
import glob
import nibabel as nib
import matplotlib.pyplot as plt
import pydicom as dcm
import numpy as np

# Qflow and Aorta Labels Input Directory and Paths
images_dir = "/Users/yiweiji/Desktop/Velocity_calculation/qflow"
p10_label_path = "/Users/yiweiji/Desktop/Velocity_calculation/aorta_label.nii"

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

# Load the aorta label
p10_label = nib.load(p10_label_path).get_fdata()

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
    velocities = (np.double(img) + rescale_intercept/2) / abs(rescale_intercept) * rescale_slope * vENC # unit: cm/s
    
    # We are only interested in the velocity values within the aorta
    roi_velocities = velocities* label.squeeze(-1).transpose() # unit: cm/s
    
    # Peak velocity
    peak_roi_vel = max(roi_velocities.flatten()) # unit: cm/s
    
    # Flow
    flow = sum(roi_velocities.flatten()) * voxel_volume_inplane # unit: ml/s
    
    # Volume
    volume = flow * dt # unit: ml^3
    
    return velocities

def plot_graph(PC_Report, para, title):
    temp_list = []
    time_step_list = []
    time_step =  RR_interval / N_phases
    for phase in range(0, N_phases + 1):
        ms = int(phase * time_step)
        time_step_list.append(ms)
        temp_list.append(PC_Report[phase][para])
    plt.plot(time_step_list, temp_list)
    plt.title(title)
    plt.xlabel('R-R Interval (ms)')
    plt.ylabel('Flow (mL/s)')
    plt.show()
    
    return temp_list, time_step_list

# Execute the function
PC_Report = [{
    'phase': 0,
    'peak_velocity': 0,
    'flow': 0,
    'forward_flow': 0,
    'backward_flow': 0,
    'volume': 0,
    'forward_volume': 0,
    'backward_volume': 0,
    }]


for phase, image_path in enumerate(image_files_list):
    peak_roi_vel, flow, volume = vel_flow_calculation(image_path, p10_label)
    
    if flow >= 0:
        forward_flow = flow
        backward_flow = 0
    else:
        forward_flow = 0
        backward_flow = flow
    
    # Forward & Backward Volume
    forward_volume = forward_flow * dt * voxel_volume_inplane # unit: cm^3
    backward_volume = backward_flow * dt * voxel_volume_inplane # unit: cm^3
    
    PC_Report.append({
        'phase': phase + 1,
        'peak_velocity': peak_roi_vel,
        'flow': flow,
        'forward_flow': forward_flow,
        'backward_flow': backward_flow,
        'volume': volume,
        'forward_volume': forward_volume,
        'backward_volume': backward_volume,
        })

# Display the key parameters
volume_total = 0
forward_volume_total = 0
backward_volume_total = 0
for parameters in PC_Report:
    volume_total += parameters['volume']
    forward_volume_total += parameters['forward_volume']
    backward_volume_total += parameters['backward_volume']
print('My Result: vol (ml):', "{0:0.2f}".format(volume_total),
      '; foward vol (ml):', "{0:0.2f}".format(forward_volume_total),
      '; backward vol (ml):', "{0:0.2f}".format(backward_volume_total),
      )
    
print('----------------------------------------------------------------------------------------------------------------')
print('James Result (s25): vol (ml): -55.98; foward vol (ml): 0.74; backward vol (ml): -56.72')
print('James Result (s39): vol (ml): 87.14; foward vol (ml): 89.05; backward vol (ml): -1.91')

# Plot the FTI
plot_graph(PC_Report, 'flow', 'FTI')