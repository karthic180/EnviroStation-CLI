# EnviroStation CLI

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Repo Size](https://img.shields.io/github/repo-size/karthic180/EnviroStation-CLI)
![Stars](https://img.shields.io/github/stars/karthic180/EnviroStation-CLI?style=social)

A powerful command‑line tool for exploring hydrology and environmental data from multiple global providers.  
Includes region search, fuzzy matching, AI‑assisted API discovery, SQLite caching, internal diagnostics, and database tools.

---

## 🚀 Features

- Multi‑provider support (AU, NZ, UK, EU, CA)
- Add your own provider (paste URL)
- AI‑assisted provider discovery with:
  - URL validation
  - Metadata preview
  - Automatic mapping hints
- Region search (dynamic + fallback)
- Fuzzy matching for region, postcode, town
- SQLite caching with auto‑purge
- Database tools (VACUUM, row counts, last readings)
- Full internal test suite
- Docker support

---

## 📦 Installation

### Clone the repo

```bash
git clone https://github.com/karthic180/EnviroStation-CLI
cd EnviroStation-CLI
Install dependencies
bash
pip install -r requirements.txt
Run the CLI
bash
python bootstrap.py
🐳 Running with Docker
Build:

bash
docker build -t envirostation .
Run:

bash
docker run -it envirostation
The SQLite database is stored in a Docker volume.

🗃️ Viewing the Database
If using VS Code, install:

SQLite Viewer  
https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer (marketplace.visualstudio.com in Bing)

Then open:

Code
env_explorer.db
🧪 Tests
Run internal tests from the main menu:

Code
3) Admin tests
Includes:

Smoke tests

End‑to‑end tests

Region tests

DB tests

API reachability

📜 License
MIT License — see LICENSE.

📝 Changelog
See CHANGELOG.md.