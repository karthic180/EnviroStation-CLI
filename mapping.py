from helpers import extract_items, safe_get, normalise_float, extract_uuid_from_url


def extract_region(provider_id, item):
    if provider_id == "united_kingdom":
        return item.get("town") or item.get("catchmentName")
    if provider_id == "australia":
        return item.get("state")
    if provider_id == "canada":
        return item.get("Province") or item.get("province")
    return None


def map_stations(provider_id: str, raw):
    items = extract_items(provider_id, raw)
    mapped = []

    for item in items:
        if provider_id == "united_kingdom":
            uri = item.get("stationReference")
            label = item.get("label")

        elif provider_id == "australia":
            uri = item.get("id")
            label = item.get("name")

        elif provider_id == "canada":
            uri = item.get("STATION_NUMBER")
            label = item.get("STATION_NAME")

        else:
            uri = safe_get(item, "@id", "id")
            label = safe_get(item, "label", "name")

        mapped.append(
            {
                "station_uri": uri,
                "station_id": extract_uuid_from_url(uri),
                "label": label,
                "river": safe_get(item, "riverName"),
                "town": safe_get(item, "town"),
                "region": extract_region(provider_id, item),
                "raw": item,
            }
        )

    return mapped


def map_measures(provider_id: str, raw):
    items = extract_items(provider_id, raw)
    mapped = []

    for item in items:
        measure_uri = item.get("measure_uri") or item.get("station")
        mapped.append(
            {
                "measure_uri": measure_uri,
                "measure_id": extract_uuid_from_url(measure_uri),
                "parameter": item.get("parameter"),
                "period": item.get("period"),
                "unit_name": item.get("unitName"),
                "value_type": item.get("valueType"),
                "raw": item,
            }
        )

    return mapped


def map_readings(provider_id: str, raw, measure_id: str):
    items = extract_items(provider_id, raw)
    mapped = []

    for item in items:
        if provider_id == "united_kingdom":
            value = normalise_float(item.get("value"))
            date = item.get