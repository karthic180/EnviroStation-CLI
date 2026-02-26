# tests_internal.py
# Comprehensive internal test suite for EnviroStation CLI

from providers import PROVIDERS
from system_info import get_ip, get_location, system_check
from geo import auto_select_provider
from api_client import fetch_stations, fetch_readings
from mapping import map_stations, map_readings
from region_search import (
    extract_regions_from_metadata,
    get_region_list,
    filter_stations_by_region,
    filter_stations_by_postcode,
)
from db import (
    init_db,
    get_conn,
    insert_readings,
    update_cache,
    get_last_fetch,
)
import time


# ------------------------------------------------------------
# BASIC SYSTEM TESTS
# ------------------------------------------------------------

def smoke_test_basic_system():
    """Check internet, IP lookup, location lookup, provider count."""
    return {
        "internet": system_check().get("Internet", False),
        "ip_lookup": get_ip() != "Unknown",
        "location_lookup": get_location().get("country") != "Unknown",
        "provider_count": len(PROVIDERS),
    }


def smoke_test_providers():
    """Ensure provider definitions exist."""
    return {
        "provider_keys": list(PROVIDERS.keys()),
        "provider_count": len(PROVIDERS),
    }


# ------------------------------------------------------------
# AUTO PROVIDER TEST
# ------------------------------------------------------------

def e2e_test_auto_provider():
    """Check auto provider detection."""
    return {"auto_provider": auto_select_provider()}


# ------------------------------------------------------------
# STATION FETCH TEST
# ------------------------------------------------------------

def e2e_test_station_fetch(provider_id="australia", sample_limit=3):
    """Fetch stations and map them."""
    try:
        raw = fetch_stations(provider_id)
        mapped = map_stations(provider_id, raw)
        sample = mapped[:sample_limit] if isinstance(mapped, list) else []
        return {
            "provider": provider_id,
            "station_count": len(mapped) if isinstance(mapped, list) else 0,
            "sample": sample,
        }
    except Exception as e:
        return {"provider": provider_id, "error": str(e)}


# ------------------------------------------------------------
# READING FETCH TEST
# ------------------------------------------------------------

def e2e_test_reading_fetch(provider_id="australia", station_id=None, sample_limit=3):
    """Fetch readings for a station and map them."""
    try:
        raw_stations = fetch_stations(provider_id)
        mapped = map_stations(provider_id, raw_stations)
        if not mapped:
            return {"provider": provider_id, "error": "No stations available"}

        station = station_id or mapped[0].get("station")
        raw_readings = list(fetch_readings(provider_id, station))
        mapped_readings = map_readings(provider_id, raw_readings, station)

        return {
            "provider": provider_id,
            "station": station,
            "reading_count": len(mapped_readings),
            "sample": mapped_readings[:sample_limit],
        }
    except Exception as e:
        return {"provider": provider_id, "error": str(e)}


# ------------------------------------------------------------
# REGION EXTRACTION TESTS
# ------------------------------------------------------------

def test_region_extraction(provider_id="united_kingdom"):
    """Test dynamic region extraction + fallback logic."""
    try:
        raw = fetch_stations(provider_id)
        mapped = map_stations(provider_id, raw)

        dynamic = extract_regions_from_metadata(provider_id, mapped)
        final_regions, source = get_region_list(provider_id, mapped)

        return {
            "provider": provider_id,
            "dynamic_region_count": len(dynamic),
            "final_region_count": len(final_regions),
            "source": source,
        }
    except Exception as e:
        return {"provider": provider_id, "error": str(e)}


def test_region_filter(provider_id="australia"):
    """Test fuzzy region filtering."""
    try:
        raw = fetch_stations(provider_id)
        mapped = map_stations(provider_id, raw)

        regions, _ = get_region_list(provider_id, mapped)
        if not regions:
            return {"provider": provider_id, "error": "No regions available"}

        query = regions[0][:4]  # fuzzy partial
        filtered = filter_stations_by_region(mapped, query)

        return {
            "provider": provider_id,
            "query": query,
            "match_count": len(filtered),
        }
    except Exception as e:
        return {"provider": provider_id, "error": str(e)}


# ------------------------------------------------------------
# POSTCODE / TOWN SEARCH TEST
# ------------------------------------------------------------

def test_postcode_filter(provider_id="australia"):
    """Test fuzzy postcode/town search."""
    try:
        raw = fetch_stations(provider_id)
        mapped = map_stations(provider_id, raw)

        if not mapped:
            return {"provider": provider_id, "error": "No stations available"}

        sample_name = mapped[0].get("name", "") or mapped[0].get("station", "")
        query = sample_name[:4]

        filtered = filter_stations_by_postcode(mapped, query)

        return {
            "provider": provider_id,
            "query": query,
            "match_count": len(filtered),
        }
    except Exception as e:
        return {"provider": provider_id, "error": str(e)}


# ------------------------------------------------------------
# DATABASE INTEGRITY TESTS
# ------------------------------------------------------------

def test_db_integrity():
    """Ensure DB tables exist."""
    try:
        init_db()
        conn = get_conn()
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        tables = [row[0] for row in cur.fetchall()]
        conn.close()

        return {
            "tables": tables,
            "has_metadata": "metadata" in tables,
            "has_readings": "readings" in tables,
            "has_cache": "cache" in tables,
        }
    except Exception as e:
        return {"error": str(e)}


def test_db_insert_and_cache():
    """Insert fake reading + update cache."""
    try:
        init_db()
        now = int(time.time())

        insert_readings([
            ("TEST_STATION", "water_level", "2024-01-01T00:00:00Z", 1.23)
        ])

        update_cache("TEST_STATION", now)
        last = get_last_fetch("TEST_STATION")

        return {
            "cache_updated": last == now,
            "last_fetch": last,
        }
    except Exception as e:
        return {"error": str(e)}


# ------------------------------------------------------------
# API REACHABILITY TEST
# ------------------------------------------------------------

def test_api_reachability(provider_id="australia"):
    """Check if provider API is reachable."""
    try:
        raw = fetch_stations(provider_id)
        return {
            "provider": provider_id,
            "reachable": isinstance(raw, list) and len(raw) > 0,
        }
    except Exception as e:
        return {"provider": provider_id, "error": str(e)}


# ------------------------------------------------------------
# FULL TEST SUITE
# ------------------------------------------------------------

def run_all_tests():
    """Run all internal tests and return a dict of results."""
    return {
        "smoke_basic": smoke_test_basic_system(),
        "smoke_providers": smoke_test_providers(),
        "e2e_auto_provider": e2e_test_auto_provider(),
        "e2e_station_fetch": e2e_test_station_fetch(),
        "e2e_reading_fetch": e2e_test_reading_fetch(),
        "region_extraction": test_region_extraction(),
        "region_filter": test_region_filter(),
        "postcode_filter": test_postcode_filter(),
        "db_integrity": test_db_integrity(),
        "db_insert_and_cache": test_db_insert_and_cache(),
        "api_reachability": test_api_reachability(),
    }
MOCK_STATIONS = [
    {
        "station": "TEST001",
        "name": "Mock River Station",
        "region": "Mockland",
        "catchment": "Mock Catchment",
        "lat": -33.0,
        "lon": 151.0,
    },
    {
        "station": "TEST002",
        "name": "Fake Creek Station",
        "region": "Mockland",
        "catchment": "Fake Catchment",
        "lat": -34.0,
        "lon": 150.0,
    }
]

MOCK_READINGS = [
    {"value": 1.23, "date": "2024-01-01T00:00:00Z"},
    {"value": 1.45, "date": "2024-01-01T01:00:00Z"},
]
