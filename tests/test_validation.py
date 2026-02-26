from validation import validate_station_id

def test_valid_ids():
    assert validate_station_id("ABC123")
    assert validate_station_id("station_01")

def test_invalid_ids():
    assert not validate_station_id("DROP TABLE;")
    assert not validate_station_id("bad{}id")
