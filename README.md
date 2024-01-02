# LNReader Remote Service
- Required LNReader version: >= 2.0.0
- `LAN network - Wifi and Windows PC` or `a web server`

## Remote Backup with GUI
1. Start LNReaderRS.exe
2. Enter your machine address `<host>:<post>`
3. Open Android App -> Setting -> Backup -> Self Host Backup

## Remote Backup with command line
1. Clone project
2. Create python virtual environment
3. Activate virtual environment
4. Run `pip install -r requirement.txt`
5. Run `python ./src/server/server.py <host> <port>`
6. Open Android App -> Setting -> Backup -> Self Host Backup

## Example
- [How to backup and restore (video)](https://youtu.be/Sg9RLLTecVk)
