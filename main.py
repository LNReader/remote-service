
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)

import os
import json

from src.server.server import WebSocketServer
from src.components.form import Form
from src.components.view import View

BASE_DIR = os.path.dirname(__file__)

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self._width = 720
        self._height = 480
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, 'static/images/icon.png')))
        self.setWindowTitle("LNReader: Remote service (not started)")
        self.setFixedSize(QSize(self._width, self._height))
        self.load_config()
        self.form = Form(self, 90, 300, 560, 181)
        self.view = View(self, 20, 20, self._width - 20*2, 270)
        self.form.start_btn.clicked.connect(self.start_server)
        self.show()
    
    def start_server(self):
        try:
            host, port, folder = self.form.valid()
        except Exception as e:
            self.log(e)
            return
        self.server = WebSocketServer(host, int(port), folder, self)
        self.server.start()
        self.app.aboutToQuit.connect(self.server.shutdown)
        
        self.form.start_btn.setDisabled(True)
        self.form.address_inp.setDisabled(True)
        self.form.port_inp.setDisabled(True)
        self.form.browse_btn.setDisabled(True)

    def log(self, message):
        self.view.text.insertHtml(f'<p>{message}</p><br>')
        self.view.text.verticalScrollBar().setValue(self.view.text.verticalScrollBar().maximum())

    # %user_dir%/.LNReader/config.json
    def load_config(self):
        self.config_dir = os.path.join(os.path.expanduser('~'), '.LNReader')
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)
        self.config_path = os.path.join(os.path.expanduser('~'), '.LNReader', 'config.json')
        if not os.path.exists(self.config_path):
            with open(self.config_path, 'w') as f:
                f.write(json.dumps({}))
        with open(self.config_path, 'r') as f:
            self.config = json.loads(f.read())

    def update_config(self):
        with open(self.config_path, 'w') as f:
            f.write(json.dumps(self.config))

app = QApplication([])

theme = {
    'primary': 'rgb(0, 87, 206)',
    'onprimary': 'rgb(255, 255, 255)',
    'primaryContainer': 'rgb(218, 226, 255)',
    'onPrimaryContainer': 'rgb(0, 25, 70)',
    'secondary': 'rgb(88, 94, 113)',
    'onSecondary': 'rgb(255, 255, 255)',
    'secondaryContainer': 'rgb(220, 226, 249)',
    'onSecondaryContainer': 'rgb(21, 27, 44)',
    'tertiary': 'rgb(114, 85, 114)',
    'onTertiary': 'rgb(255, 255, 255)',
    'error':  'rgb(186, 26, 26)',
    'onError': 'rgb(255, 255, 255)',
    'outline': 'rgb(117, 119, 128)',
    'outlineVariant': 'rgb(197, 198, 208)',
    'shadow': 'rgb(0, 0, 0)',
    'background': 'rgb(254, 251, 255)',
    'onBackground': 'rgb(27, 27, 31)',
    'surface': 'rgb(254, 251, 255)',
    'onSurface': 'rgb(27, 27, 31)',
    'surfaceDisabled': 'rgba(27, 27, 31, 0.12)',
    'onSurfaceDisabled': 'rgba(27, 27, 31, 0.38)',
}

with open(os.path.join(BASE_DIR, 'static/styles/styles.qss'), 'r') as f:
    styles = f.read()
    for attribute in theme:
        styles = styles.replace(f'-{attribute}-', theme[attribute])
    app.setStyleSheet(styles)

window = MainWindow(app)
app.exec()