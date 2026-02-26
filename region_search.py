from rapidfuzz import fuzz, process

# ------------------------------------------------------------
# Fallback region lists (used when API metadata is incomplete)
# ------------------------------------------------------------

FALLBACK_AU_REGIONS = [
    "New South Wales", "Victoria", "Queensland", "South Australia",
    "Western Australia", "Tasmania", "Northern Territory",
    "Australian Capital Territory"
]

FALLBACK_NZ_REGIONS = [
    "Northland", "Auckland", "Waikato", "Bay of Plenty", "Gisborne",
    "Hawke's Bay", "Taranaki", "Manawatū‑Whanganui", "Wellington",
    "Tasman", "Nelson", "Marlborough", "West Coast", "Canterbury",
    "Otago", "Southland"
]

FALLBACK_UK_REGIONS = [
    "Thames", "Severn", "Humber", "Anglian", "North West", "South West",
    "Northumbria", "Wessex", "Solent and South Downs",
    "River Thames", "River Avon", "River Trent", "River Severn",
    "River Ouse", "River Tyne", "River Mersey", "River Dee"
]

FALLBACK_EU_COUNTRIES = [
    "France", "Germany", "Spain", "Italy", "Netherlands", "Belgium",
    "Sweden", "Finland", "Poland", "Portugal", "Austria", "Ireland",
    "Greece", "Denmark", "Czech Republic", "Slovakia", "Hungary",
    "Romania", "Bulgaria", "Croatia", "Slovenia", "Estonia", "Latvia",
    "Lithuania", "Luxembourg", "Cyprus", "Malta"
]


# ------------------------------------------------------------
# Fuzzy helpers
# ------------------------------------------------------------

def fuzzy_find_best(query: str, choices: list[str], threshold: int = 60):
    """Return the best fuzzy match above threshold."""
    if not choices:
        return None
    result = process.extractOne(query, choices, scorer=fuzz.WRatio)
    if result and result[1] >= threshold:
        return result[0]
    return None


def fuzzy_filter(query: str, choices: list[str], threshold: int = 60):
    """Return all fuzzy matches above threshold."""
    results = process.extract(query, choices, scorer=fuzz.WRatio)
    return [item for item, score, _ in results if score >= threshold]


# ------------------------------------------------------------
# Dynamic region extraction from station metadata
# ------------------------------------------------------------

def extract_regions_from_metadata(provider_id: str, stations: list[dict]):
    """
    Extract region-like fields from station metadata.
    This is dynamic and adapts to whatever the API returns.
    """
    regions = set()

    for s in stations:
        for key in ("region", "catchment", "catchmentName", "riverName", "country", "Country"):
            if key in s and s[key]:
                regions.add(str(s[key]).strip())

    # Remove junk
    regions = {r for r in regions if len(r) > 1}

    return sorted(regions)


# ------------------------------------------------------------
# Fallback region selection
# ------------------------------------------------------------

def get_fallback_regions(provider_id: str):
    if provider_id == "australia":
        return FALLBACK_AU_REGIONS
    if provider_id == "new_zealand":
        return FALLBACK_NZ_REGIONS
    if provider_id == "united_kingdom":
        return FALLBACK_UK_REGIONS
    if provider_id == "european_union":
        return FALLBACK_EU_COUNTRIES
    return []


# ------------------------------------------------------------
# Region list selection (dynamic or fallback)
# ------------------------------------------------------------

def get_region_list(provider_id: str, stations: list[dict]):
    """
    Returns (regions, source)
    source = "dynamic" or "fallback"
    """
    dynamic = extract_regions_from_metadata(provider_id, stations)

    # If dynamic list is good enough, use it
    if dynamic and len(dynamic) >= 3:
        return dynamic, "dynamic"

    # Otherwise fallback
    fallback = get_fallback_regions(provider_id)
    return fallback, "fallback"


# ------------------------------------------------------------
# Region filtering
# ------------------------------------------------------------

def filter_stations_by_region(stations: list[dict], region_query: str):
    """
    Fuzzy match region/catchment/river fields.
    """
    filtered = []

    for s in stations:
        fields = []
        for key in ("region", "catchment", "catchmentName", "riverName", "country", "Country"):
            if key in s and s[key]:
                fields.append(str(s[key]))

        for f in fields:
            if fuzz.WRatio(region_query, f) >= 60:
                filtered.append(s)
                break

    return filtered


# ------------------------------------------------------------
# Postcode / ZIP / town filtering
# ------------------------------------------------------------

def filter_stations_by_postcode(stations: list[dict], query: str):
    """
    Fuzzy match name, station ID, region, catchment, etc.
    Useful for postcode, ZIP, town, or partial name searches.
    """
    filtered = []

    for s in stations:
        fields = []
        for key in ("name", "station", "region", "catchment", "catchmentName", "riverName"):
            if key in s and s[key]:
                fields.append(str(s[key]))

        for f in fields:
            if fuzz.WRatio(query, f) >= 60:
                filtered.append(s)
                break

    return filtered
