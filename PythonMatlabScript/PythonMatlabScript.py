import h5py
import numpy as np
import scipy.io
import matplotlib
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem
import sys

# from show_data import show_data
from MatToPy import MatToPy_Base, MatToPyHDF5, MatToPySTD

struct = MatToPySTD()

#path to the .mat file on your machine
#struct.path = 'C:\Workspace\HiWi\HCMR\Received Data\Data from Liz\Example Data\MAT_normalizedData_PostStrokeAdults_SMALL.mat'
with h5py.File('C:\Workspace\HiWi\HCMR\Received Data\Data from Christian\JupyterlabScript\struct_withEventLog_withoutData.mat', 'r') as file:
    file.visititems(lambda name, obj: print(name, obj))
#what field are you searching for:
#group_name = 'sub_char'
#MatToPySTD.import_data(struct)
# print(struct.data)
#MatToPySTD.access_matlab_subfield(struct, 'Sub', 'events')

# MatToPyHDF5.import_data(struct)
# MatToPyHDF5.explore_hdf5_structure_and_access_data(struct, group_name)
#the import works, the data is weird. some structure issues, check hdf5 documentation


#MatToPyHDF5.get_field_value_and_position_HDF5(struct, field_name)
#TODO: write a function that shows where exactly in the matlab struct a specific variable is and print out its' value