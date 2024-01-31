""" 
POST: /upload/<path&&to&&file.zip> -> write data to <path/to/file.zip>
GET: /download/<path&&to&&/file.zip> -> read .zip file from <path/to/file.zip>
also get_workspace(): is the folder path which includes backup folders <name>.backup
an example for this url : /upload/nyagami.backup&&data.zip or /upload/nyagami.backup&&download.zip
"""
import json
import sys
from pathlib import Path
from typing import Any

from flask import Flask, request, send_file

app = Flask(__name__)


def get_workspace() -> Path:
    config_path = Path.home() / ".LNReader" / "config.json"
    with config_path.open("r", encoding="utf-8") as f:
        config = json.load(f)
    return Path(config["workspace"])


@app.route("/")
def root() -> dict[str, str]:
    return {"name": "LNReader"}


@app.post("/upload/<path:path>&&<path:filename>")
def upload(path: str, filename: str) -> dict[str, Any]:
    file_path = Path(get_workspace()) / path / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file = request.get_data()
    with file_path.open("wb") as f:
        f.write(file)

    return {"path": path, "filename": filename, "size": len(file)}


@app.get("/download/<path:backup_name>&&<path:filename>")
def download(backup_name: str, filename: str):
    file_path = Path(get_workspace()) / backup_name/ filename
    if not file_path.exists():
        raise Exception("File not found")

    return send_file(file_path)


@app.get("/list")
def list() -> list[str]:
    """list all backups"""
    workspace = Path(get_workspace())
    return [str(folder.name) for folder in workspace.iterdir() if folder.is_dir() and folder.name.endswith('.backup')]


def main():
    try:
        if len(sys.argv) == 1:
            host = "localhost"
            port = 8000
        else:
            host, port = sys.argv[1], sys.argv[2]
            port = int(port)
        print(f"Start server - {host}:{port}")
        app.run(host=host, port=port)
    except Exception:
        print("python server.py [host] [port]")


if __name__ == "__main__":
    main()
