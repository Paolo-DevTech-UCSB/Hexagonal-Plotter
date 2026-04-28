# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 2024
    ---Last edited Oct 25th 2024
This Version of 3D Height Plot Code Adds both the Difference Plots and Shape Plots into One .py
    
    -LD Right and HD Full seem to be working
        -features that needed to be added:
            -Center offset, - becuase this code centers at x&y averages, a manual offset is needed for partial shapes. 
            -added more code to improve confidence in xls parsing:
                Z value needs to come immediately after X and Y to register as a data point
            -Added labeling and error features that differentiate difference from shape plot. 
                -Fixed Shape Plots Using error Correction. (V7)
                V10 - added hdb using a white cover layer
                
    Version 11: Fundamental Rewrite With Batch Procesing in mind. 

@author: Paolo Jordano
"""
#For Difference plots
import numpy as np

import numpy.ma as ma

import scipy.linalg
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
from matplotlib.colors import Normalize


#For other Operations
import os
import datetime

workDir = os.getcwd()





