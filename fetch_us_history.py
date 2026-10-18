"""Fetch cited, unaltered U.S. historical series for the household-circulation chart.

Values are stored at their source cadence.  The dashboard may select observations or
aggregate them to a coarser display cadence; it never fabricates between observations.
"""
import csv
import io
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

BASE = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
SERIES = [
    {
        "key": "pay_reaching_households", "label": "Pay reaching households",
        "color": "#67d2ff", "series_id": "A229RX0", "frequency": "monthly",
        "unit": "real disposable personal income per capita (chained dollars)",
        "source": "BEA via FRED", "starts": "1959-01-01",
    },
    {
        "key": "cost_of_staying_alive", "label": "Cost of staying alive",
        "color": "#ff927d", "series_id": "CPIAUCSL", "frequency": "monthly",
        "unit": "Consumer Price Index for All Urban Consumers (index)",
        "source": "BLS via FRED", "starts": "1947-01-01",
    },
    {
        "key": "breathing_room_debt", "label": "Breathing room / debt pressure",
        "color": "#cfa7ff", "series_id": "TDSP", "frequency": "quarterly",
        "unit": "household debt service payments as a percent of disposable personal income",
        "source": "Board of Governors of the Federal Reserve System via FRED", "starts": "2005-01-01",
    },
    {
        "key": "labor_leverage", "label": "Labor leverage",
        "color": "#7ee1ad", "series_id": "EMRATIO", "frequency": "monthly",
        "unit": "employment-population ratio, age 16+ (percent)",
        "source": "BLS via FRED", "starts": "1948-01-01",
    },
    {
        "key": "customer_cash", "label": "Customer cash / spending capacity",
        "color": "#ffd166", "series_id": "A794RX0Q048SBEA", "frequency": "quarterly",
        "unit": "real personal consumption expenditures per capita (chained dollars)",
        "source": "BEA via FRED", "starts": "1947-01-01",
    },
]


def fetch_series(item):
    url = BASE.format(series_id=item["series_id"])
    result = subprocess.run(
        ["curl", "--fail", "--location", "--silent", "--show-error", "--retry", "3", "--max-time", "180", url],
        check=True, capture_output=True, text=True,
    )
    rows = csv.DictReader(io.StringIO(result.stdout))
    observations = []
    for row in rows:
        raw = row.get(item["series_id"])
        if not raw or raw == ".":
            continue
        observations.append([row["observation_date"], float(raw)])
    if not observations:
        raise ValueError(f"No observations returned for {item['series_id']}")
    return {**item, "url": url, "observations": observations}


def main():
    path = Path(sys.argv[1]) if len(sys.argv) == 2 else Path("us_history.json")
    if len(sys.argv) > 2:
        print("Usage: python3 fetch_us_history.py [us_history.json]", file=sys.stderr)
        return 2
    series = [fetch_series(item) for item in SERIES]
    payload = {
        "title": "United States household-circulation history",
        "retrieved_at": date.today().isoformat(),
        "rule": "Source observations are retained at their published cadence. The dashboard does not interpolate missing periods.",
        "series": series,
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("Wrote " + str(path) + ": " + ", ".join(f"{item['key']}={len(item['observations'])}" for item in series))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
