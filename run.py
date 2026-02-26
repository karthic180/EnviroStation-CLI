# run.py
import time
import json

from providers import PROVIDERS, DYNAMIC_PROVIDERS
from system_info import get_ip, get_location, system_check
from geo import auto_select_provider
from ai_search import (
    ai_search_for_provider,
    choose_ai_search_country,
    is_valid_hydrology_api,
    preview_api_metadata,
)
from api_client import fetch_stations, fetch_readings
from mapping import map_stations, map_readings
from db import (
    init_db,
    insert_readings,
    get_last_fetch,
    update_cache,
    get_all_cache,
    purge_stale_cache,
)
from tests_internal import run_all_tests
from region_search import (
    get_region_list,
    filter_stations_by_region,
    filter_stations_by_postcode,
)
from db_tools import (
    db_count_rows,
    db_show_last_readings,
    db_show_stations,
    db_vacuum,
)


# ------------------------------------------------------------
# Load config
# ------------------------------------------------------------

def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except Exception:
        return {"cache_days": 7}


CONFIG = load_config()
CACHE_DAYS = int(CONFIG.get("cache_days", 7))
CACHE_SECONDS = CACHE_DAYS * 24 * 60 * 60


# ------------------------------------------------------------
# Helper: Suggest SQLite Viewer
# ------------------------------------------------------------

def suggest_sqlite_viewer():
    print("""
Tip: You can view your local database using a SQLite viewer.

Recommended (VS Code Extension):
  SQLite Viewer by Florian Klampfer
  https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer

This lets you browse tables, inspect readings, and debug data directly inside VS Code.
""")


# ------------------------------------------------------------
# Front Page
# ------------------------------------------------------------

def show_front_page() -> str | None:
    ip = get_ip()
    loc = get_location()
    checks = system_check()
    auto = auto_select_provider()

    print("\nEnvironmental Data Explorer")
    print("---------------------------")
    print(f"System Status: {'OK' if all(checks.values()) else 'Some checks failed'}")
    print(f"Your IP Address: {ip}")
    print(f"Detected Location: {loc['city']}, {loc['region']}, {loc['country']}")
    print(f"Auto-Provider: {auto if auto else 'None (manual selection required)'}")
    print()

    return auto


# ------------------------------------------------------------
# Add Custom Provider (manual URL)
# ------------------------------------------------------------

def add_custom_provider() -> str | None:
    url = input("\nPaste API URL (stations/readings JSON or CSV): ").strip()
    if not url.startswith(("http://", "https://")):
        print("Invalid URL.")
        return None

    provider_id = f"custom_{len(DYNAMIC_PROVIDERS)+1}"
    DYNAMIC_PROVIDERS[provider_id] = {
        "name": f"Custom Provider {provider_id}",
        "stations_json": url,
        "readings_json": url,
    }

    print(f"Added provider: {provider_id}")
    return provider_id


# ------------------------------------------------------------
# Add Provider via AI Search
# ------------------------------------------------------------

def add_ai_country_provider() -> str | None:
    country = choose_ai_search_country()
    if not country:
        print("Cancelled.")
        return None

    print(f"\nSearching for hydrology APIs for: {country}")
    candidates = ai_search_for_provider(country)

    if not candidates:
        print("No API-like URLs found.")
        return None

    print("\nChecking candidate URLs...\n")
    validated = []
    for url in candidates:
        ok = is_valid_hydrology_api(url)
        status = "VALID " if ok else "INVALID"
        print(f"{status} - {url}")
        if ok:
            validated.append(url)

    if not validated:
        print("\nNo valid hydrology APIs found from AI search.")
        return None

    print("\nValid API endpoints:")
    for i, url in enumerate(validated, 1):
        print(f"{i}) {url}")

    choice = input("\nSelect one (or blank to cancel): ").strip()
    if not choice:
        print("Cancelled.")
        return None

    if not choice.isdigit():
        print("Invalid choice.")
        return None

    idx = int(choice)
    if idx < 1 or idx > len(validated):
        print("Invalid choice.")
        return None

    selected = validated[idx - 1]

    # NEW: Test + preview before adding
    print(f"\nYou selected:\n  {selected}")
    test_choice = input("Test this API and show metadata preview before adding? (y/n): ").strip().lower()
    if test_choice == "y":
        preview_api_metadata(selected)
        confirm = input("\nAdd this API as a provider? (y/n): ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return None

    provider_id = f"user_{country.lower().replace(' ', '_')}"

    DYNAMIC_PROVIDERS[provider_id] = {
        "name": f"User Provider ({country})",
        "stations_json": selected,
        "readings_json": selected,
    }

    print(f"\nAdded provider: {provider_id}")
    return provider_id


# ------------------------------------------------------------
# Provider Selection Menu
# ------------------------------------------------------------

def choose_provider() -> str | None:
    auto = show_front_page()
    if auto:
        print(f"Automatically selected provider: {auto}")
        return auto

    while True:
        print("""
Choose a data source:

1) Australia – Water Data Service
2) New Zealand – Hydrology Data Service
3) Canada – Hydrometric Data
4) United Kingdom – Hydrology Data
5) European Union – Water Quality Data
6) AI Search (current location or another country)
7) Add your own provider (paste URL)
8) Back
""")

        choice = input("Select option: ").strip()

        if choice == "1": return "australia"
        if choice == "2": return "new_zealand"
        if choice == "3": return "canada"
        if choice == "4": return "united_kingdom"
        if choice == "5": return "european_union"
        if choice == "6": return add_ai_country_provider()
        if choice == "7": return add_custom_provider()
        if choice == "8": return None

        print("Invalid option.\n")


# ------------------------------------------------------------
# Region Search Menu
# ------------------------------------------------------------

def region_search_menu(provider_id: str, stations: list[dict]):
    while True:
        print("""
Region Search Menu
------------------
1) Search by region / state / province
2) Search by postcode / ZIP / town
3) Back
""")

        choice = input("Select option: ").strip()

        if choice == "1":
            return region_selection(provider_id, stations)
        elif choice == "2":
            return postcode_search(stations)
        elif choice == "3":
            return None
        else:
            print("Invalid option.")


def region_selection(provider_id: str, stations: list[dict]):
    regions, source = get_region_list(provider_id, stations)

    if source == "dynamic":
        print("\nUsing live dynamic regions from API.\n")
    else:
        print("\nAPI unavailable — using fallback region list.\n")

    print("Available regions (partial list):")
    for r in regions[:20]:
        print(f"- {r}")
    if len(regions) > 20:
        print("... (more available)")

    query = input("\nEnter region name (partial allowed): ").strip()
    matches = filter_stations_by_region(stations, query)

    if not matches:
        print("No stations matched that region.")
        return None

    print(f"\nFound {len(matches)} station(s) in that region.\n")
    return matches


def postcode_search(stations: list[dict]):
    query = input("\nEnter postcode / ZIP / town: ").strip()
    matches = filter_stations_by_postcode(stations, query)

    if not matches:
        print("No stations matched that search.")
        return None

    print(f"\nFound {len(matches)} station(s) matching that search.\n")
    return matches


# ------------------------------------------------------------
# Fetch Data for One Station
# ------------------------------------------------------------

def fetch_one_dataset(provider_id: str, station: str) -> None:
    now = int(time.time())
    last = get_last_fetch(station)

    if last and (now - last) < CACHE_SECONDS:
        days = (now - last) // (24 * 60 * 60)
        print(f"Data is current (last updated {days} day(s) ago). Skipping API fetch.")
        return

    print("Fetching new data from API...")

    raw = list(fetch_readings(provider_id, station))
    rows = map_readings(provider_id, raw, station)

    if not rows:
        print("No readings mapped.")
        return

    insert_readings(rows)
    update_cache(station, now)

    print(f"Stored {len(rows)} readings for station {station}.")
    suggest_sqlite_viewer()


# ------------------------------------------------------------
# Cache Summary + Purge
# ------------------------------------------------------------

def show_cache_summary():
    rows = get_all_cache()
    if not rows:
        print("\nNo cached stations found.\n")
        return

    print("\nCache Summary")
    print("-------------")

    now = int(time.time())

    for station, ts in rows:
        if not ts:
            continue

        age_days = (now - ts) // (24 * 60 * 60)
        status = "FRESH" if (now - ts) < CACHE_SECONDS else "STALE"

        print(f"Station: {station}")
        print(f"  Last Updated: {age_days} day(s) ago")
        print(f"  Status: {status}")
        print()


def auto_purge_stale_cache():
    now = int(time.time())
    cutoff = now - CACHE_SECONDS
    deleted = purge_stale_cache(cutoff)
    print(f"\nAuto-purge complete. Removed {deleted} stale cache entries.\n")


# ------------------------------------------------------------
# User Tests
# ------------------------------------------------------------

def run_tests() -> None:
    print("\nRunning user tests...")
    print("1) System check")
    print(system_check())

    print("\n2) Auto provider detection")
    print(auto_select_provider())

    print("\n3) Location")
    print(get_location())

    print("\nUser tests complete.\n")


# ------------------------------------------------------------
# Database Tools Menu
# ------------------------------------------------------------

def db_tools_menu():
    while True:
        print("""
Database Tools
--------------
1) Count rows in each table
2) Show last 10 readings
3) Show stations in DB
4) Vacuum / optimize DB
5) Back
""")

        choice = input("Select option: ").strip()

        if choice == "1":
            counts = db_count_rows()
            print("\nRow counts:")
            for table, count in counts.items():
                print(f"  {table}: {count}")
            print()

        elif choice == "2":
            rows = db_show_last_readings()
            print("\nLast 10 readings:")
            for r in rows:
                print(r)
            print()

        elif choice == "3":
            rows = db_show_stations()
            print("\nStations in DB:")
            for r in rows:
                print(r)
            print()

        elif choice == "4":
            db_vacuum()
            print("\nDatabase optimized.\n")

        elif choice == "5":
            return

        else:
            print("Invalid option.")


# ------------------------------------------------------------
# Admin Menu
# ------------------------------------------------------------

def admin_menu():
    while True:
        print("""
Admin Menu
----------
1) Run smoke tests
2) Run end-to-end tests
3) Run full internal test suite
4) Database tools
5) Back
""")
        choice = input("Select option: ").strip()

        if choice == "1":
            print("\nRunning smoke tests...\n")
            report = run_all_tests()
            print("SMOKE BASIC:", report.get("smoke_basic"))
            print("SMOKE PROVIDERS:", report.get("smoke_providers"))

        elif choice == "2":
            print("\nRunning end-to-end tests...\n")
            report = run_all_tests()
            print("AUTO PROVIDER:", report.get("e2e_auto_provider"))
            print("STATION FETCH:", report.get("e2e_station_fetch"))
            print("READING FETCH:", report.get("e2e_reading_fetch"))

        elif choice == "3":
            print("\nRunning full internal test suite...\n")
            report = run_all_tests()
            for section, result in report.items():
                print(f"\n[{section}]")
                print(result)

        elif choice == "4":
            db_tools_menu()

        elif choice == "5":
            return

        else:
            print("Invalid option.")


# ------------------------------------------------------------
# Main Menu
# ------------------------------------------------------------

def main() -> None:
    init_db()
    suggest_sqlite_viewer()

    while True:
        print(f"""
Main Menu
---------
1) Select provider
2) User tests
3) Admin tests
4) View cache summary
5) Auto-purge stale cache entries
6) Quit

(Current cache duration: {CACHE_DAYS} day(s))
""")
        choice = input("Select option: ").strip()

        if choice == "1":
            provider_id = choose_provider()
            if not provider_id:
                continue

            raw = fetch_stations(provider_id)
            stations = map_stations(provider_id, raw)

            filtered = region_search_menu(provider_id, stations)
            if not filtered:
                continue

            print("\nFiltered Stations:")
            for i, s in enumerate(filtered[:20], 1):
                print(f"{i}) {s.get('station')} – {s.get('name')}")

            choice = input("\nSelect station number: ").strip()
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(filtered[:20]):
                    station_id = filtered[idx - 1].get("station")
                    fetch_one_dataset(provider_id, station_id)
                else:
                    print("Invalid selection.")

        elif choice == "2":
            run_tests()

        elif choice == "3":
            admin_menu()

        elif choice == "4":
            show_cache_summary()

        elif choice == "5":
            auto_purge_stale_cache()

        elif choice == "6":
            print("Goodbye.")
            return

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
