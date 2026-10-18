# Country Coverage Register

## Top-45 nominal-GDP roster — reviewed 2026-10-18

### Selection rule and authoritative source

The tracked roster is the top 45 **sovereign economies by nominal GDP in current US dollars**. It is drawn from the World Bank World Development Indicators (WDI) [`NY.GDP.MKTP.CD` — GDP (current US$)](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD), reference year **2024**. The World Bank API was retrieved on 2026-10-18. Its country metadata endpoint was used to exclude aggregates and non-sovereign economies; exact values, ordering, source URL, and retrieval date are stored in `data.json` under `metadata.coverage_roster`.

The next five untracked sovereign economies after Egypt were added in strict descending WDI order: Romania, Pakistan, Czechia, Chile, and Portugal. Hong Kong SAR, China ($408.369bn) falls between Colombia and South Africa in the WDI economy list but is not a sovereign economy and is excluded under the selection rule. The source query is [World Bank API: 45-country GDP readings](https://api.worldbank.org/v2/country/USA;CHN;DEU;JPN;IND;GBR;FRA;ITA;CAN;RUS;BRA;KOR;MEX;AUS;ESP;IDN;TUR;SAU;NLD;CHE;POL;BEL;ARG;IRL;SWE;SGP;ARE;ISR;AUT;THA;NOR;VNM;IRN;PHL;BGD;DNK;MYS;COL;ZAF;EGY;ROU;PAK;CZE;CHL;PRT/indicator/NY.GDP.MKTP.CD?date=2024&format=json&per_page=100).

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
| 21 | Poland | PL | $0.918tn |
| 22 | Belgium | BE | $0.671tn |
| 23 | Argentina | AR | $0.638tn |
| 24 | Ireland | IE | $0.609tn |
| 25 | Sweden | SE | $0.605tn |
| 26 | Singapore | SG | $0.573tn |
| 27 | United Arab Emirates | AE | $0.552tn |
| 28 | Israel | IL | $0.542tn |
| 29 | Austria | AT | $0.535tn |
| 30 | Thailand | TH | $0.529tn |
| 31 | Norway | NO | $0.501tn |
| 32 | Vietnam | VN | $0.476tn |
| 33 | Iran | IR | $0.475tn |
| 34 | Philippines | PH | $0.462tn |
| 35 | Bangladesh | BD | $0.450tn |
| 36 | Denmark | DK | $0.425tn |
| 37 | Malaysia | MY | $0.422tn |
| 38 | Colombia | CO | $0.421tn |
| 39 | South Africa | ZA | $0.401tn |
| 40 | Egypt | EG | $0.389tn |
| 41 | Romania | RO | $0.383tn |
| 42 | Pakistan | PK | $0.372tn |
| 43 | Czechia | CZ | $0.347tn |
| 44 | Chile | CL | $0.329tn |
| 45 | Portugal | PT | $0.314tn |

### Published score rubric: coverage-input v1

For records added under coverage-input v1, each pillar is rounded to one decimal **before** summing. `calculate_hvi.py` validates the declared score and strict grade; it never recalculates and writes either field.

| Pillar | Source reading and transform |
| --- | --- |
| `survival_floor` | WDI life expectancy at birth (`SP.DYN.LE00.IN`), 2023 / 4 |
| `sovereign_cannibalization` | WDI GNI per capita, Atlas method/current US$ (`NY.GNP.PCAP.CD`), 2024 / 2,000, capped at 25 |
| `labor_retention` | WDI employment-to-population ratio, ages 15+ (`SL.EMP.TOTL.SP.ZS`), ILO modeled estimate, 2024 / 4 |
| `state_coercion` | Freedom House *Freedom in the World 2025* total score / 4 |

The WDI source endpoints and Freedom House country report URL, observation/edition, and raw reading are recorded per country in `data.json.review`. The three WDI indicators were retrieved from their documented APIs on 2026-10-18. The Freedom House 2025 edition is retained as the latest country-comparable published edition used for this review. These are explicit proxy scales, not causal claims.

The original US, GB, FR, DE, and MX entries remain labelled **legacy pilot**. Their current four readings were reviewed and retained in their review records, but no source-backed crosswalk from their hand-calibrated historical score to coverage-input v1 exists. Their declared pillars, total, and grade therefore remain unchanged rather than being silently recalibrated.

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
| PL | 65.2 | D | New v1 record. |
| BE | 82.3 | C | New v1 record. |
| AR | 61.7 | D | New v1 record. |
| IE | 85.8 | B | New v1 record. |
| SE | 85.4 | B | New v1 record. |
| SG | 74.6 | C | New v1 record. |
| AE | 69.4 | C | New v1 record. |
| IL | 79.8 | C | New v1 record. |
| AT | 82.9 | C | New v1 record. |
| TH | 47.9 | F | New v1 record. |
| NO | 86.4 | B | New v1 record. |
| VN | 43.8 | F | New v1 record. |
| IR | 34.3 | F | New v1 record. |
| PH | 49.2 | F | New v1 record. |
| BD | 45.5 | F | New v1 record. |
| DK | 85.0 | B | New v1 record. |
| MY | 54.1 | D | New v1 record. |
| CO | 54.5 | D | New v1 record. |
| ZA | 49.2 | F | New v1 record. |
| EG | 34.6 | F | New v1 record. |
| RO | 60.9 | D | New v1 record. |
| PK | 38.0 | F | New v1 record. |
| CZ | 73.4 | C | New v1 record. |
| CL | 66.2 | C | New v1 record. |
| PT | 71.8 | C | New v1 record. |

### Acute dispatches and dashboard integration

Every roster country has a country-specific Google News RSS query in `fetch_dispatches.py`, a current-run dispatch list with title, publisher, publication date, and URL in `data.json`, and a World Atlas numeric identifier in `index.html`. The fetcher is atomic: if any country feed fails, it leaves the dataset unchanged. Dispatches are evidence for current monitoring, not automatic score inputs; the review rule above governs score changes.
