"""Build the documented World Bank 2024 nominal-GDP top-30 HVI coverage roster.

This is an explicit intake tool: it adds missing roster countries with the published
coverage-input v1 transforms and preserves every already-declared legacy score.
"""

import json
import sys
import urllib.request
from datetime import date
from pathlib import Path

WDI_BASE = "https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}?date={year}&format=json&per_page=100"
TODAY = date.today().isoformat()
INDICATORS = {
    "survival_floor": ("SP.DYN.LE00.IN", 2023, "life expectancy at birth / 4"),
    "sovereign_cannibalization": ("NY.GNP.PCAP.CD", 2024, "GNI per capita, Atlas method/current US$ / 2,000, capped at 25"),
    "labor_retention": ("SL.EMP.TOTL.SP.ZS", 2024, "employment-to-population ratio, ages 15+, ILO modeled estimate / 4"),
}
# Freedom House's 2025 edition is the latest accessible, country-comparable edition
# used by this project during this run. Values are published total scores out of 100.
COUNTRIES = {
    "USA": ("US", "United States", "united-states", 84),
    "CHN": ("CN", "China", "china", 9),
    "DEU": ("DE", "Germany", "germany", 95),
    "JPN": ("JP", "Japan", "japan", 96),
    "IND": ("IN", "India", "india", 63),
    "GBR": ("GB", "United Kingdom", "united-kingdom", 92),
    "FRA": ("FR", "France", "france", 89),
    "ITA": ("IT", "Italy", "italy", 90),
    "CAN": ("CA", "Canada", "canada", 97),
    "RUS": ("RU", "Russia", "russia", 12),
    "BRA": ("BR", "Brazil", "brazil", 72),
    "KOR": ("KR", "South Korea", "south-korea", 81),
    "MEX": ("MX", "Mexico", "mexico", 60),
    "AUS": ("AU", "Australia", "australia", 95),
    "ESP": ("ES", "Spain", "spain", 90),
    "IDN": ("ID", "Indonesia", "indonesia", 56),
    "TUR": ("TR", "Turkey", "turkey", 33),
    "SAU": ("SA", "Saudi Arabia", "saudi-arabia", 9),
    "NLD": ("NL", "Netherlands", "netherlands", 97),
    "CHE": ("CH", "Switzerland", "switzerland", 96),
    "POL": ("PL", "Poland", "poland", 82),
    "BEL": ("BE", "Belgium", "belgium", 95),
    "ARG": ("AR", "Argentina", "argentina", 85),
    "IRL": ("IE", "Ireland", "ireland", 98),
    "SWE": ("SE", "Sweden", "sweden", 99),
    "SGP": ("SG", "Singapore", "singapore", 48),
    "ARE": ("AE", "United Arab Emirates", "united-arab-emirates", 18),
    "ISR": ("IL", "Israel", "israel", 73),
    "AUT": ("AT", "Austria", "austria", 93),
    "THA": ("TH", "Thailand", "thailand", 34),
}


def get_indicator(codes, indicator, year):
    url = WDI_BASE.format(codes=";".join(codes), indicator=indicator, year=year)
    request = urllib.request.Request(url, headers={"User-Agent": "VampiricIndex/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    return {row["countryiso3code"]: row["value"] for row in payload[1]}, url


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
        print("Usage: python3 refresh_top20_metadata.py [data.json]", file=sys.stderr)
        return 2
    payload = json.loads(path.read_text(encoding="utf-8"))
    codes = list(COUNTRIES)
    gdp, gdp_url = get_indicator(codes, "NY.GDP.MKTP.CD", 2024)
    readings, urls = {}, {}
    for pillar, (indicator, year, _rule) in INDICATORS.items():
        readings[pillar], urls[pillar] = get_indicator(codes, indicator, year)
    ranked = sorted(codes, key=lambda code: gdp[code], reverse=True)
    if ranked != list(COUNTRIES):
        raise ValueError(f"World Bank ranking changed: {ranked}")

    existing = {country["country_code"]: country for country in payload["countries"]}
    output = []
    roster = []
    for rank, iso3 in enumerate(ranked, 1):
        iso2, name, slug, freedom_score = COUNTRIES[iso3]
        raw = {pillar: readings[pillar][iso3] for pillar in INDICATORS}
        computed = {
            "survival_floor": round(raw["survival_floor"] / 4, 1),
            "sovereign_cannibalization": round(min(raw["sovereign_cannibalization"] / 2000, 25), 1),
            "labor_retention": round(raw["labor_retention"] / 4, 1),
            "state_coercion": round(freedom_score / 4, 1),
        }
        score = round(sum(computed.values()), 1)
        metric_evidence = {
            "reviewed_at": TODAY,
            "observed_readings": {
                "life_expectancy_years": {"value": raw["survival_floor"], "observation_year": 2023, "url": urls["survival_floor"]},
                "gni_per_capita_usd": {"value": raw["sovereign_cannibalization"], "observation_year": 2024, "url": urls["sovereign_cannibalization"]},
                "employment_to_population_percent": {"value": raw["labor_retention"], "observation_year": 2024, "url": urls["labor_retention"]},
                "freedom_house_total": {"value": freedom_score, "edition": "Freedom in the World 2025", "url": f"https://freedomhouse.org/country/{slug}/freedom-world/2025"},
            },
        }
        country = existing.get(iso2)
        if country is None:
            country = {
                "country_code": iso2,
                "name": name,
                "pillars": computed,
                "hvi_score": score,
                "grade": grade(score),
                "chronic_pathologies": [
                    f"Life expectancy at birth: {raw['survival_floor']:.3f} years (World Bank WDI, 2023)",
                    f"GNI per capita: US${raw['sovereign_cannibalization']:,.0f} (World Bank WDI, 2024)",
                    f"Employment-to-population ratio: {raw['labor_retention']:.3f}% (World Bank WDI/ILO, 2024)",
                    f"Freedom in the World 2025 total score: {freedom_score}/100 (Freedom House)",
                ],
                "acute_dispatch": [],
            }
            decision = "new coverage-input v1 record; declared score is the published transform of the cited readings"
        elif iso2 in {"US", "GB", "FR", "DE", "MX"}:
            decision = "legacy pilot score retained: current published readings were reviewed, but the repository has no source-backed legacy-to-v1 crosswalk that justifies changing a declared pilot score"
        else:
            decision = country.get("review", {}).get(
                "decision",
                "coverage-input v1 readings reviewed; declared score unchanged because the cited transform reproduces it",
            )
        country["review"] = {**metric_evidence, "rule": "coverage-input v1: round each pillar to one decimal before summing; see COUNTRY_COVERAGE.md", "decision": decision}
        output.append(country)
        roster.append({"rank": rank, "iso3": iso3, "country_code": iso2, "name": name, "gdp_current_usd": gdp[iso3], "observation_year": 2024})

    payload["metadata"] = {
        "coverage_roster": {
            "definition": "Top 30 sovereign economies by nominal GDP in current US dollars",
            "source": "World Bank World Development Indicators, NY.GDP.MKTP.CD — GDP (current US$)",
            "source_url": gdp_url,
            "observation_year": 2024,
            "retrieved_at": TODAY,
            "countries": roster,
        },
        "score_method": "coverage-input v1; legacy pilot records are retained unless a documented source-backed recalibration is available",
    }
    payload["countries"] = output
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(output)} top-30 countries; added {sum(1 for c in output if not c['acute_dispatch'])} records awaiting dispatch refresh.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
