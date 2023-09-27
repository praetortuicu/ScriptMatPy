import h5py
import numpy as np
import scipy.io
import matplotlib


from show_data import show_data
from MatToPy import is_hdf5_matlab_file

#path to the .mat file on your machine
file_path = 'C:\...\matlab_file_on_your_machine.mat'
is_hdf5_matlab_file(file_path)

if is_hdf5_matlab_file(file_path) is False:
    try:
        struct = scipy.io.loadmat(file_path)
        show_data(struct)
    except OSError:
        print("Could not load file! Check your file path, version...")
        

