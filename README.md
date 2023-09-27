# PythonMatlabScript

This script handles rudimentary dataset imports from Matlab into Python by first checking what kind of format the files are saved in (right now, either HDF5 or standard Matlab are supported).
The MatToPy.py module contains a function which checks the file type and returns True if the file is HDF5 format and False if it is standard Matlab format.
The show_data.py module prints out a neat and visible representation of the data, if it is not imported with the h5py package (used for a quick look at how the data is structured after being imported).
