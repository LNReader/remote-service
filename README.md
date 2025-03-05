# LNReader Remote Service

- Required LNReader version: >= 2.0.0
- `LAN network - Wifi and Windows PC` or `a web server`

## Remote Backup with GUI

1. Start LNReaderRS.exe
2. Enter your machine address `<host>:<post>`
3. Open Android App -> Setting -> Backup -> Self Host Backup

## Remote Backup with command line

1. Clone project
2. Run `pdm install`
3. Run `pdm run server <host> <port>`
4. Open Android App -> Setting -> Backup -> Self Host Backup

## Example

- [How to backup and restore (video)](https://youtu.be/-0H-0j8y9OI)

## Docker Deployment

1. Clone project
2. Configure environment variables (optional):
   - `PORT`: Port where the service will run (default: 8000)
   - `STORAGE_PATH`: Local path to store LNReader data (default: ~/.LNReader)
3. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```
4. Open Android App -> Setting -> Backup -> Self Host Backup with `<host>:<PORT>`

Example with custom configuration:

```bash
PORT=9000 STORAGE_PATH=/path/to/backup docker-compose up -d
```
