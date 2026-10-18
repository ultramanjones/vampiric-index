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
    "consumer_credit": {
        "id": "TOTALSL",
        "label": "Total consumer credit",
        "unit": "Millions of dollars",
        "description": "Consumer credit owned and securitized, seasonally adjusted.",
    },
    "high_yield_oas": {
        "id": "BAMLH0A0HYM2",
        "label": "US high-yield option-adjusted spread",
        "unit": "Percentage points",
        "description": "ICE BofA US High Yield Index option-adjusted spread.",
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
        "source_url": fred_url(series_id),
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


def score_consumer_exhaustion(canaries):
    """Score title-level distress signals without pretending they are audited sales figures."""
    signal_hits = sum(len(item["matched_signals"]) for item in canaries)
    score = clamp_score(signal_hits * 2.5)
    diagnosis = (
        f"{signal_hits} qualifying distress-language matches appeared across {len(canaries)} "
        "consumer-canary headlines. This is a qualitative early-warning proxy, not company-reported traffic or unit-sales data."
    )
    return score, diagnosis


def score_debt_saturation(delinquency, consumer_credit):
    """Score card delinquency level, trend, and annual consumer-credit growth."""
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
    diagnosis = (
        f"Credit-card delinquency is {level:.2f}%; annual consumer-credit change is "
        f"{credit_growth:+.2f}% when a comparable prior observation is available."
    )
    return clamp_score(score), diagnosis


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
        "consumer_credit": indicator_snapshot(series["consumer_credit"], 365),
        "high_yield_oas": indicator_snapshot(series["high_yield_oas"], 30),
        "fed_assets": indicator_snapshot(series["fed_assets"], 90),
        "reverse_repo": indicator_snapshot(series["reverse_repo"], 365),
    }
    phase_1_score, phase_1_diagnosis = score_consumer_exhaustion(canaries)
    phase_2_score, phase_2_diagnosis = score_debt_saturation(
        indicators["credit_card_delinquency"], indicators["consumer_credit"]
    )
    phase_3_score, phase_3_diagnosis = score_corporate_stress(indicators["high_yield_oas"])
    phase_4_score, phase_4_diagnosis = score_asset_repricing(
        series["fed_assets"], series["reverse_repo"]
    )
    phases = [
        {
            "number": 1,
            "name": "Base-layer consumer exhaustion",
            "score": phase_1_score,
            "diagnosis": phase_1_diagnosis,
            "indicator_keys": ["consumer_canaries"],
        },
        {
            "number": 2,
            "name": "Debt saturation and shadow-credit exhaustion",
            "score": phase_2_score,
            "diagnosis": phase_2_diagnosis,
            "indicator_keys": ["credit_card_delinquency", "consumer_credit"],
        },
        {
            "number": 3,
            "name": "Corporate cash-flow pinch and regional credit stress",
            "score": phase_3_score,
            "diagnosis": phase_3_diagnosis,
            "indicator_keys": ["high_yield_oas"],
        },
        {
            "number": 4,
            "name": "Institutional asset repricing and liquidity drain",
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
        "methodology": {
            "score_range": "Each phase is 0.0-25.0; total is 0.0-100.0. Higher values indicate deeper measured transmission risk.",
            "limitations": [
                "Phase 1 uses title-level news canaries because free, comparable QSR transaction data is not consistently available.",
                "The index is a monitoring instrument, not a recession forecast or investment recommendation.",
                "A phase score does not establish causation between consumer stress and asset prices.",
            ],
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
