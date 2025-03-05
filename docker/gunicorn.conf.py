import os

# Use PORT environment variable with default
port = int(os.environ.get("PORT", "8000"))
bind = f"0.0.0.0:{port}"

# Worker configuration
workers = 4
worker_class = "sync"
keepalive = 30

# Timeout settings
timeout = 120
graceful_timeout = 30

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Protect against slowloris DOS attack
worker_connections = 1000
