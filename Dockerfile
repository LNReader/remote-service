FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libc6-dev \
    libx11-dev \
    libxext-dev \
    && rm -rf /var/lib/apt/lists/*

# Install PDM
RUN pip install --no-cache-dir pdm

# Copy dependency files
COPY pyproject.toml pdm.lock ./

# Install dependencies
RUN pdm install --prod

# Copy application code
COPY . .

# Install Gunicorn
RUN pdm add gunicorn

# Create non-root user
RUN useradd -m myuser && \
    chown -R myuser:myuser /app
USER myuser

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run with Gunicorn
CMD ["pdm", "run", "gunicorn", "--config", "docker/gunicorn.conf.py", "src.server.server:app"]