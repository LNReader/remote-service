from http.server import BaseHTTPRequestHandler, HTTPServer
import mimetypes
import os
import json
import cgi

def get_workspace():
    app_dir = os.path.join(os.path.expanduser('~'), '.LNReader')
    config = json.loads(open(os.path.join(app_dir, 'config.json')).read())
    return config['workspace']
class Server(BaseHTTPRequestHandler):
    def _header(self, headers = {}):
        self.send_response(200)
        for key in headers:
            self.send_header(key, headers[key])
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self._header()
            data = {
                'name': 'LNReader'
            }
            self.wfile.write(bytes(json.dumps(data), 'utf-8'))
        elif self.path.startswith('/download'):
            try:
                file_path = os.path.join(get_workspace(), self.path.removeprefix('/download/'))
                f = open(file_path, 'rb')
                content_length = os.fstat(f.fileno()).st_size
                content_type = mimetypes.guess_type(file_path)[0]
                self._header({
                    'Content-Type': content_type,
                    'Content-Length': content_length
                })
                self.wfile.write(f.read())
                self.wfile.flush()
                f.close()
            except Exception as e:
                print('ERROR:', e)
                self.send_response(400)
                self.end_headers()
                self.wfile.write(bytes(str(e), 'utf-8'))

    def do_POST(self):
        try:
            form = cgi.FieldStorage( fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type'], })
            keys = form.keys()
            metadata, media = {}, None
            if 'metadata' in keys:
                metadata = json.loads(form.getvalue('metadata'))
            else:
                raise Exception('No metedata provided')
            if 'media' in keys:
                media = form['media']

            folder_path = os.path.join(get_workspace(), '/'.join(metadata['folderTree']))

            if self.path == '/list':
                if os.path.exists(folder_path):
                    data = os.listdir(folder_path)
                else:
                    data = []
                self._header({
                    'Content-Type': 'application/json'
                })
                self.wfile.write(bytes(json.dumps(data), 'utf-8'))
            elif self.path == '/exists':
                file_path = os.path.join(folder_path, metadata['name'])
                data = {
                    'exists': os.path.exists(file_path)
                }
                self._header({
                    'Content-Type': 'application/json'
                })
                self.wfile.write(bytes(json.dumps(data), 'utf-8'))
            elif self.path == '/upload':
                if media != None:
                    file_path = os.path.join(folder_path, metadata['name'])
                    os.makedirs(name=folder_path, exist_ok=True)
                    if metadata['mimeType'] == 'application/json':
                        with open(file_path, 'w', encoding="utf-8") as f:
                            f.write(media.file.read())
                    else:
                        with open(file_path, 'wb')as f:
                            f.write(media.file.read())
                    self._header()
                else:
                    raise Exception('No file provided')
            
        except Exception as e:
            print('ERROR:', e)
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes(str(e), 'utf-8'))

if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 8000), Server)
    print("Start server - localhost:8000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
