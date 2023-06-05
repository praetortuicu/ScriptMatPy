import numpy as np
import scipy.io


#path to the .mat file on your computer
struct = scipy.io.loadmat('C:\Workspace\HiWi\HCMR\Received Data\Data from Liz\Example Data\MAT_normalizedData_PostStrokeAdults_SMALL.mat')

print(struct.items())