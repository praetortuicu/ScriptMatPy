import scipy.io
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem



# DataTreeViz.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTreeWidget, QTreeWidgetItem
import scipy.io
import numpy as np

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
        try:
            data_dict = scipy.io.loadmat(self.file_path, squeeze_me=True, struct_as_record=False)
            return data_dict
        except Exception as e:
            print(f"Error importing Matlab file: {e}")
            return None

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
