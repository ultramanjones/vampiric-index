# Country Coverage Register

## Nominal-GDP coverage roster — reviewed 2026-10-18

### Selection rule and authoritative source

The tracked roster contains sovereign economies in descending nominal GDP order, drawn from the World Bank World Development Indicators (WDI) [`NY.GDP.MKTP.CD` — GDP (current US$)](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD), reference year **2024**. The World Bank all-economies API and country-metadata endpoint were retrieved on 2026-10-18; the metadata filters aggregates and non-sovereign economies. Exact values, the selected ordering, source URL, and retrieval date are stored in `data.json` under `metadata.coverage_roster`.

The prior batch ended with Samoa. The current source query ranks St. Vincent and the Grenadines at 186 (US$1.157bn), Sao Tome and Principe at 188 (US$0.825bn), and Tonga at 190 (US$0.647bn); each has complete coverage-input v1 readings and is tracked. St. Kitts and Nevis, rank 187 (US$1.122bn), and Dominica, rank 189 (US$0.689bn), are blocked because WDI returned no required 2024 employment-to-population observation; they are recorded in `metadata.coverage_roster.blocked_candidates`, with the source URL, rather than receiving invented scores. Grenada, rank 183 (US$1.351bn), is blocked for the same reason. Sint Maarten and Turks and Caicos Islands at ranks 179–180 are non-sovereign and excluded. The next eligible sovereign economy is Micronesia, Fed. Sts. (rank 191). This is a later WDI ranking snapshot than the historic rank labels in the table below; source ordering and exact values in `data.json` are authoritative where WDI revisions change a historical position. Ukraine, Sudan, Lebanon, Kosovo, Monaco, Liechtenstein, Andorra, Seychelles, and Antigua and Barbuda are also blocked because required WDI readings are unavailable; each is documented the same way. Hong Kong SAR, China, Puerto Rico, Macao SAR, China, Bermuda, New Caledonia, the Cayman Islands, French Polynesia, Aruba, the Faroe Islands, and Curaçao are non-sovereign economies and are excluded under the selection rule. The source query is [World Bank API: all-economies GDP readings](https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?date=2024&format=json&per_page=400).

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
| 93 | Sudan | SD | $0.050tn (blocked: required 2024 employment reading unavailable) |
| 94 | Libya | LY | $0.048tn |
| 95 | Bahrain | BH | $0.047tn |
| 96 | Cambodia | KH | $0.046tn |
| 97 | Paraguay | PY | $0.045tn |
| 98 | Turkmenistan | TM | $0.044tn |
| 99 | Latvia | LV | $0.044tn |
| 100 | Nepal | NP | $0.043tn |
| 101 | Estonia | EE | $0.043tn |
| 103 | Zimbabwe | ZW | $0.042tn |
| 104 | Cyprus | CY | $0.038tn |
| 105 | Honduras | HN | $0.037tn |
| 106 | El Salvador | SV | $0.035tn |
| 107 | Georgia | GE | $0.034tn |
| 108 | Iceland | IS | $0.033tn |
| 109 | Senegal | SN | $0.032tn |
| 110 | Papua New Guinea | PG | $0.031tn |
| 111 | Bosnia and Herzegovina | BA | $0.030tn |
| 112 | Albania | AL | $0.027tn |
| 113 | Mali | ML | $0.027tn |
| 114 | Lebanon | LB | $0.026tn (blocked: required 2024 employment reading unavailable) |
| 115 | Armenia | AM | $0.026tn |
| 116 | Trinidad and Tobago | TT | $0.026tn |
| 117 | Zambia | ZM | $0.025tn |
| 118 | Malta | MT | $0.025tn |
| 119 | Guinea | GN | $0.025tn |
| 120 | Guyana | GY | $0.025tn |
| 121 | Haiti | HT | $0.024tn |
| 122 | Mongolia | MN | $0.024tn |
| 123 | Burkina Faso | BF | $0.023tn |
| 124 | Mozambique | MZ | $0.023tn |
| 125 | Jamaica | JM | $0.022tn |
| 126 | Benin | BJ | $0.021tn |
| 124 | Gabon | GA | $0.021tn |
| 125 | Chad | TD | $0.020tn |
| 126 | Niger | NE | $0.020tn |
| 127 | Nicaragua | NI | $0.020tn |
| 128 | Botswana | BW | $0.019tn |
| 129 | Moldova | MD | $0.018tn |
| 130 | Kyrgyz Republic | KG | $0.018tn |
| 131 | Afghanistan | AF | $0.018tn |
| 132 | Madagascar | MG | $0.018tn |
| 133 | North Macedonia | MK | $0.017tn |
| 134 | Lao PDR | LA | $0.017tn |
| 135 | Bahamas, The | BS | $0.016tn |
| 136 | Congo, Rep. | CG | $0.016tn |
| 137 | Brunei Darussalam | BN | $0.015tn |
| 138 | Rwanda | RW | $0.015tn |
| 139 | Mauritius | MU | $0.015tn |
| 140 | Tajikistan | TJ | $0.014tn |
| 141 | Namibia | NA | $0.014tn |
| 142 | Equatorial Guinea | GQ | $0.013tn |
| 143 | Somalia, Fed. Rep. | SO | $0.012tn |
| 144 | Malawi | MW | $0.011tn |
| 145 | Kosovo | XK | $0.011tn (blocked: required 2024 employment reading unavailable) |
| 146 | Monaco | MC | $0.011tn (blocked: required 2024 GNI-per-capita and employment readings unavailable) |
| 147 | Mauritania | MR | $0.011tn |
| 148 | Togo | TG | $0.011tn |
| 150 | Liechtenstein | LI | $0.009tn (blocked: required 2024 GNI-per-capita and employment readings unavailable) |
| 152 | Montenegro | ME | $0.008tn |
| 154 | Barbados | BB | $0.008tn |
| 155 | Maldives | MV | $0.007tn |
| 156 | Sierra Leone | SL | $0.007tn |
| 158 | Fiji | FJ | $0.006tn |
| 159 | Eswatini | SZ | $0.005tn |
| 160 | Liberia | LR | $0.005tn |
| 161 | Suriname | SR | $0.004tn |
| 163 | Djibouti | DJ | $0.004tn |
| 165 | Andorra | AD | $0.004tn (blocked: required 2024 employment reading unavailable) |
| 167 | Bhutan | BT | $0.003tn |
| 168 | Belize | BZ | $0.003tn |
| 169 | Burundi | BI | $0.003tn |
| 170 | Central African Republic | CF | $0.003tn |
| 171 | Cabo Verde | CV | $0.003tn |
| 172 | St. Lucia | LC | $0.003tn |
| 173 | The Gambia | GM | $0.002tn |
| 174 | Lesotho | LS | $0.002tn |
| 175 | Seychelles | SC | $0.002tn (blocked: required 2024 employment reading unavailable) |
| 176 | Guinea-Bissau | GW | $0.002tn |
| 177 | Antigua and Barbuda | AG | $0.002tn (blocked: required 2024 employment reading unavailable) |
| 178 | Timor-Leste | TL | $0.002tn |
| 179 | Sint Maarten (Dutch part) | SX | $0.002tn (non-sovereign; excluded) |
| 180 | Turks and Caicos Islands | TC | $0.002tn (non-sovereign; excluded) |
| 181 | Comoros | KM | $0.002tn |
| 182 | Solomon Islands | SB | $0.002tn |
| 183 | Grenada | GD | $0.001tn (blocked: required 2024 employment reading unavailable) |
| 184 | Vanuatu | VU | $0.001tn |
| 185 | Samoa | WS | $0.001tn |
| 186 | St. Vincent and the Grenadines | VC | $0.001tn |
| 187 | St. Kitts and Nevis | KN | $0.001tn (blocked: required 2024 employment reading unavailable) |
| 188 | Sao Tome and Principe | ST | $0.001tn |
| 189 | Dominica | DM | $0.001tn (blocked: required 2024 employment reading unavailable) |
| 190 | Tonga | TO | $0.001tn |

### Published score rubric: coverage-input v1

For records added under coverage-input v1, each pillar is rounded to one decimal **before** summing. `calculate_hvi.py` validates the declared score and strict grade; it never recalculates and writes either field.

| Pillar | Source reading and transform |
| --- | --- |
| `survival_floor` | WDI life expectancy at birth (`SP.DYN.LE00.IN`), 2023 / 4 |
| `sovereign_cannibalization` | WDI GNI per capita, Atlas method/current US$ (`NY.GNP.PCAP.CD`), 2024 / 2,000, capped at 25 |
| `labor_retention` | WDI employment-to-population ratio, ages 15+ (`SL.EMP.TOTL.SP.ZS`), ILO modeled estimate, 2024 / 4 |
| `state_coercion` | Freedom House *Freedom in the World* country-edition total score / 4 |

The WDI source endpoints and Freedom House country report URL, observation/edition, and raw reading are recorded per country in `data.json.review`. The three WDI indicators and the sovereign GDP roster were retrieved from their documented APIs on 2026-10-18. The current top-20 review uses the country-comparable *Freedom in the World 2026* edition; the remaining covered countries retain their previously reviewed 2025-edition readings until their next full review. These are explicit proxy scales, not causal claims.

The original US, GB, FR, DE, and MX entries remain labelled **legacy pilot**. Their current four readings were reviewed and retained in their review records, but no source-backed crosswalk from their hand-calibrated historical score to coverage-input v1 exists. Their declared pillars, total, and grade therefore remain unchanged rather than being silently recalibrated.

### Review results

On 2026-10-18 the current top 20 were re-checked against the World Bank all-economies 2024 nominal-GDP query (with WDI country metadata excluding aggregates and non-sovereign economies). The ordering remains US, CN, DE, JP, IN, GB, FR, IT, CA, RU, BR, KR, MX, AU, ES, ID, TR, SA, NL, CH. All three WDI pillar readings remained available; *Freedom in the World 2026* supplied the current coercion reading. The legacy-pilot records (US, DE, GB, FR, MX) retain their declared values because no published legacy-to-v1 crosswalk exists. The coverage-input-v1 revisions are CN 44.1→44.0 (the cited 9/100 Freedom House reading is deterministically transformed as 9 ÷ 4, rounded once), IN 48.4→48.1, IT 74.2→73.5, BR 56.8→57.0, KR 75.2→75.8, AU 85.6→85.3, ES 73.1→73.4, and TR 46.6→46.4; none crosses a grade threshold. Every other top-20 v1 record reproduced its declared score. Current Google News RSS dispatches, with publisher, publication date, and link, are stored in each dossier's `acute_dispatch` array; they were reviewed as monitoring evidence only and do not automatically alter a pillar.

| Code | HVI | Grade | Review determination |
| --- | ---: | --- | --- |
| US | 45.0 | F | Legacy pilot retained; no reproducible recalibration rule. |
| CN | 44.0 | F | Current v1 review: Freedom House 2026 reading supports revision. |
| DE | 65.0 | D | Legacy pilot retained; no reproducible recalibration rule. |
| JP | 79.0 | C | v1 readings reproduce declared score; no revision. |
| IN | 48.1 | F | Current v1 review: Freedom House 2026 reading supports revision. |
| GB | 42.0 | F | Legacy pilot retained; no reproducible recalibration rule. |
| FR | 49.0 | F | Legacy pilot retained; no reproducible recalibration rule. |
| IT | 73.5 | C | Current v1 review: Freedom House 2026 reading supports revision. |
| CA | 84.8 | C | New v1 record. |
| RU | 44.1 | F | New v1 record. |
| BR | 57.0 | D | Current v1 review: Freedom House 2026 reading supports revision. |
| KR | 75.8 | C | Current v1 review: Freedom House 2026 reading supports revision. |
| MX | 37.0 | F | Legacy pilot retained; no reproducible recalibration rule. |
| AU | 85.3 | B | Current v1 review: Freedom House 2026 reading supports revision. |
| ES | 73.4 | C | Current v1 review: Freedom House 2026 reading supports revision. |
| ID | 50.7 | D | New v1 record. |
| TR | 46.4 | F | Current v1 review: Freedom House 2026 reading supports revision. |
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
| SD | — | — | Blocked: World Bank WDI has no 2024 `SL.EMP.TOTL.SP.ZS` reading; no score declared. |
| LY | 33.0 | F | New v1 record. |
| BH | 54.9 | D | New v1 record. |
| KH | 45.3 | F | New v1 record. |
| PY | 54.0 | D | New v1 record. |
| TM | 30.6 | F | New v1 record. |
| LV | 66.1 | C | New v1 record. |
| NP | 42.6 | F | New v1 record. |
| EE | 73.2 | C | New v1 record. |
| ZW | 38.7 | F | New v1 record. |
| CY | 75.3 | C | New v1 record. |
| HN | 45.0 | F | New v1 record. |
| SV | 46.0 | F | New v1 record. |
| GE | 49.5 | F | New v1 record. |
| IS | 87.5 | B | New v1 record. |
| SN | 47.8 | F | New v1 record. |
| PG | 45.7 | F | New v1 record. |
| BA | 47.9 | F | New v1 record. |
| AL | 56.2 | D | New v1 record. |
| ML | 37.9 | F | New v1 record. |
| LB | — | — | Blocked: World Bank WDI has no 2024 `SL.EMP.TOTL.SP.ZS` reading; no score declared. |
| AM | 49.9 | F | New v1 record. |
| TT | 62.6 | D | New v1 record. |
| ZM | 45.0 | F | New v1 record. |
| MT | 76.6 | C | New v1 record. |
| GN | 35.4 | F | New v1 record. |
| GY | 61.3 | D | New v1 record. |
| HT | 36.3 | F | New v1 record. |
| MN | 56.0 | D | New v1 record. |
| BF | 37.6 | F | New v1 record. |
| MZ | 45.1 | F | New v1 record. |
| JM | 58.5 | D | New v1 record. |
| BJ | 49.9 | F | New v1 record. |
| GA | 37.5 | F | New v1 record. |
| TD | 32.8 | F | New v1 record. |
| NE | 42.2 | F | New v1 record. |
| NI | 39.2 | F | New v1 record. |
| BW | 53.0 | D | New v1 record. |
| MD | 54.0 | D | New v1 record. |
| KG | 39.3 | F | New v1 record. |
| AF | 26.8 | F | New v1 record. |
| MG | 49.4 | F | New v1 record. |
| MK | 51.2 | D | New v1 record. |
| MU | 60.6 | D | New v1 record. |
| TJ | 28.8 | F | New v1 record. |
| NA | 49.0 | F | New v1 record. |
| GQ | 34.1 | F | New v1 record. |
| SO | 23.9 | F | New v1 record. |
| MW | 49.0 | F | New v1 record. |
| XK | — | — | Blocked: World Bank WDI has no 2024 `SL.EMP.TOTL.SP.ZS` reading. |
| MC | — | — | Blocked: World Bank WDI has no 2024 `NY.GNP.PCAP.CD` or `SL.EMP.TOTL.SP.ZS` reading. |
| MR | 36.9 | F | New v1 record. |
| TG | 39.7 | F | New v1 record. |
| LI | — | — | Blocked: World Bank WDI has no 2024 `NY.GNP.PCAP.CD` or `SL.EMP.TOTL.SP.ZS` reading. |
| ME | 55.1 | D | New v1 record. |
| BB | 70.4 | C | New v1 record. |
| MV | 51.4 | D | New v1 record. |
| SL | 44.0 | F | New v1 record. |
| FJ | 51.2 | D | New v1 record. |
| SZ | 30.3 | F | New v1 record. |
| LR | 50.7 | D | New v1 record. |
| SR | 53.8 | D | New v1 record. |
| DJ | 30.2 | F | New v1 record. |
| BT | 53.1 | D | New v1 record. |
| BZ | 56.8 | D | New v1 record. |
| BI | 38.6 | F | New v1 record. |
| CF | 33.1 | F | New v1 record. |
| CV | 57.1 | D | New v1 record. |
| KM | 41.1 | F | New v1 record. |
| SB | 57.9 | D | New v1 record. |
| GD | — | — | Blocked: World Bank WDI has no 2024 `SL.EMP.TOTL.SP.ZS` reading; no score declared. |
| VU | 54.4 | D | New v1 record. |
| WS | 51.6 | D | New v1 record. |
| VC | 59.8 | D | New v1 record. |
| KN | — | — | Blocked: World Bank WDI has no 2024 `SL.EMP.TOTL.SP.ZS` reading; no score declared. |
| ST | 45.2 | F | New v1 record. |
| DM | — | — | Blocked: World Bank WDI has no 2024 `SL.EMP.TOTL.SP.ZS` reading; no score declared. |
| TO | 53.4 | D | New v1 record. |

### Acute dispatches and dashboard integration

Every tracked roster country has a country-specific Google News RSS query in `fetch_dispatches.py`, a current-run dispatch list with title, publisher, publication date, and URL in `data.json`, and a World Atlas numeric identifier in `index.html`. The fetcher is atomic: if any country feed fails, it leaves the dataset unchanged. Dispatches are evidence for current monitoring, not automatic score inputs; the review rule above governs score changes. The active household-circulation v2 scorecard is populated only where all five documented World Bank readings are available; missing inputs are explicitly labelled unavailable rather than imputed.
