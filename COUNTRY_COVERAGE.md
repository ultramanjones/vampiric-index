# Country Coverage Register

## Top-20 nominal-GDP roster — reviewed 2026-10-18

### Selection rule and authoritative source

The tracked roster is the top 20 **sovereign economies by nominal GDP in current US
dollars**. It is taken from the World Bank World Development Indicators (WDI)
[`NY.GDP.MKTP.CD` — GDP (current US$)](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD),
reference year **2024**. The machine-readable source query and the exact values are
stored in `data.json` under `metadata.coverage_roster`; it was retrieved on
2026-10-18 from the [World Bank API](https://api.worldbank.org/v2/country/USA;CHN;DEU;JPN;IND;GBR;FRA;ITA;CAN;BRA;RUS;KOR;MEX;AUS;ESP;IDN;NLD;TUR;SAU;CHE/indicator/NY.GDP.MKTP.CD?date=2024&format=json&per_page=100).

| Rank | Economy | ISO-2 | 2024 GDP (current US$) |
| ---: | --- | --- | ---: |
| 1 | United States | US | $29.298tn |
| 2 | China | CN | $18.730tn |
| 3 | Germany | DE | $4.686tn |
| 4 | Japan | JP | $4.190tn |
| 5 | India | IN | $3.761tn |
| 6 | United Kingdom | GB | $3.696tn |
| 7 | France | FR | $3.160tn |
| 8 | Italy | IT | $2.383tn |
| 9 | Canada | CA | $2.270tn |
| 10 | Russian Federation | RU | $2.186tn |
| 11 | Brazil | BR | $2.186tn |
| 12 | Republic of Korea | KR | $1.875tn |
| 13 | Mexico | MX | $1.830tn |
| 14 | Australia | AU | $1.757tn |
| 15 | Spain | ES | $1.726tn |
| 16 | Indonesia | ID | $1.396tn |
| 17 | Türkiye | TR | $1.359tn |
| 18 | Saudi Arabia | SA | $1.254tn |
| 19 | Netherlands | NL | $1.214tn |
| 20 | Switzerland | CH | $0.970tn |

### Published score rubric: coverage-input v1

For records added under coverage-input v1, each pillar is rounded to one decimal
**before** summing. `calculate_hvi.py` validates the declared score and strict grade;
it never recalculates and writes either field.

| Pillar | Source reading and transform |
| --- | --- |
| `survival_floor` | WDI life expectancy at birth (`SP.DYN.LE00.IN`), 2023 / 4 |
| `sovereign_cannibalization` | WDI GNI per capita, Atlas method/current US$ (`NY.GNP.PCAP.CD`), 2024 / 2,000, capped at 25 |
| `labor_retention` | WDI employment-to-population ratio, ages 15+ (`SL.EMP.TOTL.SP.ZS`), ILO modeled estimate, 2024 / 4 |
| `state_coercion` | Freedom House *Freedom in the World 2025* total score / 4 |

The WDI source endpoints and the Freedom House country report URL, observation/edition,
and raw reading are recorded per country in `data.json.review`. The three WDI indicators
were retrieved from their documented APIs on 2026-10-18. The Freedom House 2025 edition
is retained as the latest country-comparable published edition used for this review.
These are explicit proxy scales, not causal claims.

The original US, GB, FR, DE, and MX entries remain labelled **legacy pilot**. Their
current four readings were reviewed and retained in their review records, but no
source-backed crosswalk from their hand-calibrated historical score to coverage-input
v1 exists. Their declared pillars, total, and grade therefore remain unchanged rather
than being silently recalibrated.

### Review results

| Code | HVI | Grade | Review determination |
| --- | ---: | --- | --- |
| US | 45.0 | F | Legacy pilot retained; no reproducible recalibration rule. |
| CN | 44.1 | F | v1 readings reproduce declared score; no revision. |
| DE | 65.0 | D | Legacy pilot retained; no reproducible recalibration rule. |
| JP | 79.0 | C | v1 readings reproduce declared score; no revision. |
| IN | 48.4 | F | v1 readings reproduce declared score; no revision. |
| GB | 42.0 | F | Legacy pilot retained; no reproducible recalibration rule. |
| FR | 49.0 | F | Legacy pilot retained; no reproducible recalibration rule. |
| IT | 74.2 | C | v1 readings reproduce declared score; no revision. |
| CA | 84.8 | C | New v1 record. |
| RU | 44.1 | F | New v1 record. |
| BR | 56.8 | D | New v1 record. |
| KR | 75.2 | C | New v1 record. |
| MX | 37.0 | F | Legacy pilot retained; no reproducible recalibration rule. |
| AU | 85.6 | B | New v1 record. |
| ES | 73.1 | C | New v1 record. |
| ID | 50.7 | D | New v1 record. |
| TR | 46.6 | F | New v1 record. |
| SA | 55.6 | D | New v1 record. |
| NL | 85.9 | B | New v1 record. |
| CH | 86.0 | B | New v1 record. |

### Acute dispatches and dashboard integration

Every roster country has a country-specific Google News RSS query in
`fetch_dispatches.py`, a current-run dispatch list with title, publisher, publication
date, and URL in `data.json`, and a World Atlas numeric identifier in `index.html`.
The fetcher is atomic: if any country feed fails, it leaves the dataset unchanged.
Dispatches are evidence for current monitoring, not automatic score inputs; the review
rule above governs score changes.
