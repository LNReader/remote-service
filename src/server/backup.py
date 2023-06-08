import os
import json
import base64

all_types = ['Category', 'Novel', 'NovelCatgory', 'Chapter', 'Download', 'Plugins', 'Settings', 'File']

class RequestPackage:
    def __init__(self, backup_dir, json_obj) -> None:
        self.task = json_obj.get('taskType')
        self.content = json_obj.get('content')
        self.encoding = json_obj.get('encoding')    # None, base64, utf-8
        if self.encoding == 'base64':
            self.path = os.path.join(backup_dir, 'Images', json_obj.get('relative_path'))
        else:
            self.path = os.path.join(backup_dir, 'Data', json_obj.get('relative_path'))
        self.dir = os.path.dirname(self.path)

    def __str__(self) -> str:
        return self.task

def clean(webserver):
    pass

def backup(server, json_obj):
    request = RequestPackage(server.backup_dir, json_obj)
    os.makedirs(request.dir, exist_ok=True)
    if request.encoding == 'base64':
        with open(request.path, 'wb') as f:
            f.write(base64.b64decode(request.content))
    else:
        with open(request.path, 'w', encoding='utf-8') as f:
            if request.encoding == 'utf-8':
                f.write(request.content)
            else:
                f.write(json.dumps(request.content, ensure_ascii=False))
    server.window.log(f'<span style="color: rgb(170, 241, 175);">{request.task}</span>: {request.path}')
    return {"success": True, "message": "ok"}

def restore(webserver, json_obj):
    return {"success": False, "message": "Not Implemented"}

def old_restore(webserver, json_obj):
    return {"success": False, "message": "Not Implemented"}