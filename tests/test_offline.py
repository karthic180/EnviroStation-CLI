from mapping import map_stations, map_readings
from region_search import filter_stations_by_region
from validation import validate_station_id

def test_map_stations(mock_stations):
    mapped = map_stations("australia", mock_stations)
    assert mapped[0]["station"] == "TEST001"

def test_map_readings(mock_readings):
    mapped = map_readings("australia", mock_readings, "TEST001")
    assert len(mapped) == 2

def test_region_filter(mock_stations):
    filtered = filter_stations_by_region(mock_stations, "Mock")
    assert len(filtered) == 1

def test_validation():
    assert validate_station_id("ABC123")
    assert not validate_station_id("DROP TABLE;")
