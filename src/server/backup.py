import os
import json
import base64

all_types = ['Category', 'Novel', 'NovelCatgory', 'Chapter', 'Download', 'Plugins', 'Settings', 'File']

class RequestPackage:
    def __init__(self, backup_dir, json_obj) -> None:
        self.type = json_obj.get('type')
        self.content = json_obj.get('content')
        self.encode = json_obj.get('encode')    # None or base64
        if self.encode == 'base64':
            self.path = os.path.join(backup_dir, 'Images', json_obj.get('relative_path'))
        else:
            self.path = os.path.join(backup_dir, 'Data', json_obj.get('relative_path'))
        self.dir = os.path.dirname(self.path)

    def __str__(self) -> str:
        return self.type

def backup(webserver, json_obj):
    request = RequestPackage(webserver.backup_dir, json_obj)
    os.makedirs(request.dir, exist_ok=True)
    if request.encode == 'base64':
        with open(request.path, 'wb') as f:
            f.write(base64.b64decode(request.content))
    else:
        with open(request.path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(request.content, ensure_ascii=False))
    webserver.window.log(f'{request.type}: {request.path}')
    return {"success": True, "message": "ok"}

def restore(webserver, json_obj):
    return {"success": False, "message": "Not Implemented"}

def old_backup(webserver, json_obj):
    return {"success": False, "message": "Not Implemented"}

def old_restore(webserver, json_obj):
    return {"success": False, "message": "Not Implemented"}