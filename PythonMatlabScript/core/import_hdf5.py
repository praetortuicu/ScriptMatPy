import logging
import h5py
import numpy as np
from collections import deque
from .base_importer import MatToPy_Base

logger = logging.getLogger(__name__)



class MatToPyHDF5(MatToPy_Base):
    """
    Handles importing and exploring HDF5 .mat files.
    """

    def import_data(self, file_path):
        """
        Load a Matlab .mat file and store its contents in memory.
        Args:
            file_path (str): Path to the .mat file.
        Returns:
            dict: Loaded Matlab data structure.
        """

        try:
            logger.info(f"Attempting to open file: {file_path}")
            self.path   =   file_path
            self.data   =   h5py.File(file_path, 'r')
            logger.info(f"Keys in Matlab file: {self.data.keys()}")
            return self.data
        except Exception as e:
            logger.info(f"Error importing data from HDF5 file: {e}", exc_info=True)
            return None

    @staticmethod
    def get_field_value_and_position_HDF5(field_name):
        """
		Retrieve the value and nested position of a field from the loaded data.

		Args:
			field_name (str): Name of the field to locate.

		Returns:
			tuple: (value, path_list) or (None, None) if not found.
		"""
        if not self.data:
            logger.warning("No data loaded! Call import_data() first.")
            return None
        try:
            queue   =   deque([(self.data, [])])
            while queue:
                current_data, current_path  =   queue.popleft()

            for key, value in current_data.items():
                new_path    =   current_path + [key]

            if  key ==  field_name:
                return  value,  new_path

            if  isinstance(value,   dict):
                queue.append((value,    new_path))

            logging.info(f"Field {field_name} not found!")
            return None, None

        except Exception as e:
            logger.info(f"Error opening HDF5 data file : {e}", exc_info=True)
            return None

    def explore_hdf5_structure(self,    group,  target_group_name):
        """
        Return the contents of a field or group without printing — for GUI or logging display.

		Args:
			key (str): Key or group name to inspect.

		Returns:
			dict or np.ndarray or None: The contents of the key, or None if missing.
        """
        if not self.data:
            logger.warning("No data loaded! Call import_data() first.")
            return  None
        try:
            if  target_group_name   in  group:
                target_data     =   group[target_group_name]

            if  isinstance(target_data, h5py.Group):
                logger.info(f"Contents of group: '{target_group_name}' : ")
            
                for key in  target_data:
                    logger.info(f" - {key}")
            elif    isinstance(target_data, h5py.Dataset):
                data        =   target_data[()]
                logger.info(f"Data in dataset '{target_group_name}' : ")
                return  data
            else:
                logger.warning(f"Group or dataset '{target_group_name}' not found in file!")

    def acces_hdf5_data(self,   field_name: str,    subfield_name:  str):
        """
        Access a specific subfield from the loaded MATLAB structure.

		Args:
			field_name (str): Main field name.
			subfield_name (str): Subfield to access.

		Returns:
			object: The subfield value, or None if missing.
        """
        if not  self.data:
            logger.warning("No data loaded! Call import_data() first.")
            return None

        try:
            field   =   self.data.get(field_name)
            if  field   is  None:
                logger.warning(f"Field '{field_name}' not found!")
                return  None
            subfield    =   getattr(field,  subfield_name, None) if hasattr(field,  subfield_name,  None)   else    field.get(subfield_name)
            if  subfield    is  None:
                logger.warning(f"Subfield '{subfield_name}' not found in {field_name}!")
                return  None
            return  subfield
        except  Exception   as  e:
            logger.info(f"Error accessing subfield: '{field_name}.{subfield_name}: {e}", exc_info=True)
            return  None

    def explore_hdf5_structure_and_access_data(self, group, target_group_name):
        try:
            if target_group_name in group:
                target_data = group[target_group_name]

                if isinstance(target_data, h5py.Group):
                    print(f"Contents of group: '{target_group_name}': ")
                    for key in target_data:
                        print(f" - {key}")
                elif isinstance(target_data, h5py.Dataset):
                    data = target_data[()] #Access the data in the dataset
                    print(f"Data in dataset '{target_group_name}':")
                    print(data)
                    return data
                else:
                    print(f"Group or dataset '{target_group_name}' not found in file!")
        except Exception as e:
            print(f"Error exploring or accessing HDF5 data: {e}")
        return None
