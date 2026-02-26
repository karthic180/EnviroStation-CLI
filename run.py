import os
import sys

from providers import PROVIDERS
from api_client import (
    fetch_stations,
    fetch_measures_for_station,
    fetch_readings_for_measure,
)
from mapping import map_stations, map_measures, map_readings
from search_menu import search_menu


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress Enter to continue...")


def choose_provider():
    print("\n=== Select Provider ===")
    for i, pid in enumerate(PROVIDERS.keys(), start=1):
        print(f"{i}) {pid} — {PROVIDERS[pid].name}")
    print("0) Back")

    choice = input("\nSelect provider: ").strip()
    if choice == "0":
        return None

    try:
        index = int(choice) - 1
        return list(PROVIDERS.keys())[index]
    except Exception:
        print("Invalid choice.")
        pause()
        return None


def region_search_menu(provider, stations):
    region = input("Enter region/state/province/country code: ").strip().lower()
    results = [
        s for s in stations
        if s.get("region") and region in str(s["region"]).lower()
    ]

    if not results:
        print("No stations found for that region.")
        pause()
        return None

    print(f"\nFound {len(results)} stations:")
    for i, s in enumerate(results[:20], start=1):
        print(f"{i}) {s['label']} ({s['region']})")

    choice = input("\nSelect station: ").strip()
    try:
        return results[int(choice) - 1]
    except Exception:
        print("Invalid choice.")
        pause()
        return None


def search_stations_menu(provider, stations):
    q = input("Enter search text (name/river/town/id): ").strip().lower()
    results = [
        s for s in stations
        if q in str(s.get("label", "")).lower()
        or q in str(s.get("town", "")).lower()
        or q in str(s.get("river", "")).lower()
        or q in str(s.get("station_id", "")).lower()
    ]

    if not results:
        print("No stations found.")
        pause()
        return None

    print(f"\nFound {len(results)} stations:")
    for i, s in enumerate(results[:20], start=1):
        print(f"{i}) {s['label']} ({s['station_id']})")

    choice = input("\nSelect station: ").strip()
    try:
        return results[int(choice) - 1]
    except Exception:
        print("Invalid choice.")
        pause()
        return None


def explore_station(provider, station):
    station_uri = station["station_uri"]
    clear_screen()
    print(f"=== Measures for {station['label']} ({provider}) ===")

    measures_raw = fetch_measures_for_station(provider, station_uri)
    measures = map_measures(provider, measures_raw)

    if not measures:
        print("No measures found.")
        pause()
        return

    for i, m in enumerate(measures[:20], start=1):
        print(f"{i}) {m['measure_id']}")

    choice = input("\nSelect measure: ").strip()
    try:
        measure = measures[int(choice) - 1]
    except Exception:
        print("Invalid choice.")
        pause()
        return

    clear_screen()
    print(f"=== Readings for measure {measure['measure_id']} ===")

    readings_raw = fetch_readings_for_measure(provider, measure["measure_uri"])
    readings = map_readings(provider, readings_raw, measure["measure_id"])

    if not readings:
        print("No readings available.")
        pause()
        return

    for r in readings[:20]:
        print(f"{r['date']} → {r['value']}")

    pause()


def explore_hydrology():
    provider = choose_provider()
    if not provider:
        return

    clear_screen()
    print(f"=== Hydrology Explorer ({provider}) ===")

    stations_raw = fetch_stations(provider)
    stations = map_stations(provider, stations_raw)

    if not stations:
        print("No stations found.")
        pause()
        return

    while True:
        clear_screen()
        print(f"=== Hydrology Explorer ({provider}) ===")
        print("1) List first 20 stations")
        print("2) Search by region/state/province")
        print("3) Search by name/river/town/id")
        print("0) Back")

        choice = input("\nSelect: ").strip()

        if choice == "1":
            for i, s in enumerate(stations[:20], start=1):
                print(f"{i}) {s['label']} ({s['station_id']})")
            sel = input("\nSelect station: ").strip()
            try:
                station = stations[int(sel) - 1]
                explore_station(provider, station)
            except Exception:
                print("Invalid choice.")
                pause()

        elif choice == "2":
            station = region_search_menu(provider, stations)
            if station:
                explore_station(provider, station)

        elif choice == "3":
            station = search_stations_menu(provider, stations)
            if station:
                explore_station(provider, station)

        elif choice == "0":
            return
        else:
            print("Invalid choice.")
            pause()


def admin_menu():
    print("\n=== Admin Menu ===")
    print("1) Clear DB (if used)")
    print("0) Back")

    choice = input("\nSelect option: ").strip()

    if choice == "1":
        try:
            os.remove("data/env_explorer.db")
            print("Database cleared (if it existed).")
        except FileNotFoundError:
            print("No DB file found.")
        pause()


def test_runner():
    print("\nLaunching test runner...")
    os.system("python run_tests.py")
    pause()


def main_menu():
    while True:
        clear_screen()
        print("=== EnviroStation CLI ===")
        print("1) Hydrology Explorer")
        print("2) Web Search")
        print("3) Admin Tools")
        print("4) Run Tests")
        print("0) Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            explore_hydrology()
        elif choice == "2":
            search_menu()
        elif choice == "3":
            admin_menu()
        elif choice == "4":
            test_runner()
        elif choice == "0":
            print("Goodbye.")
            sys.exit(0)
        else:
            print("Invalid choice.")
            pause()


if __name__ == "__main__":
    main_menu()
