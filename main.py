
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow
)

import os
import json
from http.server import HTTPServer
from threading import Thread

from src.server.server import Server
from src.components.form import Form

BASE_DIR = os.path.dirname(__file__)

class MainWindow(QMainWindow):
    def __init__(self, app: QApplication):
        super().__init__()
        self.app = app
        self._width = 600
        self._height = 200
        self.setWindowIcon(QIcon(os.path.join(BASE_DIR, 'static/images/icon.png')))
        self.setWindowTitle("LNReader: Remote service (not started)")
        self.setFixedSize(QSize(self._width, self._height))
        self.load_config()
        self.form = Form(self, 20, 20, 560, 180)
        self.form.start_btn.clicked.connect(self.start_server)
        self.show()
    
    def start_server(self):
        try:
            host, workspace = self.form.valid()
            ip, port = host, 80
            if ':' in host:
                ip, port_str = host.split(':')
                port = int(port_str)
            self.config['host'] = host
            self.config['workspace'] = workspace
            self.update_config()
        except Exception as e:
            print('ERROR', e)
            return
        self.httpd = HTTPServer((ip, port), Server)
        self.server_thread = Thread(target=self.httpd.serve_forever)
        self.server_thread.start()
        self.setWindowTitle(f"LNReader: Remote service ({host})")
        
        self.app.aboutToQuit.connect(self.httpd.shutdown)
        self.form.start_btn.setDisabled(True)
        self.form.host_inp.setDisabled(True)
        self.form.browse_btn.setDisabled(True)

    # %user_dir%/.LNReader/config.json
    def load_config(self):
        self.app_dir = os.path.join(os.path.expanduser('~'), '.LNReader')
        if not os.path.exists(self.app_dir):
            os.mkdir(self.app_dir)
        self.config_path = os.path.join(self.app_dir, 'config.json')
        if not os.path.exists(self.config_path):
            open(self.config_path, 'w').write(
                json.dumps({'workspace': self.app_dir})
            )
        self.config = json.loads(open(self.config_path, 'r').read())

    def update_config(self):
        open(self.config_path, 'w').write(json.dumps(self.config))

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
