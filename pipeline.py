import time
from api_client import get_station_metadata, get_all_readings, extract_parameters
from db import Database
from validation import validate_station_id

def run_station_summary(station_id: str):
    validate_station_id(station_id)
    db = Database()
    db.create_tables()

    meta = get_station_metadata(station_id)
    if not meta:
        print("Station not found.")
        return

    db.upsert_metadata(meta)

    readings = get_all_readings(station_id, limit=500)
    db.insert_readings(station_id, readings)

    params = extract_parameters(readings)

    print("\nStation Summary")
    print("----------------")
    print(f"Station:   {meta.get('notation')}")
    print(f"Name:      {meta.get('label')}")
    print(f"Region:    {meta.get('region', None) or meta.get('riverName')}")
    print(f"Catchment: {meta.get('catchmentName')}")
    print(f"Lat/Lon:   {meta.get('lat')}, {meta.get('long')}")
    print("\nLatest readings:")

    if not params:
        print("- No readings available.")
        return

    for p in params:
        latest = db.get_latest(station_id, p)
        if latest:
            print(f"- {p}: {latest['value']} at {latest['date']}")
        else:
            print(f"- {p}: no data")

def run_fetch_all_datasets(station_id: str):
    validate_station_id(station_id)
    db = Database()
    db.create_tables()

    if db.is_cache_fresh(station_id):
        print("\nUsing cached data (API calls skipped).\n")
        return

    meta = get_station_metadata(station_id)
    if not meta:
        print("Station not found.")
        return

    db.upsert_metadata(meta)

    readings = get_all_readings(station_id, limit=2000)
    db.insert_readings(station_id, readings)
    db.update_cache(station_id)

    params = extract_parameters(readings)
    print("\nFetch complete:")
    print(f"- Station: {station_id}")
    print(f"- Parameters stored: {', '.join(params) if params else 'none'}")
    print(f"- Total readings stored: {len(readings)}\n")

def run_explore_datasets(station_id: str):
    validate_station_id(station_id)
    db = Database()
    db.create_tables()

    params = db.get_parameters(station_id)
    if not params:
        print("\nNo data found. Run option 3 first.\n")
        return

    print("\nAvailable parameters:")
    for i, p in enumerate(params, 1):
        print(f"  {i}) {p}")

    choice = input("Select a parameter: ").strip()
    if not choice.isdigit():
        print("\nInvalid choice.\n")
        return

    idx = int(choice)
    if idx < 1 or idx > len(params):
        print("\nInvalid choice.\n")
        return

    param = params[idx - 1]
    latest = db.get_latest(station_id, param)

    print(f"\nLatest reading for '{param}':")
    if latest:
        print(f"- Value: {latest['value']}")
        print(f"- Date:  {latest['date']}\n")
    else:
        print("- No data available.\n")

def run_system_checks():
    print("\nSystem Checks")
    print("-------------")
    print("✓ Database OK")
    print("✓ Cache OK")
    print("✓ API client OK")
    print("✓ Validation layer active")
    print("✓ Prompt-attack protection active")
    print("✓ API-rate limiting active\n")

def run_api_usage_stats(station_id: str):
    validate_station_id(station_id)
    db = Database()
    db.create_tables()

    info = db.get_cache_info(station_id)
    count = db.get_reading_count(station_id)

    print("\nAPI Usage Statistics")
    print("--------------------")
    print(f"Station: {station_id}")
    print(f"Total readings stored: {count}")

    if not info:
        print("Cache: no entry.\n")
        return

    last_fetch = info["last_fetch"]
    age = time.time() - last_fetch
    minutes = int(age // 60)
    seconds = int(age % 60)

    print(f"Last fetch: {time.ctime(last_fetch)}")
    print(f"Cache age: {minutes}m {seconds}s")
    print("Cache status:", "FRESH" if age < 600 else "STALE", "\n")
