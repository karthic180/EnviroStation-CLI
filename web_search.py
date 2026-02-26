import requests


def search_web(query: str):
    url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_redirect": 1}

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()
    data = r.json()

    return {
        "heading": data.get("Heading"),
        "abstract": data.get("Abstract"),
        "url": data.get("AbstractURL"),
        "related": [
            t.get("Text") for t in data.get("RelatedTopics", []) if isinstance(t, dict)
        ],
    }


def search_wikipedia(title: str):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"

    r = requests.get(url, timeout=10)
    if r.status_code == 404:
        return None

    r.raise_for_status()
    data = r.json()

    return {
        "title": data.get("title"),
        "extract": data.get("extract"),
        "url": data.get("content_urls", {}).get("desktop", {}).get("page"),
    }
