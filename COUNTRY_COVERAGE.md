# Country Coverage Register

## Nominal-GDP coverage roster — reviewed 2026-10-18

### Selection rule and authoritative source

The tracked roster contains sovereign economies in descending nominal GDP order, drawn from the World Bank World Development Indicators (WDI) [`NY.GDP.MKTP.CD` — GDP (current US$)](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD), reference year **2024**. The World Bank all-economies API was retrieved on 2026-10-18. Its country metadata endpoint was used to exclude aggregates and non-sovereign economies; exact values, ordering, source URL, and retrieval date are stored in `data.json` under `metadata.coverage_roster`.

The all-economies query identified a prior roster omission: New Zealand is sovereign-roster rank 51 and is now inserted after Algeria. This run adds the next eligible untracked sequence after Slovenia: Jordan, Bolivia, Uganda, Cameroon, and Tunisia, in that strict WDI order. Ukraine is sovereign-roster rank 56 but was not assigned a record: WDI returned no 2024 observation for the required employment-to-population indicator. It is recorded as a blocker in `metadata.coverage_roster.blocked_candidates`, with its source URL, rather than receiving an invented score. Hong Kong SAR, China (raw economy-list rank 39), Puerto Rico (raw economy-list rank 62), and Macao SAR, China (raw economy-list rank 94) are not sovereign states and are excluded under the selection rule. The source query is [World Bank API: all-economies GDP readings](https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2024&format=json&per_page=400).

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
| 46 | Finland | FI | $0.299tn |
| 47 | Peru | PE | $0.292tn |
| 48 | Kazakhstan | KZ | $0.291tn |
| 49 | Iraq | IQ | $0.280tn |
| 50 | Algeria | DZ | $0.269tn |
| 51 | New Zealand | NZ | $0.261tn |
| 52 | Greece | GR | $0.256tn |
| 53 | Nigeria | NG | $0.252tn |
| 54 | Hungary | HU | $0.223tn |
| 55 | Qatar | QA | $0.216tn |
| 56 | Ukraine | UA | $0.191tn (blocked: required 2024 employment reading unavailable) |
| 57 | Kuwait | KW | $0.161tn |
| 58 | Morocco | MA | $0.161tn |
| 59 | Ethiopia | ET | $0.150tn |
| 60 | Slovak Republic | SK | $0.141tn |
| 61 | Dominican Republic | DO | $0.124tn |
| 62 | Ecuador | EC | $0.124tn |
| 63 | Uzbekistan | UZ | $0.121tn |
| 64 | Venezuela, RB | VE | $0.121tn |
| 65 | Kenya | KE | $0.120tn |
| 66 | Bulgaria | BG | $0.113tn |
| 67 | Guatemala | GT | $0.113tn |
| 68 | Oman | OM | $0.107tn |
| 69 | Angola | AO | $0.103tn |
| 70 | Sri Lanka | LK | $0.100tn |
| 71 | Costa Rica | CR | $0.097tn |
| 72 | Luxembourg | LU | $0.093tn |
| 73 | Croatia | HR | $0.093tn |
| 74 | Serbia | RS | $0.090tn |
| 75 | Cote d'Ivoire | CI | $0.087tn |
| 76 | Panama | PA | $0.087tn |
| 77 | Lithuania | LT | $0.086tn |
| 78 | Ghana | GH | $0.083tn |
| 79 | Uruguay | UY | $0.082tn |
| 80 | Tanzania | TZ | $0.079tn |
| 83 | Belarus | BY | $0.079tn |
| 84 | Democratic Republic of the Congo | CD | $0.076tn |
| 85 | Azerbaijan | AZ | $0.074tn |
| 86 | Myanmar | MM | $0.074tn |
| 87 | Slovenia | SI | $0.073tn |
| 88 | Jordan | JO | $0.059tn |
| 89 | Bolivia | BO | $0.055tn |
| 90 | Uganda | UG | $0.054tn |
| 91 | Cameroon | CM | $0.053tn |
| 92 | Tunisia | TN | $0.051tn |

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
| FI | 84.1 | C | New v1 record. |
| PE | 57.0 | D | New v1 record. |
| KZ | 47.2 | F | New v1 record. |
| IQ | 37.7 | F | New v1 record. |
| DZ | 38.7 | F | New v1 record. |
| NZ | 85.5 | B | New v1 record. |
| GR | 64.8 | D | New v1 record. |
| NG | 45.5 | F | New v1 record. |
| HU | 60.2 | D | New v1 record. |
| QA | 73.6 | C | New v1 record. |
| UA | — | — | Blocked: World Bank WDI has no 2024 `SL.EMP.TOTL.SP.ZS` reading; no score declared. |
| KW | 67.2 | C | New v1 record. |
| MA | 40.0 | F | New v1 record. |
| ET | 38.4 | F | New v1 record. |
| SK | 67.7 | C | New v1 record. |
| DO | 55.9 | D | New v1 record. |
| EC | 54.3 | D | New v1 record. |
| UZ | 36.5 | F | New v1 record. |
| VE | 35.5 | F | New v1 record. |
| KE | 45.6 | F | New v1 record. |
| BG | 58.6 | D | New v1 record. |
| GT | 47.6 | F | New v1 record. |
| OM | 52.3 | D | New v1 record. |
| AO | 40.7 | F | New v1 record. |
| LK | 48.7 | F | New v1 record. |
| CR | 64.3 | D | New v1 record. |
| LU | 84.5 | C | New v1 record. |
| HR | 63.6 | D | New v1 record. |
| RS | 51.7 | D | New v1 record. |
| CI | 44.7 | F | New v1 record. |
| PA | 64.6 | D | New v1 record. |
| LT | 70.1 | C | New v1 record. |
| GH | 51.8 | D | New v1 record. |
| UY | 69.6 | C | New v1 record. |
| TZ | 44.9 | F | New v1 record. |
| BY | 39.8 | F | New v1 record. |
| CD | 35.7 | F | New v1 record. |
| AZ | 39.2 | F | New v1 record. |
| MM | 32.5 | F | New v1 record. |
| SI | 74.4 | C | New v1 record. |
| JO | 38.7 | F | New v1 record. |
| BO | 54.3 | D | New v1 record. |
| UG | 45.5 | F | New v1 record. |
| CM | 36.3 | F | New v1 record. |
| TN | 41.6 | F | New v1 record. |

### Acute dispatches and dashboard integration

Every tracked roster country has a country-specific Google News RSS query in `fetch_dispatches.py`, a current-run dispatch list with title, publisher, publication date, and URL in `data.json`, and a World Atlas numeric identifier in `index.html`. The fetcher is atomic: if any country feed fails, it leaves the dataset unchanged. Dispatches are evidence for current monitoring, not automatic score inputs; the review rule above governs score changes.
