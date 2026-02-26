# geo.py
from system_info import get_location


def auto_select_provider():
    loc = get_location()
    country = loc.get("country", "").lower()

    if "australia" in country:
        return "australia"
    if "new zealand" in country:
        return "new_zealand"
    if "united kingdom" in country or "england" in country:
        return "united_kingdom"
    if country in ("france", "germany", "spain", "italy", "netherlands"):
        return "european_union"
    if "canada" in country:
        return "canada"

    return None
