import numpy as np
import scipy.io
from show_data import show_data
#path to the .mat file on your machine
struct = scipy.io.loadmat('C:\Workspace\...\MAT_normalizedData_PostStrokeAdults_SMALL.mat')
print(struct.keys())

show_data(struct)
