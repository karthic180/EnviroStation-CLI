# mapping.py
"""
Mapping functions convert raw API responses into a standard format.

Each provider may have different field names.
These functions normalize them.
"""

from providers import PROVIDERS, DYNAMIC_PROVIDERS


# ------------------------------------------------------------
# Station mapping
# ------------------------------------------------------------

def map_stations(provider_id: str, raw):
    """
    Convert raw station metadata into a standard structure.
    This is a template — adjust per provider as needed.
    """
    mapped = []

    for item in raw:
        station = (
            item.get("station")
            or item.get("stationId")
            or item.get("id")
            or item.get("site")
            or item.get("code")
        )

        name = (
            item.get("name")
            or item.get("stationName")
            or item.get("siteName")
            or station
        )

        region = (
            item.get("region")
            or item.get("catchment")
            or item.get("catchmentName")
            or item.get("riverName")
        )

        lat = (
            item.get("lat")
            or item.get("latitude")
            or item.get("y")
        )

        lon = (
            item.get("lon")
            or item.get("lng")
            or item.get("longitude")
            or item.get("x")
        )

        mapped.append({
            "station": station,
            "name": name,
            "region": region,
            "catchment": item.get("catchment") or item.get("catchmentName"),
            "lat": lat,
            "lon": lon,
        })

    return mapped


# ------------------------------------------------------------
# Reading mapping
# ------------------------------------------------------------

def map_readings(provider_id: str, raw, station_id: str):
    """
    Convert raw readings into tuples:
    (station, parameter, date, value)
    """
    mapped = []

    for item in raw:
        value = (
            item.get("value")
            or item.get("reading")
            or item.get("level")
            or item.get("flow")
            or item.get("discharge")
        )

        date = (
            item.get("date")
            or item.get("datetime")
            or item.get("time")
            or item.get("timestamp")
        )

        parameter = (
            item.get("parameter")
            or item.get("type")
            or "water_level"
        )

        if value is None or date is None:
            continue

        mapped.append((station_id, parameter, date, float(value)))

    return mapped
