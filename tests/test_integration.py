from system_info import get_location
from geo import auto_select_provider

def test_location_lookup():
    loc = get_location()
    assert "country" in loc

def test_auto_provider():
    provider = auto_select_provider()
    assert provider is None or isinstance(provider, str)
