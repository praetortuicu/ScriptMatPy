from abc import ABC




class MatToPy_Base(ABC):
        def __init__(self) -> None:
            self.name:  str =   "" #name of the variable in which the dataset is saved
            self.path = ""  #path to the .mat file
            self.data = []  #values inside the imported dataset
        
        @staticmethod 
        def is_hdf5_matlab_file(self, file_path):
            """
            Check if an imported Matlab file is in standard .mat format or if it is HDF5 format. Useful for debugging and 
            when instantiating the dataset object
            
            Args: 
                self.path (str): The path to the Matlab data file.
            Returns:
                Prints out a text message depending on what type of file format python detected.
            """
            try:
                print(f"Trying to open file: {file_path}")
                with h5py.File(file_path, 'r') as f:
                    print("HDF5 file!")
                    return True, None
            except OSError:
                print("Not an HDF5 file!")
                return False, None
            except Exception as e:
                print(f"Error opening file: {e}")
                return False


        def import_data(self, file_path):
            """
            Handles the data import from Matlab into Python. Checks for format type of the data and populates self.data accordingly.
            
            Args:
                self.path (str): The path to the Matlab data file.
                self.data (python collection or h5py dict): The dataset imported form Matlab.
            Returns:
                Loads the dataset into memory or throws an Exception if there is an error.
            """
            raise NotImplementedError("Subclasses must implement import_data")            
            
        # # Example usage:
        # matlab_file_path = 'your_data_file.mat'  # Replace with the path to your MATLAB data file
        # field_to_find = 'Age'                   # Replace with the name of the field you want to retrieve

        # field_value, field_position = get_field_value_and_position(matlab_file_path, field_to_find)
        # if field_value is not None:
        #     print(f"{field_to_find} = {field_value}")
        #     print(f"Position of {field_to_find} = {'.'.join(map(str, field_position))}")

