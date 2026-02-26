# ai_search.py
import requests
from typing import Any, Dict, List, Tuple

# Keys that indicate hydrology-like data
HYDRO_KEYS = {
    "station", "stations", "site", "sites",
    "river", "catchment", "lat", "lon",
    "value", "reading", "readings", "gauge",
    "waterlevel", "flow", "discharge"
}

# ------------------------------------------------------------
# AI + Web + Pattern + Static Search Layers
# ------------------------------------------------------------

def search_ai_primary(country: str) -> List[str]:
    """
    Placeholder for real AI search.
    Returns empty list so fallback layers activate.
    """
    return []


def search_web_fallback(country: str) -> List[str]:
    """
    Placeholder for real web search.
    Returns empty list so fallback layers activate.
    """
    return []


def search_pattern_fallback(country: str) -> List[str]:
    """
    Generates heuristic search patterns.
    These are not URLs, but hints that may contain URLs.
    """
    return [
        f"https://api.{country.lower().replace(' ', '')}.gov/hydrology",
        f"https://water.{country.lower().replace(' ', '')}.gov/api",
        f"https://environment.{country.lower().replace(' ', '')}.gov/api",
        f"https://{country.lower().replace(' ', '')}.hydrology.api",
    ]


def search_static_fallback(country: str) -> List[str]:
    """
    Known hydrology endpoints for specific regions.
    """
    known = {
        "united kingdom": [
            "https://environment.data.gov.uk/hydrology/id/stations",
        ],
        "australia": [
            "https://bom.gov.au/waterdata/services",
        ],
        "new zealand": [
            "https://api.niwa.co.nz/rainfall",
        ],
        "european union": [
            "https://water.europa.eu/api",
        ],
        "canada": [
            "https://dd.weather.gc.ca/hydrometric/csv",
        ],
    }
    return known.get(country.lower(), [])


def ai_search_for_provider(country: str) -> List[str]:
    """
    Full failback chain:
    1. AI search
    2. Web search
    3. Pattern search
    4. Static known endpoints
    """
    for fn in (
        search_ai_primary,
        search_web_fallback,
        search_pattern_fallback,
        search_static_fallback,
    ):
        results = fn(country)
        if results:
            return results
    return []


def choose_ai_search_country() -> str | None:
    print("\nAI Search – Choose Country")
    print("--------------------------")
    country = input("Enter country name (or blank to cancel): ").strip()
    if not country:
        return None
    return country


# ------------------------------------------------------------
# URL Validation
# ------------------------------------------------------------

def _flatten_keys(obj: Any):
    """Recursively extract all keys from nested JSON."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k.lower()
            yield from _flatten_keys(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from _flatten_keys(item)


def is_valid_hydrology_api(url: str) -> bool:
    """
    Validates whether a URL is a real hydrology API.
    """
    if not url.startswith(("http://", "https://")):
        return False
    if " " in url:
        return False
    if "google.com" in url or "bing.com" in url:
        return False

    try:
        resp = requests.get(url, timeout=6)
    except Exception:
        return False

    if not (200 <= resp.status_code < 300):
        return False

    ctype = resp.headers.get("Content-Type", "").lower()
    if "json" not in ctype and "csv" not in ctype:
        return False

    # JSON validation
    if "json" in ctype:
        try:
            data = resp.json()
        except Exception:
            return False

        keys = set(_flatten_keys(data))
        if HYDRO_KEYS & keys:
            return True
        return False

    # CSV accepted
    if "csv" in ctype:
        return True

    return False


# ------------------------------------------------------------
# Metadata Preview + Mapping Detection
# ------------------------------------------------------------

def fetch_sample_payload(url: str) -> Tuple[bool, Dict[str, Any] | None]:
    """Fetch JSON payload for preview."""
    try:
        resp = requests.get(url, timeout=8)
    except Exception:
        return False, None

    if not (200 <= resp.status_code < 300):
        return False, None

    ctype = resp.headers.get("Content-Type", "").lower()
    if "json" not in ctype:
        return False, None

    try:
        data = resp.json()
    except Exception:
        return False, None

    return True, data


def guess_mapping_from_payload(data: Any) -> Dict[str, str]:
    """
    Heuristic mapping detection.
    Returns a dict of mapping hints.
    """
    mapping: Dict[str, str] = {}

    def find_first_key(candidates: List[str]) -> str | None:
        keys = list(_flatten_keys(data))
        for c in candidates:
            if c.lower() in keys:
                return c
        return None

    station_key = find_first_key(["station", "stationId", "site", "siteId", "id", "code"])
    name_key = find_first_key(["name", "stationName", "siteName", "label"])
    lat_key = find_first_key(["lat", "latitude", "y"])
    lon_key = find_first_key(["lon", "lng", "longitude", "x"])
    value_key = find_first_key(["value", "reading", "level", "flow", "discharge"])
    date_key = find_first_key(["date", "datetime", "time", "timestamp"])

    if station_key:
        mapping["station"] = station_key
    if name_key:
        mapping["name"] = name_key
    if lat_key:
        mapping["lat"] = lat_key
    if lon_key:
        mapping["lon"] = lon_key
    if value_key:
        mapping["value"] = value_key
    if date_key:
        mapping["date"] = date_key

    return mapping


def preview_api_metadata(url: str) -> None:
    """Prints a preview of the API's JSON structure + mapping hints."""
    ok, data = fetch_sample_payload(url)
    if not ok or data is None:
        print("\nCould not fetch or parse JSON from this URL.\n")
        return

    print("\nSample metadata preview (truncated):")
    if isinstance(data, list):
        sample = data[:1]
    elif isinstance(data, dict):
        sample = {k: data[k] for k in list(data.keys())[:5]}
    else:
        sample = str(data)[:500]
    print(sample)

    mapping_hint = guess_mapping_from_payload(data)
    if mapping_hint:
        print("\nAutomatic mapping hints:")
        for k, v in mapping_hint.items():
            print(f"  {k} -> {v}")
    else:
        print("\nNo obvious mapping hints found.")
