import os
import json
import base64

class BackupRequestPackage:
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

class RestoreResponsePackage:
    def __init__(self, metadata, total) -> None:
        self.total = total
        self.type = metadata.get('type')
        self.real_path = metadata.get('real_path')
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
        res = RestoreResponsePackage(self.meta[index], len(self.meta))
        self.window.log(f'<span style="color: rgb(170, 241, 175);">{res.type}</span>: {res.real_path}')
        return res.toJson()

    def old_restore(self, json_obj):
        return {"success": False, "message": "Not Implemented"}

    def metadata(self):
        meta = []
        path = {
            'Novel': os.path.join(self.backup_dir, 'Data', 'Novel.json'),
            'Category': os.path.join(self.backup_dir, 'Data', 'Category.json'),
            'NovelCategory': os.path.join(self.backup_dir, 'Data', 'NovelCategory.json'),
            'Setting': os.path.join(self.backup_dir, 'Data', 'Setting.json'),
            'Chapter': os.path.join(self.backup_dir, 'Data', 'Chapters'),
            'Download': os.path.join(self.backup_dir, 'Data', 'Downloads'),
            'Plugin': os.path.join(self.backup_dir, 'Data', 'Plugins'),
            'Image': os.path.join(self.backup_dir, 'Images'),
            'Theme': os.path.join(self.backup_dir, 'Data', 'Theme.json')
        }

        def walk(path: str, root: str):
            if os.path.isfile(path):
                yield path.removeprefix(root + '\\').replace('\\', '/')
                return
            for item in os.scandir(path):
                for path in walk(item.path, root):
                    yield path

        for type in ['Category', 'Novel', 'NovelCategory', 'Theme']:
            meta.append({
                'type': type,
                'real_path': path[type]
            })
        if os.path.exists(path['Chapter']):
            for _path in walk(path['Chapter'], path['Chapter']):
                meta.append({
                    'type': 'Chapter',
                    'real_path': os.path.join(path['Chapter'], _path)
                })
        
        for type in ['Download', 'Plugin']:
            if os.path.exists(path[type]):
                for _path in walk(path[type], path[type]):
                    meta.append({
                        'type': type,
                        'encoding': 'utf-8',
                        'relative_path': _path,
                        'real_path': os.path.join(path[type], _path)
                    })
        if os.path.exists(path['Image']):
            for _path in walk(path['Image'], path['Image']):
                meta.append({
                    'type': 'Image',
                    'encoding': 'base64',
                    'relative_path': _path,
                    'real_path': os.path.join(path['Image'], _path)
                })

        meta.append({
            'type': 'Setting',
            'real_path': path['Setting']
        })
        
        meta_file = os.path.join(self.backup_dir, 'metadata.json')

        with open(meta_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps(meta, ensure_ascii=False))
        self.window.log('Backup successfully!')
        self.get_metadata()
