import threading
import websockets
import asyncio
import json
import os

from .backup import backup, restore, old_restore, metadata

map_handler = {
    'Backup': backup,
    'Restore': restore,
    'OldRestore': old_restore,
    'Metadata': metadata,
}

class WebSocketServer(threading.Thread):
    def __init__(self, host, port, app_dir, window):
        super().__init__()
        self.host = host
        self.port = port
        self.backup_dir = os.path.join(app_dir, 'Backup')
        os.makedirs(self.backup_dir, exist_ok=True)
        self.window = window

        # this will avoid program re-read metadata file for each request
        metadata_path = os.path.join(self.backup_dir, 'metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.meta = json.loads(f.read())

    async def handler(self, websocket):
        async for message in websocket:
            json_obj = json.loads(message)
            handler_type = json_obj.get('type')
            handler = map_handler.get(handler_type)
            if handler:
                if handler_type == 'Metadata':
                    handler(self)
                    res = None
                else:
                    res = handler(self, json_obj.get('data'))
            else:
                res = {
                    "success": False,
                    "message": "Unsupported handler"
                }
            if res: await websocket.send(json.dumps(res))
    
    async def forever(self):
        async with websockets.serve(self.handler, self.host, self.port):
            self.window.log(f'Server started at ws://{self.host}:{self.port}')
            self.window.setWindowTitle("LNReader: Remote service (started)")
            await asyncio.Future()

    def run(self):
        asyncio.run(self.forever())
    
    def shutdown(self):
        raise Exception("Kill Websocket server")