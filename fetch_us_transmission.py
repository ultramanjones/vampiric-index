"""Build a source-linked US liquidity transmission and asset-contagion snapshot."""

import csv
import io
import json
import sys
import tempfile
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

FRED_BASE_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
USER_AGENT = "VampiricIndexTransmission/1.0 (+https://github.com/ultramanjones/vampiric-index)"
MAX_HISTORY = 180

SERIES = {
    "credit_card_delinquency": {
        "id": "DRCCLACBS",
        "label": "Credit-card delinquency rate",
        "unit": "Percent of loans",
        "description": "Delinquency rate on credit cards at all commercial banks.",
    },
    "revolving_credit": {
        "id": "REVOLSL",
        "label": "Revolving consumer credit",
        "unit": "Millions of dollars",
        "description": "Revolving consumer credit owned and securitized, seasonally adjusted; primarily credit-card balances.",
    },
    "credit_card_apr": {
        "id": "TERMCBCCALLNS",
        "label": "Commercial-bank credit-card APR",
        "unit": "Percent",
        "description": "Interest rate on credit-card plans, all accounts, at commercial banks.",
    },
    "personal_saving_rate": {
        "id": "PSAVERT",
        "label": "Personal saving rate",
        "unit": "Percent of disposable income",
        "description": "Personal saving as a percentage of disposable personal income.",
    },
    "food_away_from_home_cpi": {
        "id": "CUUR0000SEFV",
        "label": "Food away from home CPI",
        "unit": "Index (1982-84=100)",
        "description": "Consumer Price Index for food purchased away from home; used only to deflate a documented restaurant same-store sales series, never as traffic itself.",
    },
    "high_yield_oas": {
        "id": "BAMLH0A0HYM2",
        "label": "US broad high-yield option-adjusted spread",
        "unit": "Percentage points",
        "description": "ICE BofA US High Yield Index option-adjusted spread.",
    },
    "ccc_oas": {
        "id": "BAMLH0A3HYC",
        "label": "CCC-and-lower high-yield spread",
        "unit": "Percentage points",
        "description": "ICE BofA US High Yield CCC or Below Index option-adjusted spread.",
    },
    "fed_assets": {
        "id": "WALCL",
        "label": "Federal Reserve total assets",
        "unit": "Millions of dollars",
        "description": "Total assets held by the Federal Reserve.",
    },
    "reverse_repo": {
        "id": "RRPONTSYD",
        "label": "Overnight reverse-repo facility balance",
        "unit": "Billions of dollars",
        "description": "Fed overnight reverse-repurchase agreements, a liquidity-buffer proxy.",
    },
}

NEWS_QUERY = (
    "(McDonald's OR Wendy's OR Domino's OR Dollar General OR Dollar Tree) "
    "(traffic OR transactions OR value menu OR discount OR low-income OR consumer pullback OR weak demand)"
)
NEWS_SIGNALS = (
    "traffic",
    "transaction",
    "value menu",
    "value meal",
    "discount",
    "dollar store",
    "low-income",
    "consumer pullback",
    "weak demand",
    "downtrading",
    "down-trading",
    "price-sensitive",
)


def fred_url(series_id):
    """Return the documented no-key FRED graph CSV endpoint for one series."""
    return f"{FRED_BASE_URL}{urllib.parse.quote(series_id)}"


def fred_series_page_url(series_id):
    """Return the human-facing FRED series page, rather than a downloaded CSV."""
    return f"https://fred.stlouisfed.org/series/{urllib.parse.quote(series_id)}"


def fetch_url(url):
    """Fetch bytes with a stable project user agent."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def parse_fred_csv(raw_csv, series_id):
    """Parse usable FRED observations into ascending date/value dictionaries."""
    rows = csv.DictReader(io.StringIO(raw_csv.decode("utf-8")))
    points = []
    for row in rows:
        raw_value = row.get(series_id, "")
        if raw_value in ("", ".", None):
            continue
        try:
            observation_date = date.fromisoformat(row["observation_date"])
            value = float(raw_value)
        except (KeyError, TypeError, ValueError):
            continue
        points.append({"date": observation_date, "value": value})
    if not points:
        raise ValueError(f"FRED series {series_id} contained no usable observations")
    return points


def fetch_series(spec):
    """Fetch one FRED series and retain enough history for change calculations."""
    series_id = spec["id"]
    points = parse_fred_csv(fetch_url(fred_url(series_id)), series_id)
    return {
        "series_id": series_id,
        "label": spec["label"],
        "unit": spec["unit"],
        "description": spec["description"],
        "source_url": fred_series_page_url(series_id),
        "points": points,
    }


def point_on_or_before(points, target_date):
    """Return the latest observation no later than target_date, if available."""
    eligible = [point for point in points if point["date"] <= target_date]
    return eligible[-1] if eligible else None


def indicator_snapshot(series, lookback_days=None):
    """Make a JSON-safe indicator record with an optional prior observation."""
    latest = series["points"][-1]
    snapshot = {
        key: series[key]
        for key in ("series_id", "label", "unit", "description", "source_url")
    }
    snapshot.update({
        "value": round(latest["value"], 4),
        "observation_date": latest["date"].isoformat(),
    })
    if lookback_days is not None:
        prior = point_on_or_before(series["points"], latest["date"] - timedelta(days=lookback_days))
        if prior is not None and prior["value"] != 0:
            snapshot["prior_value"] = round(prior["value"], 4)
            snapshot["prior_observation_date"] = prior["date"].isoformat()
            snapshot["change"] = round(latest["value"] - prior["value"], 4)
            snapshot["percent_change"] = round((latest["value"] / prior["value"] - 1) * 100, 2)
    return snapshot


def google_news_url():
    """Return a Google News RSS endpoint for qualitative consumer-distress canaries."""
    parameters = urllib.parse.urlencode({"q": NEWS_QUERY, "hl": "en-US", "gl": "US", "ceid": "US:en"})
    return f"https://news.google.com/rss/search?{parameters}"


def text_of(item, tag):
    element = item.find(tag)
    return element.text.strip() if element is not None and element.text else ""


def fetch_consumer_canaries():
    """Fetch title-level canaries; these are qualitative proxies, not sales data."""
    root = ET.fromstring(fetch_url(google_news_url()))
    canaries = []
    for item in root.findall("./channel/item"):
        title = text_of(item, "title")
        source = text_of(item, "source")
        publication_date = text_of(item, "pubDate")
        url = text_of(item, "link")
        if not all((title, source, publication_date, url)):
            continue
        matched_signals = [signal for signal in NEWS_SIGNALS if signal in title.lower()]
        canaries.append({
            "title": title,
            "source": source,
            "publication_date": publication_date,
            "url": url,
            "matched_signals": matched_signals,
        })
        if len(canaries) == 8:
            break
    if not canaries:
        raise ValueError("Google News RSS contained no usable consumer-canary headlines")
    return canaries


def clamp_score(value):
    return round(max(0.0, min(25.0, value)), 1)


def clamp_unit(value):
    return max(0.0, min(1.0, value))


def score_predatory_extraction(card_apr, revolving_credit):
    """Return a 0-20 predatory-extraction stress score with a nonlinear APR redline."""
    apr = card_apr["value"]
    debt_billions = revolving_credit["value"] / 1000
    apr_redline = clamp_unit(((apr - 18.0) / 3.0) ** 2) if apr > 18 else 0.0
    volume_redline = clamp_unit((debt_billions - 750.0) / 350.0)
    stress = 0.60 * apr_redline + 0.40 * volume_redline
    stress_score = round(20 * (0.10 + 0.90 * stress), 1)
    annualized_interest_billions = round(apr / 100 * debt_billions, 1)
    diagnosis = (
        f"Card APR is {apr:.2f}% against ${debt_billions:,.0f}B in revolving credit. "
        f"At that posted APR, annualized interest extraction reaches about ${annualized_interest_billions:,.0f}B. "
        "Above 18%, APR pressure rises nonlinearly."
    )
    return stress_score, diagnosis, annualized_interest_billions


def score_breathing_room(saving_rate, delinquency, card_apr, revolving_credit, food_away_cpi):
    """Return a 0-20 household-buffer stress score; higher means more strain."""
    savings = saving_rate["value"]
    delinquency_rate = delinquency["value"]
    apr = card_apr["value"]
    revolving_billions = revolving_credit["value"] / 1000
    food_away_inflation = food_away_cpi.get("percent_change", 0.0)
    savings_stress = clamp_unit((7.0 - savings) / 4.0)
    inflation_squeeze = clamp_unit((4.0 - (savings - food_away_inflation)) / 4.0)
    apr_stress = clamp_unit((apr - 15.0) / 7.0)
    revolving_stress = clamp_unit((revolving_billions - 750.0) / 350.0)
    delinquency_stress = clamp_unit((delinquency_rate - 2.0) / 4.0)
    stress = 0.30 * savings_stress + 0.25 * inflation_squeeze + 0.20 * apr_stress + 0.15 * revolving_stress + 0.10 * delinquency_stress
    stress_score = round(20 * stress, 1)
    diagnosis = (
        f"Personal saving is {savings:.2f}% of disposable income while food-away-from-home prices rose {food_away_inflation:.2f}% over a year, "
        f"leaving a {savings - food_away_inflation:.2f}-point nominal gap. Card APR is {apr:.2f}% and revolving credit is ${revolving_billions:,.0f}B; "
        f"card delinquency is {delinquency_rate:.2f}%. Household-buffer stress weights savings (30%), price squeeze (25%), APR (20%), revolving-credit load (15%), and missed payments (10%)."
    )
    return stress_score, diagnosis


def score_debt_saturation(delinquency, consumer_credit):
    """Legacy stress helper retained for deterministic compatibility tests."""
    level = delinquency["value"]
    if level < 2.0:
        score = 3.0
    elif level < 3.5:
        score = 6.0
    elif level < 5.0:
        score = 11.0
    elif level < 7.5:
        score = 16.0
    else:
        score = 21.0
    if delinquency.get("change", 0) >= 0.25:
        score += 3.0
    elif delinquency.get("change", 0) >= 0.10:
        score += 1.5
    credit_growth = consumer_credit.get("percent_change", 0)
    if credit_growth >= 6:
        score += 3.0
    elif credit_growth >= 3:
        score += 1.5
    return clamp_score(score), "Legacy compatibility helper."


def score_corporate_stress(high_yield):
    """Score high-yield spread level and recent widening as a credit-stress proxy."""
    spread = high_yield["value"]
    if spread < 3.5:
        score = 2.0
    elif spread < 5.0:
        score = 6.0
    elif spread < 7.0:
        score = 12.0
    elif spread < 10.0:
        score = 19.0
    else:
        score = 24.0
    recent_widening = high_yield.get("change", 0)
    if recent_widening >= 1.0:
        score += 4.0
    elif recent_widening >= 0.5:
        score += 2.0
    diagnosis = (
        f"US high-yield OAS is {spread:.2f} percentage points; the 30-day change is "
        f"{recent_widening:+.2f} points when available."
    )
    return clamp_score(score), diagnosis


def score_asset_repricing(fed_assets, reverse_repo):
    """Score liquidity-buffer depletion and a 90-day Fed balance-sheet contraction proxy."""
    rrp_lookback = point_on_or_before(
        reverse_repo["points"], reverse_repo["points"][-1]["date"] - timedelta(days=365)
    )
    latest_rrp = reverse_repo["points"][-1]["value"]
    rrp_ratio = latest_rrp / rrp_lookback["value"] if rrp_lookback and rrp_lookback["value"] else None
    if rrp_ratio is None or rrp_ratio > 0.75:
        score = 1.0
    elif rrp_ratio > 0.5:
        score = 3.0
    elif rrp_ratio > 0.25:
        score = 5.0
    elif rrp_ratio > 0.05:
        score = 7.0
    else:
        score = 9.0
    fed_change = fed_assets.get("percent_change", 0)
    if fed_change <= -5:
        score += 8.0
    elif fed_change <= -2:
        score += 5.0
    elif fed_change <= -0.5:
        score += 2.0
    ratio_text = "unavailable" if rrp_ratio is None else f"{rrp_ratio:.1%} of its year-earlier level"
    diagnosis = (
        f"The overnight reverse-repo balance is {ratio_text}; Federal Reserve total assets changed "
        f"{fed_change:+.2f}% over the prior 90 days when comparable observations are available."
    )
    return clamp_score(score), diagnosis


def active_phase(phases):
    """Report the furthest phase with material signal; otherwise report the strongest monitored phase."""
    material = [phase for phase in phases if phase["score"] >= 12.0]
    selected = material[-1] if material else max(phases, key=lambda phase: phase["score"])
    status = "material signal" if material else "monitoring signal"
    return {
        "number": selected["number"],
        "name": selected["name"],
        "score": selected["score"],
        "status": status,
    }


def load_history(path):
    """Read prior snapshot history if the existing JSON file is valid."""
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    history = payload.get("historical_snapshots", []) if isinstance(payload, dict) else []
    return history if isinstance(history, list) else []


def build_payload(history, fetched_at, series, canaries):
    """Build the complete JSON payload from live source data and prior snapshots."""
    indicators = {
        "credit_card_delinquency": indicator_snapshot(series["credit_card_delinquency"], 365),
        "revolving_credit": indicator_snapshot(series["revolving_credit"], 365),
        "credit_card_apr": indicator_snapshot(series["credit_card_apr"], 365),
        "personal_saving_rate": indicator_snapshot(series["personal_saving_rate"], 365),
        "food_away_from_home_cpi": indicator_snapshot(series["food_away_from_home_cpi"], 365),
        "high_yield_oas": indicator_snapshot(series["high_yield_oas"], 30),
        "ccc_oas": indicator_snapshot(series["ccc_oas"], 30),
        "fed_assets": indicator_snapshot(series["fed_assets"], 90),
        "reverse_repo": indicator_snapshot(series["reverse_repo"], 365),
    }
    extraction_stress, extraction_diagnosis, annualized_interest = score_predatory_extraction(
        indicators["credit_card_apr"], indicators["revolving_credit"]
    )
    breathing_stress, breathing_diagnosis = score_breathing_room(
        indicators["personal_saving_rate"], indicators["credit_card_delinquency"], indicators["credit_card_apr"], indicators["revolving_credit"], indicators["food_away_from_home_cpi"]
    )
    phase_1_score = clamp_score(extraction_stress / 20 * 25)
    phase_1_diagnosis = extraction_diagnosis
    phase_2_score = clamp_score(breathing_stress / 20 * 25)
    phase_2_diagnosis = breathing_diagnosis
    phase_3_score, phase_3_diagnosis = score_corporate_stress(indicators["ccc_oas"])
    phase_4_score, phase_4_diagnosis = score_asset_repricing(
        series["fed_assets"], series["reverse_repo"]
    )
    phases = [
        {
            "number": 1,
            "name": "Predatory extraction redline",
            "score": phase_1_score,
            "diagnosis": phase_1_diagnosis,
            "indicator_keys": ["credit_card_apr", "revolving_credit"],
        },
        {
            "number": 2,
            "name": "Household buffer & payment failure",
            "score": phase_2_score,
            "diagnosis": phase_2_diagnosis,
            "indicator_keys": ["personal_saving_rate", "food_away_from_home_cpi", "credit_card_apr", "revolving_credit", "credit_card_delinquency"],
        },
        {
            "number": 3,
            "name": "Corporate & regional credit stress",
            "score": phase_3_score,
            "diagnosis": phase_3_diagnosis,
            "indicator_keys": ["high_yield_oas"],
        },
        {
            "number": 4,
            "name": "Institutional asset repricing",
            "score": phase_4_score,
            "diagnosis": phase_4_diagnosis,
            "indicator_keys": ["fed_assets", "reverse_repo"],
        },
    ]
    total = round(sum(phase["score"] for phase in phases), 1)
    snapshot = {
        "generated_at": fetched_at,
        "total_transmission_index": total,
        "phase_scores": {str(phase["number"]): phase["score"] for phase in phases},
    }
    history = (history + [snapshot])[-MAX_HISTORY:]
    return {
        "schema_version": 1,
        "generated_at": fetched_at,
        "qsr_evidence_watch": {
            "label": "QSR physical-demand evidence watch",
            "status": "partial_public_coverage",
            "rule": "Use dated company comparable-sales releases alongside the matching food-away-from-home CPI change. The combined reading tracks price pressure against restaurant demand.",
            "formula": "price-deflated comparable-sales proxy = disclosed comparable-sales growth − food-away-from-home CPI change",
            "sources": [
                {
                    "name": "BLS Food Away From Home CPI via FRED",
                    "type": "official price index",
                    "url": fred_series_page_url(SERIES["food_away_from_home_cpi"]["id"]),
                    "use": "Official food-away-from-home price series.",
                },
                {
                    "name": "OpenTable State of the Industry",
                    "type": "seated-diner / reservation-activity benchmark",
                    "url": "https://www.opentable.com/restaurant-solutions/resources/state-of-the-industry/",
                    "use": "Tracks seated-diner and reservation activity across the provider's published coverage.",
                },
                {
                    "name": "Fiserv Small Business Index",
                    "type": "merchant-payment sales, transaction, and ticket benchmark",
                    "url": "https://www.fiserv.com/en-us/insights/small-business-index.html",
                    "use": "Tracks merchant payment sales, transaction counts, and ticket size by the provider's published industry and geography.",
                },
                {
                    "name": "Placer.ai data methodology",
                    "type": "modeled mobile-device visits",
                    "url": "https://www.placer.ai/data/",
                    "use": "Tracks modeled mobile-device visits across each report's defined restaurant set and time window.",
                },
            ],
            "survey_sources": [
                {
                    "name": "Census Household Pulse Survey",
                    "url": "https://www.census.gov/programs-surveys/household-pulse-survey/data.html",
                    "use": "Probability-based survey; selected waves include food-away-from-home spending and all waves provide food-sufficiency measures.",
                },
                {
                    "name": "USDA CPS Food Security Supplement",
                    "url": "https://www.ers.usda.gov/topics/food-nutrition-assistance/food-security-in-the-u-s/key-statistics-graphics/",
                    "use": "Annual nationally representative food insecurity and meal-cutting/skipping measures.",
                },
                {
                    "name": "Federal Reserve SHED",
                    "url": "https://www.federalreserve.gov/consumerscommunities/shed_data.htm",
                    "use": "Annual emergency-buffer and debt-dependence survey.",
                },
            ],
        },
        "methodology": {
            "score_range": "Every Transmission Engine score rises with stress: 0 is contained, the maximum is critical.",
            "source_notes": [
                "Phase scores combine dated Federal Reserve/FRED observations into a common stress scale.",
                "Consumer-canary headlines record current economic strain alongside the measured series.",
            ],
        },
        "household_stress": {
            "predatory_extraction": {
                "label": "Predatory extraction stress",
                "score": extraction_stress,
                "max_score": 20,
                "direction": "Higher is worse. Stress rises nonlinearly once card APR exceeds 18% and revolving credit exceeds $750B.",
                "annualized_interest_equivalent_billions": annualized_interest,
                "diagnosis": extraction_diagnosis,
            },
            "breathing_room": {
                "label": "Household buffer stress",
                "score": breathing_stress,
                "max_score": 20,
                "direction": "Higher is worse. Stress rises as savings thin against food-away price pressure and households lean on expensive revolving credit.",
                "diagnosis": breathing_diagnosis,
            },
        },
        "total_transmission_index": total,
        "active_contagion_phase": active_phase(phases),
        "phases": phases,
        "indicators": indicators,
        "consumer_canaries": {
            "source_url": google_news_url(),
            "method": "Google News RSS title matching against published distress-language terms.",
            "items": canaries,
        },
        "historical_snapshots": history,
    }


def write_json_atomic(path, payload):
    """Replace output only after all network work and calculations have succeeded."""
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as temp_file:
        json.dump(payload, temp_file, indent=2, ensure_ascii=False)
        temp_file.write("\n")
        temp_path = Path(temp_file.name)
    temp_path.replace(path)


def main():
    output_path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("us_transmission.json")
    if len(sys.argv) > 2:
        print("Usage: python3 fetch_us_transmission.py [us_transmission.json]", file=sys.stderr)
        return 2
    try:
        series = {name: fetch_series(spec) for name, spec in SERIES.items()}
        canaries = fetch_consumer_canaries()
        fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        payload = build_payload(load_history(output_path), fetched_at, series, canaries)
        write_json_atomic(output_path, payload)
    except (OSError, ET.ParseError, ValueError, UnicodeDecodeError) as error:
        print(f"US transmission update failed; {output_path} was not changed: {error}", file=sys.stderr)
        return 1
    print(f"US Liquidity Transmission Index: {payload['total_transmission_index']:.1f}/100")
    active = payload["active_contagion_phase"]
    print(f"Active contagion phase: {active['number']} — {active['name']} ({active['status']})")
    for phase in payload["phases"]:
        print(f"Phase {phase['number']}: {phase['score']:.1f}/25 — {phase['name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
