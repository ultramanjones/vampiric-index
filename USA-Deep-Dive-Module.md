# Blueprint Specification: US Liquidity Transmission & Asset Contagion Engine

## Objective
Expand the Vampiric Index pipeline to track the macroeconomic transmission lag inside the United States: measuring the exact sequence from base-layer consumer exhaustion (working-class liquidity collapse) to debt saturation, corporate cash-flow squeeze, and institutional asset repricing.

---

## Technical Stack & Constraints
- Python 3 (standard library only: `urllib.request`, `json`, `sys`, `xml.etree.ElementTree`, `datetime`).
- No external Python dependencies (no `requests`, `pandas`, or `numpy`).
- Data persisted cleanly into `us_transmission.json`.
- Integrated seamlessly into the existing `vampiric-index` repository and rendered in `index.html`.

---

## 1. Transmission Cascade Architecture (Four Phases)

The script must evaluate four discrete transmission stages, scoring each from 0.0 to 25.0 (Cumulative Transmission Score: 0–100, where higher indicates deeper contagion into financial assets):

### Phase 1: Base-Layer Consumer Exhaustion (The Floor)
- **Concept**: Bottom 50% income bracket exhausts cash buffers and purchasing power.
- **Canary Indicators**:
  * **QSR Foot Traffic & Unit Sales**: McDonald's (MCD), Wendy's (WEN), Domino's (DPZ). Focus on customer traffic/transaction count declines vs. headline price-gouged revenue.
  * **Deep Discount / Dollar Store Distress**: Dollar General (DG), Dollar Tree (DLTR), Family Dollar unit sales and discretionary basket collapse.
  * **Desperation Value Campaigns**: Surge of emergency sub-$5 value bundle marketing campaigns indicating foot-traffic panic.
- **Scoring Logic (0–25)**: Evaluates negative transaction trends, traffic drop velocity, and retail down-trading signals.

### Phase 2: Debt Saturation & Shadow Credit Exhaustion
- **Concept**: Households max out revolving credit and emergency micro-loans to fund core survival expenses (food, utilities).
- **Core Indicators & Public FRED Data Series**:
  * `DRCCLACBS`: Delinquency Rate on Credit Cards, All Commercial Banks.
  * `TOTALSL`: Total Consumer Credit Owned and Securitized.
  * Subprime Auto Loan Delinquency (60+ days past due).
  * Buy Now, Pay Later (BNPL) default rates on groceries and essentials.
- **Scoring Logic (0–25)**: Measures delinquency rate steepness relative to historical pre-recession thresholds.

### Phase 3: Corporate Cash-Flow Pinch & Regional Credit Stress
- **Concept**: Revenue drop at the consumer base propagates up the supply chain, squeezing lower-tier corporate margins and regional balance sheets.
- **Core Indicators**:
  * `BAMLH0A0HYM2`: ICE BofA US High Yield Index Option-Adjusted Spread (HY OAS).
  * Retail and Consumer Goods Chapter 11 bankruptcy filing rates.
  * Regional bank non-performing loan (NPL) reserves and commercial paper spreads.
- **Scoring Logic (0–25)**: Measures spread widening over Treasuries and distress frequency in vulnerable corporate sectors.

### Phase 4: Institutional Asset Repricing & Liquidity Drain
- **Concept**: Unraveling reaches sovereign asset valuations, broad-market equities, and private equity / leveraged collateral.
- **Core Indicators**:
  * Market Breadth Divergence: Mega-cap tech / top-10 concentration vs. Russell 2000 small-cap debt rollover stress.
  * Reverse Repo Facility (RRF) balance and Fed Net Liquidity drain (`WALCL` minus TGA minus RRP).
  * FINRA Margin Debt liquidation indicators.
- **Scoring Logic (0–25)**: Measures liquidity buffer depletion and equity concentration fragility.

---

## 2. Deliverables & Execution Requirements

### A. Data Ingestion & Calculation Engine (`fetch_us_transmission.py`)
1. Implement `fetch_us_transmission.py` using Python standard library.
2. Pull public economic time series directly from free endpoints (e.g., St. Louis Fed FRED public data endpoints via `urllib.request`) and scrape corporate QSR distress signals via Google News / SEC RSS.
3. Compute:
   - Phase 1 score (0–25)
   - Phase 2 score (0–25)
   - Phase 3 score (0–25)
   - Phase 4 score (0–25)
   - Total Transmission Index (0–100)
   - Active Contagion Phase (Phase 1, 2, 3, or 4)
4. Output results to `us_transmission.json` with historical snapshots, indicator metadata, source links, and clear textual diagnoses.

### B. Master Pipeline Integration (`run_pipeline.sh`)
Update `run_pipeline.sh` to orchestrate:
1. `python3 fetch_dispatches.py data.json`
2. `python3 fetch_us_transmission.py us_transmission.json`
3. `python3 calculate_hvi.py data.json`

### C. Dashboard Visualization (`index.html`)
1. When the user clicks on the **United States** map polygon or opens the US Dossier, display a dedicated **"US Liquidity Transmission Gauge"** sub-panel.
2. Render:
   - Contagion Progress Bar (Phase 1 → Phase 2 → Phase 3 → Phase 4).
   - Real-Economy Canary Card (McDonald's/QSR foot traffic status and retail down-trading warnings).
   - Credit Exhaustion & Spread Metrics with live values.
   - Narrative Gothic analysis of current institutional lag and distance to asset repricing.

---

## 3. Autonomous Execution Protocol
1. Write and verify `fetch_us_transmission.py` and initial `us_transmission.json`.
2. Update `index.html` and verify UI responsiveness, styling, and drawer integration.
3. Run `bash run_pipeline.sh` and ensure zero runtime errors.
4. Stage all changes, commit with `feat: implement US liquidity transmission and asset contagion engine`, and push to `origin main`.
