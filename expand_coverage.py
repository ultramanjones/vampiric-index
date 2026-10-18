"""Add the next verified sovereign economies from the documented WDI GDP roster."""

import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

GDP_URL = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2024&format=json&per_page=400"
WDI_URL = "https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}?date={year}&format=json&per_page=100"
# Strict descending WDI 2024 sovereign GDP order after Albania. Aggregates and
# non-sovereign economies are excluded under COUNTRY_COVERAGE.md.
CANDIDATES = [
    (113, "MLI", "ML", "Mali", "mali", 24),
    (115, "ARM", "AM", "Armenia", "armenia", 54),
    (116, "TTO", "TT", "Trinidad and Tobago", "trinidad-and-tobago", 82),
]
BLOCKED_CANDIDATES = [
    (114, "LBN", "LB", "Lebanon", "labor_retention"),
]
INDICATORS = {
    "survival_floor": ("SP.DYN.LE00.IN", 2023, "life_expectancy_years"),
    "sovereign_cannibalization": ("NY.GNP.PCAP.CD", 2024, "gni_per_capita_usd"),
    "labor_retention": ("SL.EMP.TOTL.SP.ZS", 2024, "employment_to_population_percent"),
}


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "VampiricIndex/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
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


def main():
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("data.json")
    if len(sys.argv) > 2:
        print("Usage: python3 expand_coverage.py [data.json]", file=sys.stderr)
        return 2

    payload = json.loads(path.read_text(encoding="utf-8"))
    existing = {country["country_code"] for country in payload["countries"]}
    wanted_codes = {item[2] for item in CANDIDATES} | {item[2] for item in BLOCKED_CANDIDATES}
    overlap = existing & wanted_codes
    if overlap:
        raise ValueError(f"Candidates already tracked: {sorted(overlap)}")

    gdp_rows = fetch(GDP_URL)[1]
    gdp = {row["countryiso3code"]: row["value"] for row in gdp_rows}
    iso3_codes = [item[1] for item in CANDIDATES] + [item[1] for item in BLOCKED_CANDIDATES]
    readings, reading_urls = {}, {}
    for pillar, (indicator, year, _) in INDICATORS.items():
        url = WDI_URL.format(codes=";".join(iso3_codes), indicator=indicator, year=year)
        rows = fetch(url)[1]
        readings[pillar] = {row["countryiso3code"]: row["value"] for row in rows}
        reading_urls[pillar] = url

    roster = payload["metadata"]["coverage_roster"]["countries"]
    if roster[-1]["country_code"] != "AL" or roster[-1]["rank"] != 112:
        raise ValueError("Expected the existing roster to end with Albania at rank 112")
    previous_gdp = roster[-1]["gdp_current_usd"]
    added = []
    blocked = []
    for rank, iso3, iso2, name, missing_pillar in BLOCKED_CANDIDATES:
        raw = {pillar: readings[pillar][iso3] for pillar in INDICATORS}
        if raw[missing_pillar] is not None:
            raise ValueError(f"Expected required WDI reading to be missing for {iso3}: {raw}")
        if not gdp[iso3] or gdp[iso3] >= previous_gdp:
            raise ValueError(f"GDP ordering failed for blocked candidate {iso3}")
        # Blocked economies are documented without becoming an ordering baseline:
        # a later eligible economy can have higher GDP than this blocked slot.
        payload["metadata"]["coverage_roster"]["blocked_candidates"].append({
            "rank": rank,
            "iso3": iso3,
            "country_code": iso2,
            "name": name,
            "reason": "Required coverage-input v1 indicator has no World Bank observation; no HVI record was fabricated.",
            "missing_indicators": [missing_pillar],
            "source_urls": {missing_pillar: reading_urls[missing_pillar]},
        })
        blocked.append(name)
    for rank, iso3, iso2, name, slug, freedom_score in CANDIDATES:
        raw = {pillar: readings[pillar][iso3] for pillar in INDICATORS}
        if any(value is None for value in raw.values()):
            raise ValueError(f"Required WDI reading missing for {iso3}: {raw}")
        if not gdp[iso3] or gdp[iso3] >= previous_gdp:
            raise ValueError(f"GDP ordering failed for {iso3}")
        previous_gdp = gdp[iso3]
        pillars = {
            "survival_floor": round(raw["survival_floor"] / 4, 1),
            "sovereign_cannibalization": round(min(raw["sovereign_cannibalization"] / 2000, 25), 1),
            "labor_retention": round(raw["labor_retention"] / 4, 1),
            "state_coercion": round(freedom_score / 4, 1),
        }
        score = round(sum(pillars.values()), 1)
        country = {
            "country_code": iso2,
            "name": name,
            "pillars": pillars,
            "hvi_score": score,
            "grade": grade(score),
            "chronic_pathologies": [
                f"Life expectancy at birth: {raw['survival_floor']:.3f} years (World Bank WDI, 2023)",
                f"GNI per capita: US${raw['sovereign_cannibalization']:,.0f} (World Bank WDI, 2024)",
                f"Employment-to-population ratio: {raw['labor_retention']:.3f}% (World Bank WDI/ILO, 2024)",
                f"Freedom in the World 2025 total score: {freedom_score}/100 (Freedom House)",
            ],
            "acute_dispatch": [],
            "review": {
                "reviewed_at": date.today().isoformat(),
                "observed_readings": {
                    "life_expectancy_years": {"value": raw["survival_floor"], "observation_year": 2023, "url": reading_urls["survival_floor"]},
                    "gni_per_capita_usd": {"value": raw["sovereign_cannibalization"], "observation_year": 2024, "url": reading_urls["sovereign_cannibalization"]},
                    "employment_to_population_percent": {"value": raw["labor_retention"], "observation_year": 2024, "url": reading_urls["labor_retention"]},
                    "freedom_house_total": {"value": freedom_score, "edition": "Freedom in the World 2025", "url": f"https://freedomhouse.org/country/{slug}/freedom-world/2025"},
                },
                "rule": "coverage-input v1: round each pillar to one decimal before summing; see COUNTRY_COVERAGE.md",
                "decision": "new coverage-input v1 record; declared score is the published transform of the cited readings",
            },
        }
        payload["countries"].append(country)
        roster.append({"rank": rank, "iso3": iso3, "country_code": iso2, "name": name, "gdp_current_usd": gdp[iso3], "observation_year": 2024})
        added.append(name)

    payload["metadata"]["coverage_roster"]["source_url"] = GDP_URL
    payload["metadata"]["coverage_roster"]["retrieved_at"] = date.today().isoformat()
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("Added: " + ", ".join(added))
    print("Blocked: " + ", ".join(blocked))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
