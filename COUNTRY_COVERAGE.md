# Country Coverage Register

## 2026-10-17 expansion: China, Japan, India, and Italy

### Selection rule and nominal-GDP source

The coverage queue is descending **nominal GDP in current US dollars**.  The selection
source for this batch is World Bank World Development Indicators (WDI), indicator
[`NY.GDP.MKTP.CD` — GDP (current US$)](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD),
reference year **2024**, retrieved 2026-10-17 through the [World Bank API](https://api.worldbank.org/v2/country/US;CN;DE;JP;IN;GB;FR;IT;CA;RU;BR;MX/indicator/NY.GDP.MKTP.CD?date=2024&format=json).

Existing tracked countries were excluded. The relevant ordered sovereign-economy
observations in that source are: United States (US$29.298tn; already tracked), China
(US$18.730tn), Germany (US$4.686tn; already tracked), Japan (US$4.190tn), India
(US$3.761tn), United Kingdom (US$3.696tn; already tracked), France (US$3.160tn;
already tracked), Italy (US$2.383tn), Canada (US$2.270tn), Russian Federation
(US$2.186tn), Brazil (US$2.186tn), and Mexico (US$1.830tn; already tracked).

Accordingly, this batch adds the next four untracked countries: **CN, JP, IN, IT**.
The next candidate countries, if the same 2024 WDI ordering remains the chosen
reference, are **Canada, Russian Federation, and Brazil** (Russia slightly exceeds
Brazil in the cited observation).

### Score-input method and provenance

The original five-country dashboard is an explicitly hand-calibrated pilot. To avoid
silently presenting a different method as identical, these four records are marked in
this register as **coverage-input v1**. It is a deterministic, source-linked intake
method; it does not revise or retroactively compare the legacy pilot scores.

For each new record, pillars are rounded to one decimal from these fixed transforms:

| Pillar | Input and transform |
| --- | --- |
| `survival_floor` | World Bank WDI life expectancy at birth (`SP.DYN.LE00.IN`), 2023 / 4 |
| `sovereign_cannibalization` | World Bank WDI GNI per capita, Atlas method/current US$ (`NY.GNP.PCAP.CD`), 2024 / 2,000, capped at 25 |
| `labor_retention` | World Bank WDI employment-to-population ratio, ages 15+ (`SL.EMP.TOTL.SP.ZS`), ILO modeled estimate, 2024 / 4 |
| `state_coercion` | Freedom House *Freedom in the World 2025* total score / 4 |

The labels are legacy HVI pillar names. The first three transforms are explicit proxy
scales rather than causal claims; the fourth uses a published civil-liberties and
political-rights score. HVI remains the sum of the four declared, rounded pillars;
`calculate_hvi.py` validates but never overwrites declared scores or grades. Its strict
scale is A ≥93, B ≥85, C ≥66, D ≥50, F <50.

WDI inputs were retrieved from the indicator API endpoints for the four ISO-3 codes:

- [Life expectancy, 2023](https://api.worldbank.org/v2/country/CHN;JPN;IND;ITA/indicator/SP.DYN.LE00.IN?date=2023&format=json)
- [GNI per capita, 2024](https://api.worldbank.org/v2/country/CHN;JPN;IND;ITA/indicator/NY.GNP.PCAP.CD?date=2024&format=json)
- [Employment-to-population ratio, 2024](https://api.worldbank.org/v2/country/CHN;JPN;IND;ITA/indicator/SL.EMP.TOTL.SP.ZS?date=2024&format=json)

Freedom House country reports used for the 2025 total-score input:
[China](https://freedomhouse.org/country/china/freedom-world/2025),
[Japan](https://freedomhouse.org/country/japan/freedom-world/2025),
[India](https://freedomhouse.org/country/india/freedom-world/2025), and
[Italy](https://freedomhouse.org/country/italy/freedom-world/2025).

| Code | Survival | Sovereign | Labor | State | HVI | Grade |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| CN | 19.5 | 6.8 | 15.5 | 2.3 | 44.1 | F |
| JP | 21.0 | 18.6 | 15.4 | 24.0 | 79.0 | C |
| IN | 18.0 | 1.3 | 13.3 | 15.8 | 48.4 | F |
| IT | 20.8 | 19.3 | 11.6 | 22.5 | 74.2 | C |

### Dispatch and map integration

Each added ISO-2 code has a country-specific Google News RSS query in
`fetch_dispatches.py` and its ISO numeric ID in `index.html` (`CN` 156, `JP` 392,
`IN` 356, `IT` 380). Acute dispatches are intentionally fetched atomically by the
pipeline, so a failed country feed leaves `data.json` unchanged.
