import sys
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem

#define an empty dictionary with Project files. Example below
data = {"Project A: ": ["file1.txt", "file2.mat", "file3.xls"]} #Project A would in this case be the name of the sub, the files would then be the 
                                                                #matlab struct(s)
app = QApplication() #called QApplication singleton. same bro same

tree = QTreeWidget()
tree.setColumnCount(2) #this is file specific. can change this to update automatically- would be nice. but probably just check the structure of the data and update as needed
tree.setHeaderLabels(["Name", "Type"]) #same as above


#iterate the data structure, create the QTreeWidgetItem elements and add the corresponding children to each parent. We also take the extension name for only the files and add them to the second column
items = []
for key, values in data.items():
    item = QTreeWidgetItem([key])
    for value in values:
        ext = value.split(".")[-1].upper()
        child = QTreeWidgetItem([value, ext])
        item.addChild(child)
    items.append(item)
tree.insertTopLevelItems(0, items)

tree.show()
sys.exit(app.exec())