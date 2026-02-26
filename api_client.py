import requests
from requests.adapters import HTTPAdapter, Retry
from functools import lru_cache
from providers import PROVIDERS
from helpers import extract_uuid_from_url, parse_csv


def _provider(pid):
    if pid not in PROVIDERS:
        raise ValueError(f"Unknown provider: {pid}")
    return PROVIDERS[pid]


def _session():
    s = requests.Session()
    retries = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


SESSION = _session()


@lru_cache(maxsize=32)
def fetch_stations(pid):
    p = _provider(pid)
    r = SESSION.get(p.stations, timeout=p.timeout)
    r.raise_for_status()

    if p.format == "csv":
        return {"items": parse_csv(r.text)}

    try:
        return r.json()
    except Exception:
        return {"items": []}


@lru_cache(maxsize=64)
def fetch_measures_for_station(pid, station_uri):
    p = _provider(pid)

    if p.region == "uk" and p.format == "csv":
        r = SESSION.get(p.measures, timeout=p.timeout)
        r.raise_for_status()
        return {"items": parse_csv(r.text)}

    # Australia & Canada treat station as measure
    return {"items": [{"measure_uri": station_uri, "station": station_uri}]}


@lru_cache(maxsize=128)
def fetch_readings_for_measure(pid, measure_uri_or_id):
    p = _provider(pid)

    if p.region == "uk" and p.format == "csv":
        url = f"{p.readings}?station={measure_uri_or_id}&_limit=200&sort=latest"
        r = SESSION.get(url, timeout=p.timeout)
        r.raise_for_status()
        return {"items": parse_csv(r.text)}

    if p.region == "aus":
        url = f"{p.readings}/{measure_uri_or_id}.json"
        r = SESSION.get(url, timeout=p.timeout)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return {"items": []}

    if p.region == "ca":
        url = f"{p.readings}/daily/{measure_uri_or_id}.csv"
        r = SESSION.get(url, timeout=p.timeout)
        r.raise_for_status()
        return {"items": parse_csv(r.text)}

    return {"items": []}
