# U.S. QSR Traffic / Household Demand Source Map

**Purpose:** Add an honest demand-side signal to the U.S. Transmission Engine without pretending sales, restaurant locations, or search interest are literal customer visits.

**Research date:** 2026-10-19

## Blunt conclusion

A free, stable, legally redistributable national feed of *actual quick-service restaurant visits* was not found. The big mobility vendors have the real modeled-visit data, but it is commercial/licensed:

- [Placer.ai](https://www.placer.ai/) — modeled visits and dwell time; public reports are citable snapshots, detailed data is licensed.
- [SafeGraph Patterns documentation](https://docs.safegraph.com/docs/monthly-patterns) — modeled visits; commercial license.
- [Advan Research](https://www.advanresearch.com/) — commercial mobility data.
- [Near](https://www.near.com/) — commercial location intelligence.

Do not scrape their charts, reconstruct their series, or relabel a paid vendor's prose as a public time series.

That does **not** mean the demand side is unknowable. It means the dashboard must separate three useful kinds of evidence:

1. official restaurant-sector activity proxies,
2. official household surveys about food stress and food-away-from-home spending, and
3. clearly marked commercial/public-report snapshots when they are available.

## Tier 1 — automate these first

### 1. Census monthly restaurant-sector sales — activity proxy, not visits

- **Metric:** Monthly sales for NAICS 722, *Food services and drinking places*.
- **Source:** [Census Monthly Retail Trade Survey API](https://api.census.gov/data/timeseries/eits/mrts.html)
- **Variable catalog:** [MRTS variables](https://api.census.gov/data/timeseries/eits/mrts/variables.html)
- **Cadence:** Monthly.
- **What it proves:** Whether nominal activity in the restaurant sector is rising or falling.
- **What it does not prove:** Customer count, QSR-specific traffic, or real volume. Price increases can raise sales while visits fall.
- **Use in dashboard:** Label exactly: **Restaurant-sector nominal sales (Census, not visits)**. Pair with CPI/food-away-from-home inflation if showing a volume-like direction.

### 2. BLS food-services employment — activity proxy, not visits

- **Metric:** Employment in Food Services and Drinking Places (NAICS 722).
- **Source:** [BLS CES public API, series CES7072200001](https://api.bls.gov/publicAPI/v2/timeseries/data/CES7072200001?startyear=2015&endyear=2026)
- **Cadence:** Monthly.
- **What it proves:** Restaurant-sector labor demand and staffing direction.
- **What it does not prove:** Visits; restaurants may change staffing, hours, productivity, or use delivery platforms.
- **Use in dashboard:** A supporting “demand transmission” line, not a traffic gauge.

### 3. Census Household Pulse Survey — direct household survey signal

- **Metric:** Food sufficiency in the prior seven days. Selected questionnaire phases also include household spending on food prepared away from home, including restaurants, fast food, and takeout.
- **Sources:** [Household Pulse Survey](https://www.census.gov/programs-surveys/household-pulse-survey.html), [datasets and tables](https://www.census.gov/programs-surveys/household-pulse-survey/datasets.html), [technical documentation](https://www.census.gov/programs-surveys/household-pulse-survey/technical-documentation.html).
- **Cadence:** Fielded in published phases/cycles, not one perfectly uninterrupted monthly line.
- **Method:** Probability-based Census household sample with weights and nonresponse adjustment; still an online-response instrument with response-rate limitations.
- **What it proves:** Direct, high-frequency household reports of food insufficiency; where the module exists, reported food-away-from-home spending.
- **Use in dashboard:** A clearly labeled **survey canary**, with each cycle's field dates and question wording preserved.

## Tier 2 — strongest recurring household-hardship surveys

### 4. USDA CPS Food Security Supplement — the meal-skipping series

- **Metric:** Household food insecurity, very low food security, and adults cutting meal size or skipping meals because there was not enough money for food.
- **Sources:** [USDA ERS food-security key statistics](https://www.ers.usda.gov/topics/food-nutrition-assistance/food-security-in-the-u-s/key-statistics-graphics/), [USDA ERS food-security topic page](https://www.ers.usda.gov/topics/food-nutrition-assistance/food-security-in-the-u-s/).
- **Cadence:** Annual; principal series begins in 1995.
- **Method:** Census Current Population Survey Food Security Supplement; nationally representative probability sample.
- **What it proves:** A direct survival outcome: households reporting food hardship or meal reduction because of money.
- **Use in dashboard:** Annual household-depletion validation metric; do not splice it with Pulse food insufficiency as though they were the same survey question.

### 5. Federal Reserve SHED — buffers, credit, and emergency survival

- **Metric:** How adults say they would cover a $400 emergency; whether they would pay cash/savings, revolve a card, borrow, sell something, or cannot pay; emergency savings adequacy.
- **Sources:** [SHED landing page](https://www.federalreserve.gov/consumerscommunities/shed.htm), [downloadable SHED data](https://www.federalreserve.gov/consumerscommunities/shed_data.htm).
- **Cadence:** Annual since 2013.
- **Method:** Probability-recruited Ipsos KnowledgePanel, weighted to U.S. adults.
- **What it proves:** Direct household-reported resilience and dependence on debt for a shock.
- **Use in dashboard:** A yearly counterpart to credit-card APR/revolving-balance stress. Do not count someone using a paid-in-full credit card as equivalent to someone carrying debt.

### 6. Purdue Consumer Food Insights — fast, labeled directional survey

- **Metric:** Monthly food insecurity, food affordability, spending, and food-away-from-home/eating-out behavior; exact modules vary by report.
- **Source:** [Purdue Consumer Food Insights](https://ag.purdue.edu/cfdas/consumer-food-insights/)
- **Cadence:** Monthly since January 2022.
- **Method:** Weighted opt-in online panel (often approximately 1,200 adults), not a probability sample.
- **What it proves:** Fast directional survey evidence on affordability and behavior.
- **What it does not prove:** A definitive national population estimate comparable to CPS or Census.
- **Use in dashboard:** Only with a prominent **weighted opt-in survey** label, report date, sample size, and source link.

## Tier 3 — cited commercial snapshots, not automated data

- Placer.ai public reports can be cited with their publication date and exact coverage.
- Individual public-company earnings releases occasionally split comparable-sales changes into **transactions/traffic** and **average check**. Stronger candidates include:
  - [Chipotle investor news releases](https://ir.chipotle.com/news-releases)
  - [Starbucks financial releases](https://investor.starbucks.com/press-releases/financial-releases/default.aspx)
- These are company-specific, definitions can change, and they must be hand-curated with release dates. They are not a national QSR traffic index.

## Explicit exclusions

| Tempting input | Why it is excluded as a traffic measure |
|---|---|
| Census restaurant sales | Sales can rise due to price inflation while visits decline. |
| BLS restaurant employment | Staffing is not customer count. |
| Yelp review counts / Google search interest | Engagement/search proxies, not visits; terms and method issues. |
| OSM/Overture restaurant POIs | Locations/supply, not demand. |
| Unlicensed extraction of Placer/SafeGraph/Advan charts | Not an auditable or permitted public data pipeline. |

## Recommended implementation order

1. Add **Census NAICS 722 sales** and **BLS NAICS 722 employment** as monthly public activity proxies, labeled honestly.
2. Add a separate **Household Survey Canary** card using the latest available Census Pulse food-sufficiency result and USDA annual food-security/meal-skipping result.
3. Add SHED annual emergency-buffer results to the existing household breathing-room section.
4. Add Purdue only as a clearly labeled faster directional supplement after manually verifying its current report layout/data availability.
5. If a real visit series is later licensed, add it as a separately sourced QSR Traffic line. Do not silently substitute sales for traffic.
