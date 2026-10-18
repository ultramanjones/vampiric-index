"""Refresh the current top-20 nominal-GDP HVI review from documented sources.

The script verifies the World Bank's all-economies 2024 nominal-GDP ranking before
writing. It refreshes the three published WDI inputs and Freedom House's current
country-comparable edition. Legacy pilot scores are never recalibrated here.
"""

import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

GDP_URL = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2024&format=json&per_page=400"
COUNTRIES_URL = "https://api.worldbank.org/v2/country?format=json&per_page=400"
WDI_URL = "https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}?date={year}&format=json&per_page=100"
INDICATORS = {
    "survival_floor": ("SP.DYN.LE00.IN", 2023, "life_expectancy_years", "life expectancy at birth / 4"),
    "sovereign_cannibalization": ("NY.GNP.PCAP.CD", 2024, "gni_per_capita_usd", "GNI per capita, Atlas method/current US$ / 2,000, capped at 25"),
    "labor_retention": ("SL.EMP.TOTL.SP.ZS", 2024, "employment_to_population_percent", "employment-to-population ratio, ages 15+, ILO modeled estimate / 4"),
}
LEGACY_CODES = {"US", "GB", "FR", "DE", "MX"}
USER_AGENT = "VampiricIndexTop20Review/1.0"


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def grade(score):
    if score >= 93:
        return "A"
    if score >= 85:
        return "B"
    if score >= 66:
        return "C"
    if score >= 50:
        return "D"
    return "F"


def freedom_house_score(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        page = response.read().decode("utf-8")
    match = re.search(
        r'<div class="scorecard fiw 2026">.*?<div class="country-score">(\d+)</div>',
        page,
        re.DOTALL,
    )
    if not match:
        raise ValueError(f"Unable to parse the Freedom House 2026 total from {url}")
    return int(match.group(1))


def main():
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("data.json")
    if len(sys.argv) > 2:
        print("Usage: python3 refresh_top20_review.py [data.json]", file=sys.stderr)
        return 2
    payload = json.loads(path.read_text(encoding="utf-8"))
    roster = payload["metadata"]["coverage_roster"]
    top20 = sorted((item for item in roster["countries"] if item["rank"] <= 20), key=lambda item: item["rank"])
    if len(top20) != 20:
        raise ValueError("Coverage metadata does not contain exactly 20 ranked countries")

    # Verify the documented roster against the source, excluding WDI aggregates
    # and non-sovereign economies using its country metadata.
    all_gdp = fetch_json(GDP_URL)[1]
    country_metadata = fetch_json(COUNTRIES_URL)[1]
    sovereign_codes = {
        item["id"] for item in country_metadata
        if item["region"]["id"] != "NA" and item["capitalCity"]
    }
    ranked = sorted(
        (item for item in all_gdp if item["countryiso3code"] in sovereign_codes and item["value"] is not None),
        key=lambda item: item["value"],
        reverse=True,
    )
    expected_iso3 = [item["iso3"] for item in top20]
    actual_iso3 = [item["countryiso3code"] for item in ranked[:20]]
    if actual_iso3 != expected_iso3:
        raise ValueError(f"World Bank top-20 roster changed: {actual_iso3}")

    iso3_codes = ";".join(expected_iso3)
    raw_readings, source_urls = {}, {}
    for pillar, (indicator, year, _, _) in INDICATORS.items():
        url = WDI_URL.format(codes=iso3_codes, indicator=indicator, year=year)
        rows = fetch_json(url)[1]
        readings = {row["countryiso3code"]: row["value"] for row in rows}
        missing = [code for code in expected_iso3 if readings.get(code) is None]
        if missing:
            raise ValueError(f"Missing {indicator} values for {missing}; no data written")
        raw_readings[pillar] = readings
        source_urls[pillar] = url

    countries_by_code = {country["country_code"]: country for country in payload["countries"]}
    changed_scores = []
    for roster_entry in top20:
        country = countries_by_code[roster_entry["country_code"]]
        iso3 = roster_entry["iso3"]
        old_review = country.get("review", {})
        old_fh_url = old_review["observed_readings"]["freedom_house_total"]["url"]
        fh_url = old_fh_url.rsplit("/", 1)[0] + "/2026"
        fh_score = freedom_house_score(fh_url)
        readings = {pillar: raw_readings[pillar][iso3] for pillar in INDICATORS}
        computed = {
            "survival_floor": round(readings["survival_floor"] / 4, 1),
            "sovereign_cannibalization": round(min(readings["sovereign_cannibalization"] / 2000, 25), 1),
            "labor_retention": round(readings["labor_retention"] / 4, 1),
            "state_coercion": round(fh_score / 4, 1),
        }
        review = {
            "reviewed_at": date.today().isoformat(),
            "observed_readings": {
                "life_expectancy_years": {"value": readings["survival_floor"], "observation_year": 2023, "url": source_urls["survival_floor"]},
                "gni_per_capita_usd": {"value": readings["sovereign_cannibalization"], "observation_year": 2024, "url": source_urls["sovereign_cannibalization"]},
                "employment_to_population_percent": {"value": readings["labor_retention"], "observation_year": 2024, "url": source_urls["labor_retention"]},
                "freedom_house_total": {"value": fh_score, "edition": "Freedom in the World 2026", "url": fh_url},
            },
            "rule": "coverage-input v1: round each pillar to one decimal before summing; see COUNTRY_COVERAGE.md",
        }
        if country["country_code"] in LEGACY_CODES:
            review["decision"] = (
                "legacy pilot score retained: current published readings (including Freedom in the World 2026) were reviewed, "
                "but the repository has no source-backed legacy-to-v1 crosswalk that justifies changing a declared pilot score"
            )
        else:
            old_score = country["hvi_score"]
            country["pillars"] = computed
            country["hvi_score"] = round(sum(computed.values()), 1)
            country["grade"] = grade(country["hvi_score"])
            if country["hvi_score"] == old_score:
                review["decision"] = "coverage-input v1 readings reviewed; declared score unchanged because the cited transform reproduces it"
            else:
                review["decision"] = "coverage-input v1 score revised because the latest cited reading changes its published transformed pillar"
                changed_scores.append(f"{country['country_code']} {old_score:.1f}->{country['hvi_score']:.1f}")
        country["review"] = review

    roster["source_url"] = GDP_URL
    roster["retrieved_at"] = date.today().isoformat()
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Top-20 review completed; score changes: " + (", ".join(changed_scores) or "none"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
