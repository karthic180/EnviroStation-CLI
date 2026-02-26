# providers.py
"""
Provider definitions for EnviroStation CLI.

Each provider entry defines:
- name: Human-readable name
- stations_json: URL for station metadata
- readings_json: URL for readings/time-series
- format: "json" or "csv" (optional)
"""

PROVIDERS = {
    "australia": {
        "name": "Australia – Water Data Service",
        "stations_json": "https://bom.gov.au/waterdata/services/stations",
        "readings_json": "https://bom.gov.au/waterdata/services/readings",
        "format": "json",
    },

    "new_zealand": {
        "name": "New Zealand – NIWA Hydrology",
        "stations_json": "https://api.niwa.co.nz/rainfall/stations",
        "readings_json": "https://api.niwa.co.nz/rainfall/data",
        "format": "json",
    },

    "canada": {
        "name": "Canada – Hydrometric Data",
        "stations_json": "https://dd.weather.gc.ca/hydrometric/csv/stations.csv",
        "readings_json": "https://dd.weather.gc.ca/hydrometric/csv",
        "format": "csv",
    },

    "united_kingdom": {
        "name": "United Kingdom – Environment Agency Hydrology",
        "stations_json": "https://environment.data.gov.uk/hydrology/id/stations",
        "readings_json": "https://environment.data.gov.uk/hydrology/id/readings",
        "format": "json",
    },

    "european_union": {
        "name": "European Union – Water Quality",
        "stations_json": "https://water.europa.eu/api/stations",
        "readings_json": "https://water.europa.eu/api/readings",
        "format": "json",
    },
}

# Dynamic providers added at runtime (AI Search or manual URL)
DYNAMIC_PROVIDERS = {}
