# system_info.py
import requests


def get_ip():
    try:
        resp = requests.get("https://api.ipify.org?format=json", timeout=5)
        return resp.json().get("ip", "Unknown")
    except Exception:
        return "Unknown"


def get_location():
    try:
        resp = requests.get("https://ipapi.co/json/", timeout=5)
        data = resp.json()
        return {
            "city": data.get("city", "Unknown"),
            "region": data.get("region", "Unknown"),
            "country": data.get("country_name", "Unknown"),
        }
    except Exception:
        return {"city": "Unknown", "region": "Unknown", "country": "Unknown"}


def system_check():
    try:
        requests.get("https://www.google.com", timeout=5)
        internet = True
    except Exception:
        internet = False

    return {"Internet": internet}
