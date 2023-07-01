from PyQt6 import QtCore, QtWidgets
from subprocess import check_output
import re
import os

class Form(QtWidgets.QWidget):
    def __init__(self, parent, x, y, w, h) -> None:
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(x, y, w, h))
        self.setObjectName("form")
        self.address_label = QtWidgets.QLabel(self)
        self.address_label.setGeometry(QtCore.QRect(20, 20, 81, 31))
        self.address_label.setObjectName("address_label")
        self.address_label.setText("Address")
        self.address_inp = QtWidgets.QLineEdit(self)
        self.address_inp.setGeometry(QtCore.QRect(120, 20, 221, 31))
        self.address_inp.setObjectName("address_inp")

        self.port_label = QtWidgets.QLabel(self)
        self.port_label.setGeometry(QtCore.QRect(20, 70, 81, 31))
        self.port_label.setObjectName("port_label")
        self.port_label.setText("Port")
        self.port_inp = QtWidgets.QLineEdit(self)
        self.port_inp.setGeometry(QtCore.QRect(120, 70, 221, 31))
        self.port_inp.setObjectName("port_inp")

        self.folder_laber = QtWidgets.QLabel(self)
        self.folder_laber.setGeometry(QtCore.QRect(20, 120, 81, 31))
        self.folder_laber.setObjectName("folder_laber")
        self.folder_laber.setText("Folder")
        self.folder_inp = QtWidgets.QLineEdit(self)
        self.folder_inp.setGeometry(QtCore.QRect(120, 120, 221, 31))
        self.folder_inp.setObjectName("folder_inp")
        self.folder_inp.setDisabled(True)
        self.browse_btn = QtWidgets.QPushButton(self)
        self.browse_btn.setGeometry(QtCore.QRect(350, 120, 60, 31))
        self.browse_btn.setText("Browse")
        self.browse_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.browse_btn.clicked.connect(self.browser_folder)

        self.start_btn = QtWidgets.QPushButton(self)
        self.start_btn.setGeometry(QtCore.QRect(420, 20, 100, 40))
        self.start_btn.setObjectName("start_btn")
        self.start_btn.setText("Start")
        self.start_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.port_inp.setText("8000")
        if self.parent().config.get("folder"):
            self.folder_inp.setText(self.parent().config.get("folder"))
        else:
            path = os.path.join(os.path.expanduser('~'), 'Downloads')
            self.folder_inp.setText(path)
            self.parent().config["folder"] = path
            self.parent().update_config()

    def valid(self):
        host, port, folder = self.address_inp.text(), self.port_inp.text(), self.folder_inp.text()
        return host, port, folder
    
    def browser_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.folder_inp.setText(path)
        self.parent().config["folder"] = path
        self.parent().update_config()
