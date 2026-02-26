import requests
from requests.adapters import HTTPAdapter, Retry
from functools import lru_cache
from providers import PROVIDERS


# Create a session with retry logic
def _create_session():
    session = requests.Session()

    retries = Retry(
        total=3,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retries)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


SESSION = _create_session()


@lru_cache(maxsize=32)
def fetch_stations(provider_id: str):
    """
    Fetch station metadata from a provider.
    Cached + retried.
    """
    if provider_id not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider_id}")

    url = PROVIDERS[provider_id]["stations"]
    timeout = PROVIDERS[provider_id].get("timeout", 10)

    try:
        response = SESSION.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch stations from {provider_id}: {e}")


@lru_cache(maxsize=128)
def fetch_readings(provider_id: str, station_id: str):
    """
    Fetch readings for a specific station.
    Cached + retried.
    """
    if provider_id not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider_id}")

    base = PROVIDERS[provider_id]["readings"]
    timeout = PROVIDERS[provider_id].get("timeout", 10)

    url = f"{base}/{station_id}"

    try:
        response = SESSION.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise RuntimeError(
            f"Failed to fetch readings for station {station_id} from {provider_id}: {e}"
        )
