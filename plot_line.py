#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 17:12:51 2023

@author: yiweiji
"""

# open json file in python as df
# list of dictionary

import json
import pandas as pd
import matplotlib.pyplot as plt
f = open ('/Users/yiweiji/Desktop/Internship/Image_processing/Qflow_CINE_LVOT_Intersection_Plane_Info.json')
coordinates = json.load(f)

df_coordinates = pd.DataFrame(coordinates)

# plot the intersect_points of the first patient
inter_point1 = df_coordinates.loc[0]["intersect_points_Qflow"]
inter_point2 = df_coordinates.loc[0]["intersect_points_3CH"]
plt.plot(inter_point1[0],inter_point1[1],inter_point2[0],inter_point2[1])
plt.show()

