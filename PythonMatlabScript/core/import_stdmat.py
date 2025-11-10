import logging
import scipy.io
import numpy as np
from collection import deque
from .base_importer import MatToPy_Base


logger  =   logging.getLogger(__name__)

class MatToPySTD(MatToPy_Base):
    """
    Handles importing and exploring of standard (non-HDF5) .mat files.
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
            self.path = file_path
            self.data = scipy.io.loadmat(file_path, squeeze_me=True, struct_as_record=False)
            logger.info(f"Keys in Matlab file: {self.data.keys()}")
            return self.data
        except Exception as e:
            logger.info(f"Error importing data from .mat file: {e}")
            return None
        
    @staticmethod
    def get_field_value_and_position_stdmat(self, field_name):
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
            # Initialize a queue for BFS traversal of the data dictionary
            queue = deque([(self.data, [])])

            while queue:
                current_data, current_path = queue.popleft()

                for key, value in current_data.items():
                    new_path = current_path + [key]

                    if key == field_name:
                        return value, new_path

                    if isinstance(value, dict):
                        queue.append((value, new_path))

            logger.info(f"Field '{field_name}' not found.")
            return None, None

        except Exception as e:
            logger.info(f"Error traversing Matlab structure: {e}", exc_info=True)
            return None, None
        

    def explore_structure(self, key: str) -> dict:
        """
        Return the contents of a field or group without printing — for GUI or logging display.

		Args:
			key (str): Key or group name to inspect.

		Returns:
			dict or np.ndarray or None: The contents of the key, or None if missing.
        """
        if not self.data:
            logger.warning("No data loaded! Call import_data() first.")
            return None

        try:
            if key not in self.data:
                logger.warning(f"Key {key} not found!")
                return None

            target = self.data[key]
            return target

        except Exception as e:
            logger.error(f"Error loading or exploring MAT file: {e}")
            return None


    def access_subfield(self, field_name: str, subfield_name: str):
        """
        Access a specific subfield from the loaded MATLAB structure.

		Args:
			field_name (str): Main field name.
			subfield_name (str): Subfield to access.

		Returns:
			object: The subfield value, or None if missing.
        """
        if not self.data:
			logger.warning("No data loaded. Call import_data() first.")
			return None

        try:
            field = self.data.get(field_name)
            if field is None:
                logger.warning(f"Field '{field_name}' not found!\n")
                return None

            subfield = getattr(field, subfield_name, None) if hasattr(field, subfield_name) else field.get(subfield_name)
			if subfield is None:
				logger.warning(f"Subfield '{subfield_name}' not found in '{field_name}'.")
				return None

            return subfield
        except Exception as e:
            logger.info(f"Error accessing subfield: '{field_name}.{subfield_name}: {e}", exc_info=True)
            return None
