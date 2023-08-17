import os
import json
import base64

class BackupRequestPackage:
    def __init__(self, backup_dir, json_obj) -> None:
        self.task = json_obj.get('taskType')
        self.content = json_obj.get('content')
        self.encoding = json_obj.get('encoding')    # None, base64, utf-8
        if self.encoding == 'base64':
            self.path = slash_join(backup_dir, 'Download', json_obj.get('relative_path'))
        else:
            self.path = slash_join(backup_dir, 'Data', json_obj.get('relative_path'))
        self.dir = os.path.dirname(self.path)

    def __str__(self) -> str:
        return self.task

class RestoreResponsePackage:
    def __init__(self, metadata, total, backup_dir) -> None:
        self.total = total
        self.type = metadata.get('type')
        self.real_path = slash_join(backup_dir, metadata.get('suffix_path'))
        self.encoding = None
        self.relative_path = None
        if metadata.get('encoding'):
            self.encoding = metadata.get('encoding')
            self.relative_path = metadata.get('relative_path')

        if self.encoding == 'base64':
            with open(self.real_path, 'rb') as f:
                self.content = base64.b64encode(f.read()).decode()
        else:
            with open(self.real_path, 'r', encoding='utf-8') as f:
                if self.encoding == 'utf-8':
                    self.content = f.read()
                else:
                    self.content = json.loads(f.read())
        
    def toJson(self):
        return {
           'success': True, 
           'message': 'ok',
           'taskType': self.type,
           'content': self.content,
           'relative_path': self.relative_path,
           'total': self.total,
        }

def slash_join(_arg: str, *args: str):
    res = _arg.replace('\\', '/').removesuffix('/')
    for arg in args:
        arg = arg.replace('\\', '/').removeprefix('/')
        res = (res + '/' + arg).removesuffix('/')
    return res

class BackupHandler:
    def backup(self, json_obj):
        request = BackupRequestPackage(self.backup_dir, json_obj)
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
        self.window.log(f'<span style="color: rgb(170, 241, 175);">{request.task}</span>: {request.path}')
        return {"success": True, "message": "ok"}

    def restore(self, json_obj):
        finished = json_obj.get('finished')
        if finished:
            self.window.log('Restore successfully')
            return
        index = int(json_obj.get('index'))
        res = RestoreResponsePackage(self.meta[index], len(self.meta), self.backup_dir)
        self.window.log(f'<span style="color: rgb(170, 241, 175);">{res.type}</span>: {res.real_path}')
        return res.toJson()

    def old_restore(self, json_obj):
        return {"success": False, "message": "Not Implemented"}

    def metadata(self):
        meta = []

        # (filePath, encoding)
        paths = {
            'Version': (slash_join(self.backup_dir, 'Data', 'Version.json'), None),
            'Novel': (slash_join(self.backup_dir, 'Data', 'Novel.json'), None),
            'Category': (slash_join(self.backup_dir, 'Data', 'Category.json'), None),
            'NovelCategory': (slash_join(self.backup_dir, 'Data', 'NovelCategory.json'), None),
            'Setting': (slash_join(self.backup_dir, 'Data', 'Setting.json'), None),
            'Chapter': (slash_join(self.backup_dir, 'Data', 'Chapters'), None),
            'Download': (slash_join(self.backup_dir, 'Download'), 'base64'),
            'Theme':(slash_join(self.backup_dir, 'Data', 'Theme.json'), None)
        }

        def walk(path: str, root: str):
            if os.path.isfile(path):
                yield (path.removeprefix(root + '/'), 
                       path.removeprefix(self.backup_dir + '/'))
                return
            for item in os.scandir(path):
                for path in walk(item.path.replace('\\', '/'), root):
                    yield path

        for type in paths:
            path, encoding = paths[type]
            if os.path.exists(path):
                for realative_path, suffix_path in walk(path, path):
                    item = {
                        'type': type,
                        'suffix_path': suffix_path
                    }
                    if encoding:
                        item['encoding'] = encoding
                        item['relative_path'] = realative_path
                    meta.append(item)

        meta_file = slash_join(self.backup_dir, 'metadata.json')

        with open(meta_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(meta, ensure_ascii=False))
        self.get_metadata()
        self.window.log('Backup successfully!')
