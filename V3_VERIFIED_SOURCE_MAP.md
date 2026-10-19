# Vampiric Index v3 — Verified Source Map

**Purpose:** Measure the extraction pressure on ordinary people and the resilience/power left to them. This is an early-warning conditions dashboard, **not** a machine that claims it can predict a specific revolt or collapse date.

## Global core: sources actually verified

| Pressure / protection question | Source and exact series | Why it belongs | Main honesty rule |
|---|---|---|---|
| How much national income reaches the lower half? | [World Inequality Database bulk files](https://wid.world/bulk_download/): `sptincj992`, percentile `p0p50` | Direct bottom-50 share of pretax national income, allocated to equal-split adults | It is not household disposable income. Retain WID's `data_quality` field and source year. |
| How concentrated is income at the top? | WID `sptincj992`, `p90p100` | Top-10 share is the opposing capture measure | Do not substitute a survey series without visibly changing the definition. |
| Does the lower half own anything? | WID `shwealj992`, `p0p50` | Bottom-50 net-personal-wealth share | Wealth estimates are more model-dependent; do not hide quality/staleness. |
| How concentrated is wealth at the top? | WID `shwealj992`, `p90p100` | Top-10 wealth share | Shows the asset layer directly rather than inferring it from GDP. |
| How much output reaches labor rather than capital? | [UN SDG API / ILO modelled estimate](https://unstats.un.org/SDGAPI/v1/sdg/Series/Data?seriesCode=SL_EMP_GTOTL): `SL_EMP_GTOTL` | Labour share of GDP, SDG 10.4.1 | It is functional distribution, not median pay or worker power by itself. |
| Are households already cutting food quality/quantity? | [World Bank / FAO](https://api.worldbank.org/v2/country/all/indicator/SN.ITK.MSFI.ZS?format=json&per_page=20000): `SN.ITK.MSFI.ZS`; severe: `SN.ITK.SVFI.ZS` | Moderate-or-severe and severe food insecurity; annual material-strain signal | It is a hardship outcome, not proof of the cause or a forecast of unrest. |
| Is there a protective floor? | [World Bank ASPIRE/WDI](https://api.worldbank.org/v2/country/all/indicator/per_allsp.cov_pop_tot?format=json&per_page=20000): `per_allsp.cov_pop_tot` | Population participating in a social-protection or labor program | Coverage is not adequacy. Optional companion: `per_allsp.adq_pop_tot`. |
| Could households survive a job-income loss? | [Global Findex 2025 CSV](https://thedocs.worldbank.org/en/doc/be6615202d1f08a25855c8ac2d615122-0050012025/related/GlobalFindexDatabase2025.csv): `fin24ba` (<2 weeks of expenses after loss of main income), `fin24bb` (~1 month), `fin24bc` (~2 months), `fin24bd` (>2 months) | Direct survey measure of financial fragility/resilience | It is intermittent survey data; money can come from savings, debt, asset sale, or family. Do not call all "can cover" responses healthy resilience. |

## Confirmed WID spot checks (2024)

Percent of total; WID `data_quality` kept separately.

| Country | Bottom 50 income share | Top 10 income share | Bottom 50 wealth share | Top 10 wealth share |
|---|---:|---:|---:|---:|
| United States | 13.44% | 46.76% | 0.96% | 69.54% |
| Canada | 16.92% | 36.78% | 13.98% | 59.79% |
| Iran | 16.52% | 46.71% | 4.45% | 60.13% |
| Ethiopia | 17.34% | 40.47% | 4.78% | 58.14% |
| Democratic Republic of the Congo | 11.56% | 53.97% | 3.42% | 65.63% |

## The useful pressure model

A real "host is being drained" system should watch separate mechanisms, not mash them into a cheerful GDP score:

1. **Capture:** bottom-half income/wealth shrinking while top shares rise.
2. **Labor extraction:** labor share falls; low-pay, insecure, informal, or underemployed work grows.
3. **Material failure:** food insecurity, rent/utility arrears, debt distress, foregone health care, and residual income collapse.
4. **Buffer failure:** people cannot survive a job loss without debt, asset liquidation, or family rescue; protection coverage is inadequate.
5. **Power / response capacity:** bargaining coverage, ability to organize, rights enforcement, labor inspection, strikes and wage-theft redress — primarily a country-dossier layer because global comparability is thinner.

## What cannot be honestly promised

- These conditions can identify **pressure, vulnerability, and extractive saturation**.
- They cannot prove that a country will revolt or collapse on a particular date.
- Event datasets about protests or conflict should be used, if at all, as a retrospective validation layer — never as a deterministic revolt alarm.
- High GDP, high consumption, or low unemployment must not cancel out extreme concentration, food insecurity, debt, or lack of worker power.

## Next build proof-of-concept

Build v3 alongside v2, not as a destructive rewrite:

1. WID ingestion for income/wealth floor and capture (with quality flags).
2. ILO labor-share ingestion.
3. FAO food-insecurity and Findex financial-fragility panels.
4. United States dossier with the stronger domestic evidence for housing, debt service/delinquency, real median wages, and labor enforcement.
5. Choose score logic only after looking at the raw distributions and missing-data patterns.
