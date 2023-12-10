from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QApplication
from scipy.io import loadmat, matlab
import numpy as np
import sys

class DataTreeViewer(QDialog):
    def __init__(self, file_path):
        super().__init__()

        self.file_path = file_path
        self.data_dict = self.load_matlab_data()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('MATLAB Data Tree Visualization')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(["Key", "Value"])

        self.layout.addWidget(self.tree)
        self.setLayout(self.layout)

        self.populate_tree()





    def load_matlab_data(self):
        """
        This function should be called instead of direct scipy.io.loadmat
        as it cures the problem of not properly recovering python dictionaries
        from mat files. It calls the function check keys to cure all entries
        which are still mat-objects
        """
        def _check_vars(d):
            """
            Checks if entries in dictionary are mat-objects. If yes
            todict is called to change them to nested dictionaries
            """
            for key in d:
                if isinstance(d[key], matlab.mio5_params.mat_struct):
                    d[key] = _todict(d[key])
                elif isinstance(d[key], np.ndarray):
                    d[key] = _toarray(d[key])
            return d

        def _todict(matobj):
            """
            A recursive function that constructs nested dictionaries from matobjects
            """
            d = {}
            for strg in matobj._fieldnames:
                elem = matobj.__dict__[strg]
                if isinstance(elem, matlab.mio5_params.mat_struct):
                    d[strg] = _todict(elem)
                elif isinstance(elem, np.ndarray):
                    d[strg] = _toarray(elem)
                else:
                    d[strg] = elem
            return d

        def _toarray(ndarray):
            """
            A recursive function that constructs an ndarray from cellarrays
            (which are loaded as numpy ndarrays), recursing into the elements
            if they contain matobjects.
            """
            if ndarray.dtype != 'float64':
                elem_list = []
                for sub_elem in ndarray:
                    if isinstance(sub_elem, matlab.mio5_params.mat_struct):
                        elem_list.append(_todict(sub_elem))
                    elif isinstance(sub_elem, np.ndarray):
                        elem_list.append(_toarray(sub_elem))
                    else:
                        elem_list.append(sub_elem)
                return np.array(elem_list)
            else:
                return ndarray

        data = loadmat(self.file_path, struct_as_record=False, squeeze_me=True)
        data_dict = _check_vars(data)
        return data_dict


    def add_items_to_tree(self, parent_item, values):
        if isinstance(values, np.ndarray) and len(values.shape) == 1:
            child_item = QTreeWidgetItem(["Value", str(values)])
            if parent_item is not None:
                parent_item.addChild(child_item)
            else:
                self.tree.addTopLevelItem(child_item)
        elif isinstance(values, np.ndarray) and len(values.shape) == 2:
            for row in values:
                child_item = QTreeWidgetItem(["Value", str(row)])
                if parent_item is not None:
                    parent_item.addChild(child_item)
                else:
                    self.tree.addTopLevelItem(child_item)
        elif isinstance(values, np.ndarray) and values.dtype.names is not None:
            for field_name in values.dtype.names:
                field_value = values[field_name]
                child_item = QTreeWidgetItem([str(field_name), "Value"])
                if parent_item is not None:
                    parent_item.addChild(child_item)
                else:
                    self.tree.addTopLevelItem(child_item)
                self.add_items_to_tree(child_item, field_value)
        elif isinstance(values, dict):
            for key, sub_values in values.items():
                child_item = QTreeWidgetItem([str(key)])
                if parent_item is not None:
                    parent_item.addChild(child_item)
                else:
                    self.tree.addTopLevelItem(child_item)
                self.add_items_to_tree(child_item, sub_values)
        elif hasattr(values, '_fieldnames'):
            for field_name in values._fieldnames:
                field_value = getattr(values, field_name)
                child_item = QTreeWidgetItem([str(field_name)])
                if parent_item is not None:
                    parent_item.addChild(child_item)
                else:
                    self.tree.addTopLevelItem(child_item)
                self.add_items_to_tree(child_item, field_value)
        else:
            child_item = QTreeWidgetItem(["Value", str(values)])
            if parent_item is not None:
                parent_item.addChild(child_item)
            else:
                self.tree.addTopLevelItem(child_item)

    def populate_tree(self):
        if self.data_dict is not None:
            items = []
            for key, values in self.data_dict.items():
                item = QTreeWidgetItem([str(key)])
                self.add_items_to_tree(item, values)
                items.append(item)
            self.tree.insertTopLevelItems(0, items)