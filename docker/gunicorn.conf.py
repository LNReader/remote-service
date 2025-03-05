import os

# Get configuration from environment variables with defaults
host = os.environ.get("HOST_IP", "0.0.0.0")
port = int(os.environ.get("HOST_PORT", "8000"))
workers = int(os.environ.get("MAX_WORKERS", "4"))
timeout = int(os.environ.get("TIMEOUT", "120"))

# Bind to host:port
bind = f"{host}:{port}"

# Worker configuration
worker_class = "sync"
keepalive = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Protect against slowloris DOS attack
worker_connections = 1000
timeout = timeout
graceful_timeout = 30
