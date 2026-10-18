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
        "query": "United Kingdom economy",
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
    "CA": {
        "query": "Canada (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-CA",
        "region": "CA",
        "edition": "CA:en",
    },
    "RU": {
        "query": "Russia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "US",
        "edition": "US:en",
    },
    "BR": {
        "query": "Brazil (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "BR",
        "edition": "BR:en",
    },
    "KR": {
        "query": "South Korea (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "KR",
        "edition": "KR:en",
    },
    "AU": {
        "query": "Australia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-AU",
        "region": "AU",
        "edition": "AU:en",
    },
    "ES": {
        "query": "Spain (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "ES",
        "edition": "ES:en",
    },
    "ID": {
        "query": "Indonesia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "ID",
        "edition": "ID:en",
    },
    "NL": {
        "query": "Netherlands (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "NL",
        "edition": "NL:en",
    },
    "TR": {
        "query": "Turkey (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "TR",
        "edition": "TR:en",
    },
    "SA": {
        "query": "Saudi Arabia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "SA",
        "edition": "SA:en",
    },
    "CH": {
        "query": "Switzerland labor OR strike OR inflation OR debt",
        "language": "en",
        "region": "CH",
        "edition": "CH:en",
    },
    "PL": {
        "query": "Poland (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "PL",
        "edition": "PL:en",
    },
    "BE": {
        "query": "Belgium inflation",
        "language": "en",
        "region": "BE",
        "edition": "BE:en",
    },
    "AR": {
        "query": "Argentina (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "AR",
        "edition": "AR:en",
    },
    "IE": {
        "query": "Ireland economy",
        "language": "en-IE",
        "region": "IE",
        "edition": "IE:en",
    },
    "SE": {
        "query": "Sweden inflation",
        "language": "en",
        "region": "SE",
        "edition": "SE:en",
    },
    "SG": {
        "query": "Singapore (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-SG",
        "region": "SG",
        "edition": "SG:en",
    },
    "AE": {
        "query": "United Arab Emirates (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "AE",
        "edition": "AE:en",
    },
    "IL": {
        "query": "Israel (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "IL",
        "edition": "IL:en",
    },
    "AT": {
        "query": "Austria inflation",
        "language": "en",
        "region": "AT",
        "edition": "AT:en",
    },
    "TH": {
        "query": "Thailand inflation",
        "language": "en",
        "region": "TH",
        "edition": "TH:en",
    },
    "NO": {
        "query": "Norway inflation",
        "language": "en",
        "region": "NO",
        "edition": "NO:en",
    },
    "VN": {
        "query": "Vietnam inflation",
        "language": "en",
        "region": "VN",
        "edition": "VN:en",
    },
    "IR": {
        "query": "Iran (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "IR",
        "edition": "IR:en",
    },
    "PH": {
        "query": "Philippines inflation",
        "language": "en",
        "region": "PH",
        "edition": "PH:en",
    },
    "BD": {
        "query": "Bangladesh (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "BD",
        "edition": "BD:en",
    },
    "DK": {
        "query": "Denmark economy",
        "language": "en",
        "region": "DK",
        "edition": "DK:en",
    },
    "MY": {
        "query": "Malaysia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "MY",
        "edition": "MY:en",
    },
    "CO": {
        "query": "Colombia (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "CO",
        "edition": "CO:en",
    },
    "ZA": {
        "query": "South Africa (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en-ZA",
        "region": "ZA",
        "edition": "ZA:en",
    },
    "EG": {
        "query": "Egypt (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "EG",
        "edition": "EG:en",
    },
    "RO": {
        "query": "Romania (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "RO",
        "edition": "RO:en",
    },
    "PK": {
        "query": "Pakistan (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "PK",
        "edition": "PK:en",
    },
    "CZ": {
        "query": "Czechia economy",
        "language": "en",
        "region": "CZ",
        "edition": "CZ:en",
    },
    "CL": {
        "query": "Chile economy",
        "language": "en",
        "region": "CL",
        "edition": "CL:en",
    },
    "PT": {
        "query": "Portugal (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "PT",
        "edition": "PT:en",
    },
    "FI": {
        "query": "Finland economy",
        "language": "en",
        "region": "FI",
        "edition": "FI:en",
    },
    "PE": {
        "query": "Peru economy",
        "language": "en",
        "region": "PE",
        "edition": "PE:en",
    },
    "KZ": {
        "query": "Kazakhstan (labor strike OR inflation OR sovereign debt OR protest suppression)",
        "language": "en",
        "region": "KZ",
        "edition": "KZ:en",
    },
    "IQ": {
        "query": "Iraq economy",
        "language": "en",
        "region": "IQ",
        "edition": "IQ:en",
    },
    "DZ": {
        "query": "Algeria economy",
        "language": "en",
        "region": "DZ",
        "edition": "DZ:en",
    },
}

# Google News search is not a structured country filter. A panel must not
# receive a generic or neighboring-country result merely because it matched a
# broad risk term, so publish only headlines that identify the country itself.
COUNTRY_TERMS = {
    "US": ("united states", "u.s.", "u.s.a.", "america", "american"),
    "CN": ("china", "chinese"),
    "DE": ("germany", "german"),
    "JP": ("japan", "japanese"),
    "IN": ("india", "indian"),
    "GB": ("united kingdom", "britain", "british", "england", "english"),
    "FR": ("france", "french", "paris"),
    "IT": ("italy", "italian", "rome"),
    "CA": ("canada", "canadian"),
    "RU": ("russia", "russian", "moscow"),
    "BR": ("brazil", "brazilian"),
    "KR": ("south korea", "korea", "korean", "seoul"),
    "MX": ("mexico", "mexican"),
    "AU": ("australia", "australian"),
    "ES": ("spain", "spanish", "madrid"),
    "ID": ("indonesia", "indonesian", "jakarta"),
    "TR": ("turkey", "turkish", "turkiye", "ankara"),
    "SA": ("saudi", "saudi arabia", "riyadh"),
    "NL": ("netherlands", "dutch", "amsterdam", "the hague"),
    "CH": ("switzerland", "swiss", "geneva", "zurich", "bern"),
    "PL": ("poland", "polish", "warsaw"),
    "BE": ("belgium", "belgian", "brussels"),
    "AR": ("argentina", "argentine", "buenos aires"),
    "IE": ("ireland", "irish", "dublin"),
    "SE": ("sweden", "swedish", "stockholm"),
    "SG": ("singapore", "singaporean"),
    "AE": ("united arab emirates", "emirati", "dubai", "abu dhabi"),
    "IL": ("israel", "israeli", "jerusalem", "tel aviv"),
    "AT": ("austria", "austrian", "vienna"),
    "TH": ("thailand", "thai", "bangkok"),
    "NO": ("norway", "norwegian", "oslo"),
    "VN": ("vietnam", "vietnamese", "hanoi", "ho chi minh"),
    "IR": ("iran", "iranian", "tehran"),
    "PH": ("philippines", "philippine", "filipino", "manila"),
    "BD": ("bangladesh", "bangladeshi", "dhaka"),
    "DK": ("denmark", "danish", "copenhagen"),
    "MY": ("malaysia", "malaysian", "kuala lumpur"),
    "CO": ("colombia", "colombian", "bogota", "bogotá"),
    "ZA": ("south africa", "south african", "pretoria", "cape town", "johannesburg"),
    "EG": ("egypt", "egyptian", "cairo"),
    "RO": ("romania", "romanian", "bucharest"),
    "PK": ("pakistan", "pakistani", "islamabad", "karachi", "lahore"),
    "CZ": ("czechia", "czech republic", "czech", "prague"),
    "CL": ("chile", "chilean", "santiago"),
    "PT": ("portugal", "portuguese", "lisbon"),
    "FI": ("finland", "finnish", "helsinki"),
    "PE": ("peru", "peruvian", "lima"),
    "KZ": ("kazakhstan", "kazakh", "astana", "almaty"),
    "IQ": ("iraq", "iraqi", "baghdad", "basra", "erbil"),
    "DZ": ("algeria", "algerian", "algiers"),
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


def article_headline(title, source):
    """Return the article headline without Google News' publisher suffix."""
    source_suffix = f" - {source}"
    return title[:-len(source_suffix)] if title.endswith(source_suffix) else title


def is_country_relevant(country_code, title, source):
    """Return whether the article headline identifies its assigned country.

    Google News appends `` - Publisher`` to titles. Strip that suffix first so
    a publisher such as France 24 cannot make unrelated Iran coverage appear in
    France's panel.
    """
    normalized_headline = article_headline(title, source).casefold()
    return any(term in normalized_headline for term in COUNTRY_TERMS[country_code])


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
    seen_headlines = set()
    for item in root.findall("./channel/item"):
        title = text_of(item, "title")
        url = text_of(item, "link")
        publication_date = text_of(item, "pubDate")
        source = text_of(item, "source")
        if not all((title, source, publication_date, url)):
            continue
        if not is_country_relevant(country_code, title, source):
            continue
        normalized_headline = article_headline(title, source).casefold()
        if normalized_headline in seen_headlines:
            continue
        seen_headlines.add(normalized_headline)
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
