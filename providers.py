class Provider:
    def __init__(self, name, stations, measures=None, readings=None, fmt="json", timeout=10, region=None):
        self.name = name
        self.stations = stations
        self.measures = measures
        self.readings = readings
        self.format = fmt
        self.timeout = timeout
        self.region = region


PROVIDERS = {
    "united_kingdom": Provider(
        name="United Kingdom – EA Hydrology CSV",
        stations="https://environment.data.gov.uk/hydrology/id/stations.csv",
        measures="https://environment.data.gov.uk/hydrology/id/measures.csv",
        readings="https://environment.data.gov.uk/hydrology/data/readings.csv",
        fmt="csv",
        region="uk",
    ),

    "australia": Provider(
        name="Australia – Bureau of Meteorology (JSON)",
        stations="http://www.bom.gov.au/fwo/IDZ00054.json",
        readings="http://www.bom.gov.au/fwo",
        fmt="json",
        region="aus",
    ),

    "canada": Provider(
        name="Canada – Hydrometric CSV",
        stations="https://dd.weather.gc.ca/hydrometric/csv/stations.csv",
        readings="https://dd.weather.gc.ca/hydrometric/csv",
        fmt="csv",
        region="ca",
    ),
}
