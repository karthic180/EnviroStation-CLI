import requests

def search_for_provider(api_key: str, cx: str, query: str) -> list[str]:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
    }
    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    urls = []
    for item in data.get("items", []):
        link = item.get("link")
        if link and any(ext in link for ext in [".json", ".csv", "/api/", "/services/"]):
            urls.append(link)

    return urls[:10]  # return top 10 candidates
