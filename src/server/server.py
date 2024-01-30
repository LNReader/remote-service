""" 
POST: /upload/<path&&to&&file.zip> -> write data to <path/to/file.zip>
GET: /download/<path&&to&&/file.zip> -> read .zip file from <path/to/file.zip>
also get_workspace(): is the folder path which includes backup folders <name>.backup
an example for this url : /upload/nyagami.backup&&data.zip or /upload/nyagami.backup&&download.zip
"""
import sys
import json
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import FastAPI, File
from fastapi.responses import FileResponse

app = FastAPI()


def get_workspace():
    config_path = Path.home() / ".LNReader" / "config.json"
    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    return config["workspace"]


@app.get("/")
async def root():
    return {"name": "LNReader"}


@app.post("/upload/{path}&&{filename}")
async def upload(path: str, filename: str, file: Annotated[bytes, File()]):
    file_path = Path(get_workspace()) / path / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("wb") as f:
        f.write(file)

    return {"path": path, "filename": filename, "size": len(file)}


@app.get("/download/{path}&&{filename}")
async def download(path: str, filename: str):
    file_path = Path(get_workspace()) / path / filename
    if not file_path.exists():
        raise Exception("File not found")

    return FileResponse(file_path)


def main():
    try:
        if len(sys.argv) == 1:
            host = "localhost"
            port = 8000
        else:
            host, port = sys.argv[1], sys.argv[2]
            port = int(port)
        print(f"Start server - {host}:{port}")
        uvicorn.run(app, host=host, port=port)
    except Exception:
        print("python server.py [host] [port]")


if __name__ == "__main__":
    main()
