# EnviroStation CLI Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create volume for SQLite DB
VOLUME ["/app/env_explorer.db"]

# Default command: run bootstrap (auto-installs missing deps, launches CLI)
CMD ["python", "bootstrap.py"]
