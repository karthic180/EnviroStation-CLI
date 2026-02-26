import csv

from rapidfuzz import fuzz

def fuzzy_match(query: str, text: str, threshold: int = 60) -> bool:
    if not text:
        return False
    score = fuzz.partial_ratio(query.lower(), text.lower())
    return score >= threshold

def extract_uuid_from_url(value: str) -> str:
    if not value:
        return value
    if value.startswith("http"):
        return value.rstrip("/").split("/")[-1]
    return value


def extract_items(provider_id, raw):
    if isinstance(raw, dict) and "items" in raw:
        return raw["items"]
    if isinstance(raw, dict) and "data" in raw:
        return raw["data"]
    return raw


def safe_get(item: dict, *keys):
    for key in keys:
        if key in item and item[key] not in (None, "", []):
            return item[key]
    return None


def normalise_float(value):
    try:
        return float(value)
    except Exception:
        return None


def parse_csv(text: str):
    rows = []
    reader = csv.DictReader(text.splitlines())
    for row in reader:
        rows.append(row)
    return rows
