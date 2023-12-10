from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog
from DataTreeViz import DataTreeViewer

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Main GUI')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()

        self.import_button = QPushButton('Import MATLAB Data')
        self.import_button.clicked.connect(self.import_matlab_data)

        self.layout.addWidget(self.import_button)
        self.setLayout(self.layout)

    def import_matlab_data(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Open MATLAB Data File", "", "MATLAB Files (*.mat);;All Files (*)", options=options)

        if file_path:
            # Create an instance of the DataTreeViewer with the imported data
            tree_viewer = DataTreeViewer(file_path)
            tree_viewer.exec_()  # Show the tree visualization window

if __name__ == '__main__':
    app = QApplication([])
    main_gui = MainGUI()
    main_gui.show()
    app.exec_()