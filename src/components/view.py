import typing
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QTextBrowser

class View(QWidget):
    def __init__(self, parent, x, y, w, h) -> None:
        super().__init__(parent)
        self.setGeometry(x, y, w, h)
        self.setObjectName("view")
        self.text = QTextBrowser(self)
        self.text.setGeometry(0, 0, w, h)
