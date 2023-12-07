from PyQt5.QtWidgets import QTreeView, QDialog, QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog, QTableWidget, QTableWidgetItem, QComboBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import sys
import numpy as np
import scipy.io

from MatToPy import MatToPyHDF5, MatToPySTD, MatToPy_Base


class SubArrayViewer(QDialog):
    def __init__(self, data):
        super().__init__()

        self.data = data
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.tree_view = QTreeView()
        self.model = QStandardItemModel()
        self.tree_view.setModel(self.model)
        self.tree_view.doubleClicked.connect(self.show_sub_array_dialog)

        self.layout.addWidget(self.tree_view)
        self.setLayout(self.layout)

        self.display_sub_array_data()

    def display_sub_array_data(self):
        if self.data is not None:
            self.populate_model(self.data, self.model.invisibleRootItem())

    def populate_model(self, data, parent_item):
        if isinstance(data, np.ndarray) and data.dtype.names is not None:
            # Handle structured array
            for field_name in data.dtype.names:
                field_data = data[field_name]
                field_item = QStandardItem(str(field_name))
                parent_item.appendRow(field_item)

                if isinstance(field_data, np.ndarray):
                    # If the field is an array, add its elements as child items
                    for i in range(field_data.shape[0]):
                        sub_array_item = QStandardItem(f"Element {i+1}")
                        field_item.setChild(i, sub_array_item)
                        self.populate_model(field_data[i], sub_array_item)
                elif isinstance(field_data, np.void):
                    # If the field is a nested structure, recursively populate
                    self.populate_model(field_data, field_item)
                else:
                    # If the field is a scalar, add it as a child item
                    item = QStandardItem(str(field_data))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make cells non-editable
                    field_item.appendRow(item)
        elif isinstance(data, dict):
            # Handle nested structure
            for field_name, field_data in data.items():
                field_item = QStandardItem(str(field_name))
                parent_item.appendRow(field_item)

                # Recursively populate for nested structs or arrays
                self.populate_model(field_data, field_item)
        else:
            # Handle other types of data (e.g., scalars, strings)
            item = QStandardItem(str(data))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make cells non-editable
            parent_item.appendRow(item)

    def show_sub_array_dialog(self, index):
        item = self.model.itemFromIndex(index)
        if item is not None:
            sub_array_data = self.extract_sub_array_data(item)
            if sub_array_data is not None:
                sub_array_dialog = SubArrayViewer(sub_array_data)
                sub_array_dialog.exec_()

    def extract_sub_array_data(self, item):
        # Extract the data associated with the clicked item
        data = self.data
        path = {}

        # Traverse the hierarchy to extract the path
        while item is not None:
            path.insert(0, item.text())
            item = item.parent()

        # Follow the path to extract the corresponding data
        for field_name in path:
            if isinstance(data, np.ndarray):
                if data.dtype.names and field_name in data.dtype.names:
                    data = data[field_name]
                elif field_name.startswith("Element"):
                    # Handling array elements
                    element_index = int(field_name.split()[-1]) - 1
                    data = data[element_index]
                elif field_name.isdigit():
                    # Handling tuple indices
                    data = data[int(field_name) - 1]
            elif isinstance(data, dict):
                data = data[field_name]
            elif isinstance(data, tuple):
                data = data[int(field_name.split()[-1]) - 1]

        return data


class MatplotlibViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()

        self.load_button = QPushButton('Load MATLAB Data')
        self.load_button.clicked.connect(self.load_matlab_data)

        self.group_selector_label = QLabel('Select Group:')
        self.group_selector = QComboBox()

        self.data_label = QLabel('')

        self.table = QTableWidget()
        self.table.itemDoubleClicked.connect(self.show_sub_array_dialog)

        self.data = None

        self.layout.addWidget(self.load_button)
        self.layout.addWidget(self.group_selector_label)
        self.layout.addWidget(self.group_selector)
        self.layout.addWidget(self.data_label)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.show()

        self.group_selector.currentIndexChanged.connect(self.display_group_data)

    def show_sub_array_dialog(self, item):
        if item is not None:
            row = item.row()
            col = item.column()

            # Retrieve the sub-array data based on the clicked cell
            sub_array_data = self.data[row, col]

            # Display the sub-array data in a new dialog
            sub_array_dialog = SubArrayViewer(sub_array_data)
            sub_array_dialog.exec_()

    def display_mat_data(self, data_dict):
        # Clear previous table contents
        self.table.clear()

        if data_dict is not None:
            # Iterate over the keys and values in data_dict
            for key, value in data_dict.items():
                # Create a new row in the table for each key-value pair
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)

                # Set the key in the first column
                key_item = QTableWidgetItem(str(key))
                key_item.setFlags(key_item.flags() ^ Qt.ItemIsEditable)  # Make cells non-editable
                self.table.setItem(row_position, 0, key_item)

                # Set the value in the second column
                value_item = QTableWidgetItem(str(value))
                value_item.setFlags(value_item.flags() ^ Qt.ItemIsEditable)  # Make cells non-editable
                self.table.setItem(row_position, 1, value_item)

    def load_matlab_data(self):
        try:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getOpenFileName(self, "Open MATLAB Data File", "", "MATLAB Files (*.mat);;All Files (*)", options=options)
            print(f"File path: {file_path}")

            if file_path:
                mat_to_py_instance = MatToPy_Base()
                is_hdf5, data = mat_to_py_instance.is_hdf5_matlab_file(file_path)

                if is_hdf5:
                    hdf5_instance = MatToPyHDF5()
                    self.data = hdf5_instance.import_data(file_path)
                else:
                    # Load standard MATLAB data
                    data_dict = MatplotlibViewer.load_standard_mat(file_path)
                    self.data = data_dict.get('StructTimeSmaller', None)

                if self.data is not None:
                    self.group_selector.clear()
                    if is_hdf5:
                        group_names = list(self.data.keys())
                    else:
                        group_names = ["StructTimeSmaller"]  # Replace with actual group names
                    self.group_selector.addItems(group_names)
                    self.display_group_data(0)  # Display the first group by default
                    self.data_label.setText(f'Data shape: {self.data.shape}')
                else:
                    print("Data import failed!")

        except Exception as e:
            print(f"Error importing data: {e}")
        if self.data is not None:
            print("Matlab data: ")
            print(self.data)

    @staticmethod
    def load_standard_mat(file_path):
        try:
            data_dict = scipy.io.loadmat(file_path)
            return data_dict
        except Exception as e:
            print(f"Error loading standard MATLAB file: {e}")
            return None

    def display_group_data(self, group_index):
        if self.data is not None and group_index < len(self.data):
            group_data = self.data[group_index]

            # Clear previous table contents
            self.table.clear()

            if isinstance(group_data, np.ndarray):
                if group_data.ndim == 1:
                    # If it's a 1D array, reshape it to have a single column
                    group_data = group_data.reshape(-1, 1)

                rows, cols = group_data.shape
                self.table.setRowCount(rows)
                self.table.setColumnCount(cols)

                for i in range(rows):
                    for j in range(cols):
                        item = QTableWidgetItem(str(group_data[i, j]))
                        item.setFlags(item.flags() ^ Qt.ItemIsEditable)  # Make cells non-editable
                        self.table.setItem(i, j, item)

            else:
                print("Group data is not an array.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = MatplotlibViewer()
    sys.exit(app.exec_())
