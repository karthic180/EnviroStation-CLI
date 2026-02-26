# ============================
# EnviroStation CLI Makefile
# ============================

PYTHON = python
PIP = pip

# ----------------------------
# Installation
# ----------------------------

install:
    $(PIP) install -r requirements.txt
    $(PIP) install pytest

# ----------------------------
# Run the CLI
# ----------------------------

run:
    $(PYTHON) bootstrap.py

# ----------------------------
# Pytest Test Suite
# ----------------------------

pytest:
    pytest

pytest-offline:
    pytest -m "not online"

pytest-online:
    pytest -m online

test: pytest

# ----------------------------
# Docker
# ----------------------------

docker-build:
    docker build -t envirostation .

docker-run:
    docker run -it envirostation

# ----------------------------
# Code formatting (optional)
# ----------------------------

format:
    $(PYTHON) -m black .

# ----------------------------
# Cleanup
# ----------------------------

clean:
    rm -f env_explorer.db
    find . -type d -name "__pycache__" -exec rm -rf {} +
