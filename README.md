# 🌍 EnviroStation CLI

A cross‑platform command‑line tool for exploring environmental monitoring stations, fetching live readings, and performing offline/online analysis.  
Built for reliability, portability, and clean data workflows.

---

## 📛 Badges

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://github.com/karthic180/EnviroStation-CLI/actions/workflows/ci.yml/badge.svg)
![Status](https://img.shields.io/badge/Status-Active-success)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

---

## 🚀 Features

- Fetch environmental stations from multiple providers  
- Retrieve live readings with retry logic + caching  
- Offline and online test modes  
- Region search and fuzzy matching  
- Data mapping utilities  
- Cross‑platform support  
- Clean modular architecture  

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/karthic180/EnviroStation-CLI.git
cd EnviroStation-CLI
Install dependencies:

bash
pip install -r requirements.txt
▶️ Usage
Run the CLI:

bash
python run.py
Run the test suite:

bash
python run_tests.py
Choose:

1 → All tests

2 → Offline tests

3 → Online tests

🧪 Testing
Tests are located in the tests/ directory.

To run with pytest directly:

bash
pytest
📁 Project Structure
Code
EnviroStation-CLI/
│
├── api_client.py
├── providers.py
├── mapping.py
├── region_search.py
├── validation.py
├── system_info.py
├── geo.py
├── db.py
├── db_tools.py
├── run.py
├── run_tests.py
│
├── utils/
│   └── helpers.py
│
├── data/
│   └── sample.json
│
├── logs/
│   └── app.log
│
└── tests/
    ├── test_offline.py
    ├── test_online.py
    ├── test_integration.py
    └── test_validation.py
## 📚 Documentation

EnviroStation CLI provides a modular architecture for fetching, mapping, and analyzing environmental station data.

### Core Modules

| Module | Description |
|--------|-------------|
| `api_client.py` | Handles API requests with retries + caching |
| `providers.py` | Defines provider endpoints and metadata |
| `mapping.py` | Normalizes station and reading data |
| `region_search.py` | Fuzzy region matching and filtering |
| `validation.py` | Input validation and sanitization |
| `system_info.py` | Auto-detects system and location info |
| `geo.py` | Provider auto-selection and geolocation helpers |
| `utils/helpers.py` | Shared utility functions |

### Test Suite

The project includes a full offline + online test suite:

- `test_offline.py` — mapping, region search, validation  
- `test_online.py` — live API tests  
- `test_integration.py` — system-level checks  
- `test_validation.py` — input sanitization  

Run tests:

```bash
python run_tests.py

📜 License
This project is licensed under the MIT License.