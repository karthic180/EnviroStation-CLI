import re

def validate_station_id(station_id: str) -> bool:
    if not station_id:
        return False

    # Reject dangerous characters
    if re.search(r"[;\"'{}\(\)]", station_id):
        return False

    return True
