# Vampiric Index v3 — Common-People / Labor Conditions Redesign

## The correction

V2’s GNI-per-person and consumption-per-person inputs are useful context, but they are **not a measure of ordinary people’s position**. They are national aggregates divided by population. A large share can go to owners, high earners, foreign investors, or asset holders while median workers remain squeezed.

**Do not keep patching v2’s ceilings and call that a solution.** The USA scoring issue exposed a deeper problem: the wrong kind of number is doing too much work.

The public question should become:

> Can the median worker and the lower half of the population afford a stable life, retain a share of what the country produces, and build any security or power?

## Design rules

1. Lead with medians, lower-half shares, and affordability after essentials — not GDP/GNI averages.
2. Separate outcomes (pay, hardship, wealth) from worker power (bargaining, rights, enforcement).
3. Do not let a high score in one area cancel a severe failure in another.
4. Preserve raw values, source year, definition, source link, and data-quality status.
5. No fabricated universal series. Use a global core, then regional/national dossier modules.
6. Keep v2 visible as a provisional comparison layer while v3 is researched and built beside it. Do not overwrite history.

## Candidate v3 modules

### 1. What reaches ordinary people?

**Question:** Does national income actually reach the median person and the bottom half?

- Median equivalized disposable household income (PPP and local currency)
- Bottom-50 share of income
- Bottom-20 or P20 income relative to the median
- Bottom-50 income trend over 5/10 years
- Top-10 share, shown as the opposing concentration measure

**Best sources:**
- World Inequality Database (WID) distributional national accounts
- OECD Income Distribution Database and LIS for median disposable income
- World Bank Poverty and Inequality Platform only as a clearly labeled survey-based supplement

**WID machine-readable core:**
- `sptinc992j`, `p0p50`: bottom-50 share of pre-tax national income
- `sptinc992j`, `p90p100`: top-10 share of pre-tax national income
- `sdiinc992j` where available: post-tax national-income distribution

WID bulk documentation: https://wid.world/bulk_download/README.md

### 2. Does work pay, and is work secure?

**Question:** Can people obtain enough stable work, at pay that covers life?

- Median hourly earnings, not mean annual pay
- Low-pay incidence / P20 pay relative to median pay
- Real median-pay and lower-pay growth
- Time-related underemployment and labor underutilization
- Informal employment, involuntary part-time work, and youth NEET
- Excessive-hours share

**Global source base:** ILOSTAT. Use mean wage only as context when a country lacks a usable median; never relabel it median pay.

### 3. Does labor retain power?

**Question:** Can workers say no, bargain, organize, and enforce rights?

- Labor share of GDP (ILO SDG 10.4.1) — share of production flowing to labor, not owners
- Collective-bargaining coverage — preferred over union membership alone
- Labor-rights compliance / freedom-of-association evidence
- Labor-inspection capacity and wage-theft enforcement where national data exist
- Workplace injury/fatality rates

The ILO labor share is a global core indicator. Bargaining coverage and enforcement belong in a separate clearly labeled power module; laws on paper do not equal actual protection.

### 4. Can people afford the basics and keep any remainder?

**Question:** What is left after housing, food, utilities, transport, health care, and debt?

- Housing-cost burden and, preferably, residual income after housing
- Food insecurity
- Energy insecurity / utility arrears
- Out-of-pocket health burden and foregone care due to cost
- Household debt exposure plus arrears/debt-service distress where available
- Essential transport and childcare burden in country dossiers

There is no honest universal annual rent-burden dataset. EU-SILC has high-quality European housing/arrears measures; elsewhere this needs national dossiers, not made-up global comparisons.

### 5. Does the bottom half own anything or have a buffer?

**Question:** Are people building security, or merely servicing claims owned by others?

- Bottom-50 share of net personal wealth
- Top-10 wealth share
- Share with zero/negative net wealth
- Household debt-to-income / debt-service burden
- Emergency-expense resilience

**Global distribution source:** WID wealth series where available:
- `shweal992j`, `p0p50`: bottom-50 net-personal-wealth share
- `shweal992j`, `p90p100`: top-10 wealth share

Wealth data should always carry a data-quality warning: it is thinner, more modeled, and more sensitive to valuation and tax-haven assumptions than income data.

## Scoring approach

- Publish the raw indicators and trends first.
- Score each module only against transparent, meaningful anchors — not merely “best country in the sample.”
- Use a minimum-condition penalty or geometric mean for any optional overall score, so high aggregate income cannot wash away food insecurity, housing failure, or worker repression.
- Keep a separate data-confidence grade. A modeled global estimate is not equivalent to a representative household survey or payroll record.
- Do not publish a national overall score unless its core modules are sufficiently covered.

## Implementation sequence

1. Freeze v2 formulas after the current scaling correction; do not keep tuning aggregate thresholds.
2. Add a non-scoring **v3 research panel** for the United States first:
   - bottom-50/top-10 income and wealth shares
   - labor share
   - median/low-wage earnings trend
   - housing, debt, and basic-cost evidence
3. Build a WID ingestion proof of concept for bottom-50 and top-10 income/wealth shares, retaining WID definitions and source year per country.
4. Add ILO labor-share and labor-underutilization proof-of-concept ingestion.
5. Build country dossiers with stronger national sources before claiming universal affordability or worker-power rankings.
6. Only after inspecting coverage and behavior should we choose v3 headline labels and any composite scoring formula.

## What v3 must not claim

- GDP/GNI per capita is not typical income.
- Average wages are not typical pay.
- Employment alone is not labor leverage.
- Debt/GDP is not household debt distress.
- Legal rights on paper are not worker power.
- A single international score cannot prove how every ordinary person in a country lives.
