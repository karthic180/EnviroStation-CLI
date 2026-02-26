import pytest
from api_client import fetch_stations
from mapping import map_stations


@pytest.mark.online
@pytest.mark.parametrize("provider", ["united_kingdom", "new_zealand", "australia", "canada", "europe"])
def test_online_stations(provider):
    raw = fetch_stations(provider)
    stations = map_stations(provider, raw)
    assert isinstance(stations, list)
