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
        name="United Kingdom – Environment Agency Hydrology",
        stations="https://environment.data.gov.uk/hydrology/id/stations",
        measures="https://environment.data.gov.uk/hydrology/id/measures",
        readings="https://environment.data.gov.uk/hydrology/id/measures",
        fmt="json",
        region="uk",
    ),
    "new_zealand": Provider(
        name="New Zealand – NIWA Hydrology (simplified)",
        stations="https://api.niwa.co.nz/rainfall/stations",
        readings="https://api.niwa.co.nz/rainfall/data",
        fmt="json",
        region="nz",
    ),
    "australia": Provider(
        name="Australia – Bureau of Meteorology (simplified)",
        stations="http://www.bom.gov.au/fwo/IDZ00054.json",
        readings="http://www.bom.gov.au/fwo",
        fmt="json",
        region="aus",
    ),
    "canada": Provider(
        name="Canada – Hydrometric (simplified)",
        stations="https://dd.weather.gc.ca/hydrometric/csv/stations.csv",
        readings="https://dd.weather.gc.ca/hydrometric/csv",
        fmt="csv",
        region="ca",
    ),
    "europe": Provider(
        name="European Union – EEA Waterbase (simplified)",
        stations="https://water.discomap.eea.europa.eu/arcgis/rest/services/Waterbase/WISE_SoE_Eionet/MapServer/0/query?where=1%3D1&f=json",
        readings="https://water.discomap.eea.europa.eu/arcgis/rest/services/Waterbase/WISE_SoE_Eionet/MapServer/0/query",
        fmt="json",
        region="eu",
    ),
}
