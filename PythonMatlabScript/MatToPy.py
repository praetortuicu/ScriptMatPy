#this module handles the imports of data in either HDF5 or standard MAT format

import h5py 
import scipy
file_path = 'C:\...\Matlab_file_on_your_machine.mat'


def is_hdf5_matlab_file(file_path):
    try:
        with h5py.File(file_path, 'r') as f:
            print("HDF5 file!")
            return True
    except OSError:
        print("Not an HDF5 file!")
        return False
        