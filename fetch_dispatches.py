"""Fetch and persist acute HVI dispatches from Google News RSS."""

import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

SEARCHES = {
    "US": {
        "query": "United States (labor strike OR inflation OR federal debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "GB": {
        "query": "United Kingdom (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-GB",
        "region": "GB",
        "edition": "GB:en",
    },
    "FR": {
        "query": "France (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "FR",
        "edition": "FR:en",
    },
    "DE": {
        "query": "Germany (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "MX": {
        "query": "Mexico (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "CN": {
        "query": "China (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "JP": {
        "query": "Japan (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-US",
        "region": "US",
        "edition": "US:en",
    },
    "IN": {
        "query": "India (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-IN",
        "region": "IN",
        "edition": "IN:en",
    },
    "IT": {
        "query": "Italy (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "IT",
        "edition": "IT:en",
    },
}


def rss_url(search):
    """Build a Google News RSS URL for one country-specific acute-risk query."""
    parameters = urllib.parse.urlencode({
        "q": search["query"],
        "hl": search["language"],
        "gl": search["region"],
        "ceid": search["edition"],
    })
    return f"https://news.google.com/rss/search?{parameters}"


def text_of(item, tag):
    element = item.find(tag)
    return element.text.strip() if element is not None and element.text else ""


def fetch_dispatches(country_code):
    """Return the first two usable Google News dispatches for a country."""
    search = SEARCHES[country_code]
    request = urllib.request.Request(
        rss_url(search),
        headers={"User-Agent": "VampiricIndexDispatchFetcher/1.0"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        root = ET.fromstring(response.read())

    dispatches = []
    for item in root.findall("./channel/item"):
        title = text_of(item, "title")
        url = text_of(item, "link")
        publication_date = text_of(item, "pubDate")
        source = text_of(item, "source")
        if not all((title, source, publication_date, url)):
            continue
        dispatches.append({
            "title": title,
            "source": source,
            "publication_date": publication_date,
            "url": url,
        })
        if len(dispatches) == 2:
            break
    return dispatches


def print_dispatches(countries):
    for country in countries:
        print(f"{country['country_code']} — {country['name']}")
        for dispatch in country["acute_dispatch"]:
            print(f"  - {dispatch['title']}")
            print(f"    {dispatch['source']} | {dispatch['publication_date']}")
            print(f"    {dispatch['url']}")


def main():
    path = sys.argv[1] if len(sys.argv) == 2 else "data.json"
    if len(sys.argv) > 2:
        print("Usage: python3 fetch_dispatches.py [data.json]", file=sys.stderr)
        return 2

    try:
        with open(path, encoding="utf-8") as data_file:
            payload = json.load(data_file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Unable to load {path}: {error}", file=sys.stderr)
        return 1

    countries = payload.get("countries") if isinstance(payload, dict) else None
    if not isinstance(countries, list):
        print("data.json must contain a countries array.", file=sys.stderr)
        return 1

    errors = []
    fetched = {}
    for country in countries:
        code = country.get("country_code") if isinstance(country, dict) else None
        if code not in SEARCHES:
            errors.append(f"Unsupported or missing country code: {code!r}")
            continue
        try:
            dispatches = fetch_dispatches(code)
        except (OSError, ET.ParseError) as error:
            errors.append(f"{code}: unable to fetch RSS feed: {error}")
            continue
        if not dispatches:
            errors.append(f"{code}: RSS feed contained no usable headlines")
            continue
        fetched[code] = dispatches

    if errors:
        print("Dispatch update failed; data.json was not changed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    for country in countries:
        country["acute_dispatch"] = fetched[country["country_code"]]

    try:
        with open(path, "w", encoding="utf-8") as data_file:
            json.dump(payload, data_file, indent=2, ensure_ascii=False)
            data_file.write("\n")
    except OSError as error:
        print(f"Unable to write {path}: {error}", file=sys.stderr)
        return 1

    print_dispatches(countries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
