# EnviroStation CLI (Minimal)

A small, open-source, terminal-based hydrology explorer for multiple regions:

- United Kingdom (Environment Agency)
- New Zealand (NIWA, simplified)
- Australia (BOM, simplified)
- Canada (Hydrometric, simplified)
- Europe (EEA Waterbase, simplified)

## Features

- Browse stations by provider
- Search by region/state/province/country code
- Search by station name, river, town, or ID
- View readings for a selected station/measure
- Web search (DuckDuckGo + Wikipedia)
- Minimal dependencies

## Installation

```bash
pip install -r requirements.txt
Usage
bash
python run.py
Tests
bash
pytest -q
Docker
bash
docker build -t envirostation-cli .
docker run -it envirostation-cli
License
MIT