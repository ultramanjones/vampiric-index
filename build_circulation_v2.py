"""Fetch authoritative readings and build the transparent household-circulation v2 scorecard.

The pipeline draws on World Bank data, documented same-family WDI fallbacks,
and a supplemental-source registry for countries where a required WDI series is absent.
It preserves source dates and country-level provenance throughout.
"""

import json
import sys
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

API = "https://api.worldbank.org/v2/country/{codes}/indicator/{indicator}?date=2020:2024&format=json&per_page=2000"
USER_AGENT = "VampiricIndexCirculation/1.0 (+https://github.com/ultramanjones/vampiric-index)"
SCORECARD_KEY = "household_circulation_v2"
LEGACY_KEY = "legacy_four_pillar_v1"
MODULE_MAX = 20.0

MODULES = {
    "pay_reaching_households": {
        "label": "Pay reaching households",
        "short_label": "Pay",
        "description": "Broad income-per-person reading for household resource flow.",
        "indicator_id": "NY.GNP.PCAP.CD",
        "source_label": "GNI per capita, Atlas method (current US$)",
        "formula": "clamp(value / 5000, 0, 20)",
    },
    "cost_of_staying_alive": {
        "label": "Cost of staying alive",
        "short_label": "Costs",
        "description": "Annual consumer-price pressure reading for the cost of staying alive.",
        "indicator_id": "FP.CPI.TOTL.ZG",
        "source_label": "Inflation, consumer prices (annual %)",
        "formula": "clamp(20 - 2 * max(value - 2, 0), 0, 20)",
    },
    "breathing_room_debt": {
        "label": "Breathing room / debt pressure",
        "short_label": "Debt",
        "description": "Private-credit pressure reading for household breathing room and debt exposure.",
        "indicator_id": "FS.AST.PRVT.GD.ZS",
        "source_label": "Domestic credit to private sector (% of GDP)",
        "formula": "clamp(20 - value / 10, 0, 20)",
    },
    "labor_leverage": {
        "label": "Labor leverage",
        "short_label": "Labor",
        "description": "Employment attachment reading for labor leverage.",
        "indicator_id": "SL.EMP.TOTL.SP.ZS",
        "source_label": "Employment-to-population ratio, ages 15+, total (%) (modeled ILO estimate)",
        "formula": "clamp(value / 5, 0, 20)",
    },
    "customer_cash": {
        "label": "Customer cash / spending capacity",
        "short_label": "Customer cash",
        "description": "Household and NPISH consumption per-person reading for customer spending capacity.",
        "indicator_id": "NE.CON.PRVT.PC.KD",
        "source_label": "Households and NPISHs final consumption expenditure per capita (constant 2015 US$)",
        "formula": "clamp(value / 2500, 0, 20)",
    },
}
ORDER = list(MODULES)

# Verified external observations used only where the World Bank does not publish
# the required current series.  Each item names the exact series and is preserved
# in data.json alongside its observation year; no value is interpolated.
SUPPLEMENTAL_READINGS = {
    "breathing_room_debt": {
        "CAN": {
            "value": 100.06666,
            "observation_year": 2024,
            "indicator_id": "IMF DataMapper HH_LS",
            "source_label": "IMF household loans (% of GDP)",
            "url": "https://www.imf.org/external/datamapper/api/v1/HH_LS",
            "source_tier": "IMF international fallback",
        },
        "ETH": {
            "value": 26.8257348313042,
            "observation_year": 2022,
            "indicator_id": "IMF FAS FCSODCG_GDP_PT",
            "source_label": "IMF Financial Access Survey: outstanding loans from commercial banks (% of GDP)",
            "url": "https://api.imf.org/external/sdmx/2.1/data/FAS/A.ET.FCSODCG_GDP_PT",
            "source_tier": "IMF international fallback",
        },
        "LKA": {
            "value": 36.3889173136525, "observation_year": 2023,
            "indicator_id": "IMF FAS FCSODCG_GDP_PT",
            "source_label": "IMF Financial Access Survey: outstanding loans from commercial banks (% of GDP)",
            "url": "https://api.imf.org/external/sdmx/2.1/data/FAS/A.LK.FCSODCG_GDP_PT", "source_tier": "IMF international fallback",
        },
        "CMR": {
            "value": 15.6910425449205, "observation_year": 2020,
            "indicator_id": "IMF FAS FCSODCG_GDP_PT",
            "source_label": "IMF Financial Access Survey: outstanding loans from commercial banks (% of GDP)",
            "url": "https://api.imf.org/external/sdmx/2.1/data/FAS/A.CM.FCSODCG_GDP_PT", "source_tier": "IMF international fallback",
        },
        "BHR": {
            "value": 69.8097365331999, "observation_year": 2024,
            "indicator_id": "IMF FAS FCSODCG_GDP_PT",
            "source_label": "IMF Financial Access Survey: outstanding loans from commercial banks (% of GDP)",
            "url": "https://api.imf.org/external/sdmx/2.1/data/FAS/A.BH.FCSODCG_GDP_PT", "source_tier": "IMF international fallback",
        },
        "MRT": {
            "value": 232.805074861383, "observation_year": 2024,
            "indicator_id": "IMF FAS FCSODCG_GDP_PT",
            "source_label": "IMF Financial Access Survey: outstanding loans from commercial banks (% of GDP)",
            "url": "https://api.imf.org/external/sdmx/2.1/data/FAS/A.MR.FCSODCG_GDP_PT", "source_tier": "IMF international fallback",
        },
        "LAO": {
            "value": 59.2653624487854, "observation_year": 2023,
            "indicator_id": "IMF FAS FCSODCG_GDP_PT",
            "source_label": "IMF Financial Access Survey: outstanding loans from commercial banks (% of GDP)",
            "url": "https://api.imf.org/external/sdmx/2.1/data/FAS/A.LA.FCSODCG_GDP_PT", "source_tier": "IMF international fallback",
        },
        "VEN": {
            "value": 23.9318515900636, "observation_year": 2015,
            "indicator_id": "WDI FD.AST.PRVT.GD.ZS",
            "source_label": "World Bank domestic credit provided by banking sector (% of GDP) — latest published Venezuelan observation is 2015",
            "url": "https://api.worldbank.org/v2/country/VEN/indicator/FD.AST.PRVT.GD.ZS?format=json&per_page=100", "source_tier": "WDI historical fallback; stale observation disclosed",
        },
        "GAB": {
            "value": 13.3764779657931, "observation_year": 2019,
            "indicator_id": "WDI FS.AST.PRVT.GD.ZS",
            "source_label": "World Bank domestic credit to private sector (% of GDP) — latest published Gabon observation is 2019",
            "url": "https://api.worldbank.org/v2/country/GAB/indicator/FS.AST.PRVT.GD.ZS?format=json&per_page=100", "source_tier": "WDI historical fallback; stale observation disclosed",
        },
        "IRN": {
            "value": 36.6037094731315,
            "observation_year": 2018,
            "indicator_id": "IMF FAS FCSODCG_GDP_PT",
            "source_label": "IMF Financial Access Survey: outstanding loans from commercial banks (% of GDP) — latest published Iranian observation is 2018",
            "url": "https://api.imf.org/external/sdmx/2.1/data/FAS/A.IR.FCSODCG_GDP_PT",
            "source_tier": "IMF international fallback; stale observation disclosed",
        },
    },
    "cost_of_staying_alive": {
        "SOM": {"value": 5.5, "observation_year": 2024, "indicator_id": "IMF WEO PCPIPCH", "source_label": "IMF World Economic Outlook: inflation, average consumer prices (annual %)", "url": "https://www.imf.org/external/datamapper/api/v1/PCPIPCH", "source_tier": "IMF international fallback"},
        "SWZ": {"value": 4.0, "observation_year": 2024, "indicator_id": "IMF WEO PCPIPCH", "source_label": "IMF World Economic Outlook: inflation, average consumer prices (annual %)", "url": "https://www.imf.org/external/datamapper/api/v1/PCPIPCH", "source_tier": "IMF international fallback"},
        "VEN": {"value": 49.4, "observation_year": 2024, "indicator_id": "IMF WEO PCPIPCH", "source_label": "IMF World Economic Outlook: inflation, average consumer prices (annual %)", "url": "https://www.imf.org/external/datamapper/api/v1/PCPIPCH", "source_tier": "IMF international fallback"},
        "TKM": {"value": 4.6, "observation_year": 2024, "indicator_id": "IMF WEO PCPIPCH", "source_label": "IMF World Economic Outlook: inflation, average consumer prices (annual %)", "url": "https://www.imf.org/external/datamapper/api/v1/PCPIPCH", "source_tier": "IMF international fallback"},
        "MMR": {"value": 29.6, "observation_year": 2024, "indicator_id": "IMF WEO PCPIPCH", "source_label": "IMF World Economic Outlook: inflation, average consumer prices (annual %)", "url": "https://www.imf.org/external/datamapper/api/v1/PCPIPCH", "source_tier": "IMF international fallback"},
        "COD": {
            "value": 17.7,
            "observation_year": 2024,
            "indicator_id": "IMF WEO PCPIPCH",
            "source_label": "IMF World Economic Outlook: inflation, average consumer prices (annual %)",
            "url": "https://www.imf.org/external/datamapper/api/v1/PCPIPCH",
            "source_tier": "IMF international fallback",
        },
    },
}


def clamp(value, low=0.0, high=MODULE_MAX):
    return max(low, min(high, value))


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


def score_module(key, value):
    if key == "pay_reaching_households":
        return round(clamp(value / 5000), 1)
    if key == "cost_of_staying_alive":
        return round(clamp(20 - 2 * max(value - 2, 0)), 1)
    if key == "breathing_room_debt":
        return round(clamp(20 - value / 10), 1)
    if key == "labor_leverage":
        return round(clamp(value / 5), 1)
    if key == "customer_cash":
        return round(clamp(value / 2500), 1)
    raise KeyError(key)


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def latest_indicator(iso3_codes, indicator, source_label, start_year=2020):
    url = API.format(codes=";".join(iso3_codes), indicator=urllib.parse.quote(indicator))
    payload = fetch_json(url)
    rows = payload[1] if isinstance(payload, list) and len(payload) > 1 and payload[1] else []
    readings = {}
    for row in rows:
        code, value = row.get("countryiso3code"), row.get("value")
        if code and value is not None and code not in readings:
            readings[code] = {"value": value, "observation_year": int(row["date"]), "indicator_id": indicator, "source_label": source_label, "url": url}
    return readings


def latest_readings(iso3_codes, module):
    definition = MODULES[module]
    return latest_indicator(iso3_codes, definition["indicator_id"], definition["source_label"])


def apply_world_bank_fallbacks(iso3_codes, readings):
    """Use same-family WDI alternatives before declaring an input unavailable."""
    bank_credit = latest_indicator(iso3_codes, "FD.AST.PRVT.GD.ZS", "Domestic credit provided by banking sector (% of GDP)")
    for code, reading in bank_credit.items():
        readings["breathing_room_debt"].setdefault(code, reading)

    consumption_total = latest_indicator(iso3_codes, "NE.CON.PRVT.KD", "Household/NPISH final consumption expenditure (constant 2015 US$)")
    population = latest_indicator(iso3_codes, "SP.POP.TOTL", "Population, total")
    for code, total in consumption_total.items():
        pop = population.get(code)
        if not pop or not pop["value"]:
            continue
        readings["customer_cash"].setdefault(code, {
            "value": total["value"] / pop["value"],
            "observation_year": min(total["observation_year"], pop["observation_year"]),
            "indicator_id": "NE.CON.PRVT.KD / SP.POP.TOTL",
            "source_label": "Household/NPISH consumption per person, calculated from WDI total consumption and population",
            "url": total["url"],
        })

    # Last-resort, explicitly labeled capacity proxy for countries where WDI does
    # not publish household-consumption series at all. It is not consumption.
    missing_cash_codes = [code for code in iso3_codes if code not in readings["customer_cash"]]
    gdp_per_person = latest_indicator(missing_cash_codes, "NY.GDP.PCAP.KD", "GDP per capita (constant 2015 US$)") if missing_cash_codes else {}
    for code, reading in gdp_per_person.items():
        readings["customer_cash"].setdefault(code, {
            **reading,
            "indicator_id": "NY.GDP.PCAP.KD",
            "source_label": "GDP per capita (constant 2015 US$), used only where household-consumption data is unavailable",
            "source_tier": "WDI last-resort spending-capacity proxy",
        })


def apply_supplemental_readings(readings):
    """Fill WDI holes from explicitly registered, internationally documented sources."""
    for module, by_iso3 in SUPPLEMENTAL_READINGS.items():
        for iso3, reading in by_iso3.items():
            readings[module].setdefault(iso3, dict(reading))


def migrate_country(country, iso3, readings, retrieved_at):
    scorecards = country.setdefault("scorecards", {})
    scorecards.setdefault(LEGACY_KEY, {
        "status": "legacy",
        "modules": dict(country["pillars"]),
        "hvi_score": country["hvi_score"],
        "grade": country["grade"],
    })
    observed = {key: readings[key].get(iso3) for key in ORDER}
    missing = [key for key, value in observed.items() if value is None]
    v2 = {
        "status": "unavailable" if missing else "complete",
        "retrieved_at": retrieved_at,
        "observed_readings": {key: value for key, value in observed.items() if value is not None},
    }
    if missing:
        v2["missing_modules"] = missing
    else:
        modules = {key: score_module(key, observed[key]["value"]) for key in ORDER}
        total = round(sum(modules.values()), 1)
        v2.update({"modules": modules, "hvi_score": total, "grade": grade(total)})
    scorecards[SCORECARD_KEY] = v2


def main():
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("data.json")
    if len(sys.argv) > 2:
        print("Usage: python3 build_circulation_v2.py [data.json]", file=sys.stderr)
        return 2
    payload = json.loads(path.read_text(encoding="utf-8"))
    roster = payload.get("metadata", {}).get("coverage_roster", {}).get("countries", [])
    iso3_by_iso2 = {item["country_code"]: item["iso3"] for item in roster}
    countries = payload.get("countries", [])
    if not countries or any(country["country_code"] not in iso3_by_iso2 for country in countries):
        raise ValueError("Every tracked country must exist in metadata.coverage_roster.countries")
    iso3_codes = [iso3_by_iso2[country["country_code"]] for country in countries]
    readings = {key: latest_readings(iso3_codes, key) for key in ORDER}
    apply_world_bank_fallbacks(iso3_codes, readings)
    apply_supplemental_readings(readings)
    retrieved_at = date.today().isoformat()
    for country in countries:
        migrate_country(country, iso3_by_iso2[country["country_code"]], readings, retrieved_at)
    metadata = payload.setdefault("metadata", {})
    scorecards = metadata.setdefault("scorecards", {})
    scorecards[LEGACY_KEY] = {
        "label": "Legacy four-pillar HVI (v1)", "scale_max": 100, "module_max": 25,
        "module_order": ["survival_floor", "sovereign_cannibalization", "labor_retention", "state_coercion"],
        "modules": {"survival_floor": {"label": "Survival"}, "sovereign_cannibalization": {"label": "Sovereign"}, "labor_retention": {"label": "Labor"}, "state_coercion": {"label": "Coercion"}},
    }
    scorecards[SCORECARD_KEY] = {
        "label": "Household-circulation HVI (v2)", "scale_max": 100, "module_max": MODULE_MAX,
        "module_order": ORDER, "modules": MODULES,
        "rule": "Complete scores combine five dated readings: pay reaching households, cost of staying alive, debt pressure, labor leverage, and customer spending capacity. The pipeline records World Bank primary series, same-family WDI fallbacks, and named IMF international fallbacks with source, series, URL, and observation year.",
        "source_note": "The current global source ledger tracks rent burden, household debt service, disposable income, wages, underemployment, and multiple-jobholding as future additions.",
    }
    metadata["active_scorecard"] = SCORECARD_KEY
    metadata["score_method"] = "Household-circulation v2 is the active scorecard; legacy v1 remains available for comparison."
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    complete = sum(c["scorecards"][SCORECARD_KEY]["status"] == "complete" for c in countries)
    print(f"Wrote v2 scorecards for {len(countries)} countries: {complete} complete, {len(countries) - complete} unavailable due to missing source inputs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
