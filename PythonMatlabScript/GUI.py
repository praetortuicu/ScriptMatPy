from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem
import sys
import numpy as np

from MatToPy import MatToPyHDF5, MatToPySTD, MatToPy_Base

class MatplotlibViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.load_button = QPushButton('Load MATLAB Data')
        self.load_button.clicked.connect(self.load_matlab_data)

        self.data_label = QLabel('')

        self.table = QTableWidget()

        self.data = None

        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.data_label)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.show()

    def load_matlab_data(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Open MATLAB Data File", "", "MATLAB Files (*.mat);;All Files (*)", options=options)
            print(f"File path: {file_path}")

            if file_path:
                mat_to_py_instance = MatToPy_Base()
                is_hdf5, data = mat_to_py_instance.is_hdf5_matlab_file(file_path)
                if is_hdf5:
                    # Load MATLAB HDF5 data
                    hdf5_instance = MatToPyHDF5()
                    object_references = hdf5_instance.import_data(file_path)

                    # Access the objects in 'Sub' using the new approach
                    data_dict = hdf5_instance.access_objects_in_dataset(object_references)

                    # Display grouped data
                    for group_index, obj_ref in data_dict.items():
                        print(f"Data in group {group_index}:")
                        print(obj_ref)

                    print("File path: ", file_path)
                else:
                    mat_to_py_instance = MatToPySTD()
                    data_dict = mat_to_py_instance.import_data(file_path)
                    self.data = data_dict.get('StructTimeSmaller', None)
                
                    if self.data is not None:
                        # Display data
                        if hasattr(self.data, 'shape'):
                            self.data_label.setText(f'Data shape: {self.data.shape}')
                        else:
                            self.data_label.setText('Data shape: (Not applicable)')

                        # Populate table
                        if isinstance(self.data, np.ndarray):
                            self.table.setRowCount(self.data.shape[0])
                            self.table.setColumnCount(self.data.shape[1])

                            for i in range(self.data.shape[0]):
                                for j in range(self.data.shape[1]):
                                    item = QTableWidgetItem(str(self.data[i, j]))
                                    self.table.setItem(i, j, item)
                        else:
                            print("Data is not an array.")
                    else:
                        print("Data import failed!")

        except Exception as e:
            print(f"Error importing data: {e}")
            return None



                    

def main():
    app = QApplication(sys.argv)
    viewer = MatplotlibViewer()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
