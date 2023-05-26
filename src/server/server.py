import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

from .backup import backup, restore, old_backup, old_restore

map_handler = {
    '/backup': backup,
    '/restore': restore,
    '/old_backup': old_backup,
    '/old_restore': old_restore,
}

class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes("<h1>Hello</h1>", "utf-8"))

    def do_POST(self):
        handler = map_handler.get(self.path)
        if not handler:
            self.send_response(400)
        else: 
            content_len = int(self.headers.get("Content-Length"))
            try:
                post_body = self.rfile.read(content_len)
                json_obj = json.loads(post_body)
                handler(json_obj)
                self.send_response(200)
            except:
                self.send_response(400) 
        self.send_header("Content-type", "application/json")
        self.end_headers()
  
class WebServer(threading.Thread):
    def __init__(self, host, port, app_dir):
        super().__init__()
        self.host = host
        self.port = port
        self.backup_dir = os.path.join(app_dir, 'Backup')
        self.images_dir = os.path.join(self.backup_dir, 'Images')
        self.data_dir = os.path.join(self.backup_dir, 'Data')
        os.makedirs(self.backup_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        self.server = HTTPServer((self.host, self.port), ServerHandler)

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        # set the two flags needed to shutdown the HTTP server manually
        self.server._BaseServer__is_shut_down.set()
        self.server.__shutdown_request = True
        self.server.shutdown()
        self.server.server_close()
