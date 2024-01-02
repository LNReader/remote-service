from PyQt6 import QtCore, QtWidgets

class Form(QtWidgets.QWidget):
    def __init__(self, parent, x, y, w, h) -> None:
        super().__init__(parent)
        self.setGeometry(QtCore.QRect(x, y, w, h))
        self.setObjectName("form")
        self.host_label = QtWidgets.QLabel(self)
        self.host_label.setGeometry(QtCore.QRect(20, 20, 81, 31))
        self.host_label.setObjectName("host_label")
        self.host_label.setText("Host")
        self.host_inp = QtWidgets.QLineEdit(self)
        self.host_inp.setGeometry(QtCore.QRect(120, 20, 221, 31))
        self.host_inp.setObjectName("host_inp")
        self.host_inp.setPlaceholderText("192.168.10.17:8000")
        self.host_inp.setText(parent.config.get('host') or '')

        self.workspace_laber = QtWidgets.QLabel(self)
        self.workspace_laber.setGeometry(QtCore.QRect(20, 100, 81, 31))
        self.workspace_laber.setObjectName("workspace_laber")
        self.workspace_laber.setText("Workspace")
        self.workspace_inp = QtWidgets.QLineEdit(self)
        self.workspace_inp.setGeometry(QtCore.QRect(120, 100, 221, 31))
        self.workspace_inp.setObjectName("workspace_inp")
        self.workspace_inp.setDisabled(True)
        self.workspace_inp.setText(parent.config.get('workspace'))
        self.browse_btn = QtWidgets.QPushButton(self)
        self.browse_btn.setGeometry(QtCore.QRect(350, 100, 60, 31))
        self.browse_btn.setText("Browse")
        self.browse_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.browse_btn.clicked.connect(self.browser_folder)

        self.start_btn = QtWidgets.QPushButton(self)
        self.start_btn.setGeometry(QtCore.QRect(420, 20, 100, 40))
        self.start_btn.setObjectName("start_btn")
        self.start_btn.setText("Start")
        self.start_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    def valid(self):
        host, folder = self.host_inp.text(), self.workspace_inp.text()
        if not (host and folder):
            raise Exception("You have to fill all inputs")
        return host, folder

    def browser_folder(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self)
        self.workspace_inp.setText(path)

