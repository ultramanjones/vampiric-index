cat << 'EOF' > ~/git-repos/vampiric-index/PROJECT_BLUEPRINT.md
# Master Blueprint: Vampiric Index Dashboard

## Overview
A public diagnostic dashboard tracking macroeconomic extraction and institutional strain across sovereign nations. Uses a Gothic aesthetic ("Vampire Infestation") with an empirical, deterministic core metric: Host Viability Index (HVI, 0-100).

## Current Status
- Steps 1 & 2 completed: `calculate_hvi.py` and baseline `data.json` for US, GB, FR, DE, MX exist and are verified.

## Outstanding Pipeline Tasks

### Step 3: Acute Wire Ingestion (`fetch_dispatches.py`)
- Python script using standard library only (`urllib.request`, `xml.etree.ElementTree`, `urllib.parse`, `json`, `sys`).
- Query Google News RSS search endpoints (`https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en`).
- Target country-specific strain terms (inflation, strikes, debt, unrest) with `User-Agent: Mozilla/5.0`.
- Extract the top 2 articles per country: title, source, publication date, link.
- Ingest into the `acute_dispatch` field for each country in `data.json`.
- Test execution: Run `python3 fetch_dispatches.py` and ensure `data.json` populates cleanly.

### Step 4: Frontend Web Dashboard (`index.html`)
- Standalone HTML/CSS/JS file deployable directly on GitHub Pages.
- Visuals: Dark gothic theme (deep black `#0a0a0c`, blood red `#8a0303`, bone `#e2e8f0`).
- Map: Interactive SVG world map using D3.js (via CDN) with Equal Earth projection, centered on prime meridian/Africa.
- Countries colored dynamically by HVI Grade:
  * A (85-100): Emerald muted
  * B (70-84): Amber-green
  * C (55-69): Amber/Orange
  * D (40-54): Crimson/Rust
  * F (<40): Deep Blood Red
- Interactive Dossier: Clicking a tracked country displays a slide-out drawer or modal showing:
  * Country name, ISO code, HVI score, and Grade badge.
  * 4-Pillar breakdown bar gauges (Survival, Sovereign, Labor, Coercion).
  * Chronic Pathologies list.
  * Acute Wire Dispatches list with source and clickable links.
- Reads `data.json` dynamically via `fetch('./data.json')`.

### Step 5: Master Automation Runner (`run_pipeline.sh`)
- Bash runner script orchestrating:
  1. `python3 fetch_dispatches.py` (updates live news dispatches)
  2. `python3 calculate_hvi.py data.json` (validates schema and scores)
- Ensure executable permissions (`chmod +x run_pipeline.sh`).

## Execution Protocol
- Work autonomously until Step 3, Step 4, and Step 5 are fully implemented and verified.
- Commit working milestones to git.
- Report only upon complete verification or unrecoverable blocking error.
EOF
