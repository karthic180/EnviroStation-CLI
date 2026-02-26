import pytest
from api_client import fetch_stations, fetch_readings
from mapping import map_stations, map_readings

@pytest.mark.online
def test_online_provider():
    stations = fetch_stations("australia")
    assert len(stations) > 0

    mapped = map_stations("australia", stations)
    station_id = mapped[0]["station"]

    readings = fetch_readings("australia", station_id)
    mapped_r = map_readings("australia", readings, station_id)

    assert len(mapped_r) > 0
