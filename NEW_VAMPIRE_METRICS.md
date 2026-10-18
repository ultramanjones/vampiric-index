# New Vampire Metrics

**Status:** research and design proposal — not yet a replacement scoring formula.

## What this index is actually trying to detect

The project should not primarily ask whether a country is rich, orderly, healthy, or nominally free.

It should ask whether ordinary households can still keep the **production → wages → survival → spending → business revenue → jobs** loop alive.

A circulation failure begins when output, profit, rent, debt payments, fees, and asset appreciation rise while ordinary people’s usable income does not. Households then cut non-essential spending, bridge essentials with debt, run down savings, take extra work, or move in with family/roommates. Businesses lose demand and respond with closures, layoffs, price hikes, automation, or further extraction. Those responses reduce household capacity again.

This is not exclusive to capitalism in the narrow ideological sense. The same question applies wherever a system extracts too much from households and weakens their ability to live, choose work, and participate in the economy.

## The cycle we need to show

```text
Production and productivity
        ↓
Pay reaches ordinary households
        ↓
Households cover housing, food, energy, healthcare, transport, and debt
        ↓
Money left after essentials: savings, stability, and ordinary consumption
        ↓
Demand reaches local businesses and employers
        ↓
Revenue supports jobs and production
        ↓
(back to wages and household capacity)
```

### The extraction failure loop

```text
More income captured by profits, rents, interest, fees, and asset holders
        ↓
Less usable household income after essentials
        ↓
Debt, arrears, multiple jobs, depleted savings, lower discretionary spending
        ↓
Weaker consumer demand and local business revenue
        ↓
Layoffs, closures, price hikes, automation, and more labor pressure
        ↓
Even less usable household income
```

A future interactive circle can make each node clickable. Every metric page should answer:

1. **Where is this in the cycle?**
2. **What does a rise or fall mean?**
3. **What does it affect next?**
4. **What does it not prove by itself?**
5. **What source and year are we looking at?**

## Why the current four pillars are not sufficient

Current v1 inputs are:

| Current label | Actual current proxy | Why it is not the main circulation measure |
|---|---|---|
| Survival floor | Life expectancy | Important outcome, but cannot show whether rent, debt, and essential bills are swallowing wages now. |
| Sovereign cannibalization | GNI per capita | The label does not describe the measure. GNI per capita measures average national income, not sovereign extraction or household cannibalization. It can be high while housing and debt make life impossible. |
| Labor retention | Employment-to-population ratio | Shows whether people are formally working, not whether pay supports life or whether one job is enough. A high ratio can coexist with two-job dependence and poverty pay. |
| State coercion | Freedom House score | Useful as a broad rights/institutions context measure, but it is not a calibrated 0–25 measure of day-to-day police violence, labor repression, or “how close to civil war” a country is. |

**Important:** the current HVI should remain visibly labeled **legacy / coverage-input v1** until it is deliberately rebuilt. It must not quietly claim to measure the new circulation model.

## Proposed replacement structure: the Household Circulation Index

The eventual main score should be called something ordinary people can understand, such as:

# Can People Still Make It?

Technical subtitle:

> **Household Circulation and Extraction Index**

Do not finalize the public name until we discuss it. The essential point is that the dashboard leads with a question, not jargon.

The score should be made of five linked modules. Each module receives a plain-English name, a short label, a direction, and a source note.

| Module | Plain-English question | Position in the cycle | What a bad result means |
|---|---|---|---|
| **1. Pay That Reaches People** | Is ordinary work keeping up with prices and productivity? | Wages entering households | Pay is weak, falling in real terms, or losing ground to the share captured above it. |
| **2. Cost of Staying Alive** | After a paycheck, can people cover housing and essentials? | Survival pressure | Housing and essential costs absorb too much income. |
| **3. Breathing Room or Debt** | Do households have savings and room to absorb a shock, or are they borrowing to survive? | Household buffer | Savings are weak/falling, debt service or arrears rise, and households have no exit room. |
| **4. Ability to Say No** | Can a person leave a bad job, reduce hours, or change work without immediate ruin? | Labor bargaining power | Multiple-job dependence, underemployment, loss of benefits, and weak supports turn employment into coercion. |
| **5. Demand Still Alive** | After essentials and debt, are households still able to spend enough to sustain ordinary business activity? | Consumer demand / feedback | Real per-person household consumption stalls or falls; consumer confidence and retail volume weaken. |

### Context panel, not part of the first circulation score

| Context measure | Plain-English question | Why it remains separate |
|---|---|---|
| **Rights and Repression Context** | Can people organize, protest, report abuse, and resist the system without state retaliation? | It changes the consequences and political exit routes, but it should not disguise itself as an exact “coercion intensity” scale. |
| **State Capacity / Public Floor** | Do public healthcare, housing support, transit, unemployment support, and utilities reduce household dependence on employers and landlords? | This helps explain why two countries with similar wages can have very different ability to survive. |

This solves the current naming problem:

- “Sovereign cannibalization” is retired. It does not say what is measured.
- “Labor retention” becomes **Ability to Say No** only after it is rebuilt around real labor precarity rather than employment alone.
- “State coercion” becomes a clearly labeled context/risk module until data supports a more specific labor-rights and repression measure.
- “Survival” remains, but becomes **Cost of Staying Alive**, tied to actual household pressure.

## Minimum viable metric set

We should begin with a small, sourced set that can be explained to a normal visitor. Do not create a fake-precise mega-score from whatever happens to be available.

### 1. Pay That Reaches People

| Candidate indicator | What it tells us | Best source path | Use / caution |
|---|---|---|---|
| Real household disposable-income growth, preferably per capita | Whether household purchasing power is actually rising or falling after taxes/transfers and inflation | OECD Quarterly National Accounts / Economic Outlook for participating economies | Prefer rolling 3- or 5-year cumulative movement over one quarter. Keep household vs. household+NPISH definition visible. |
| Labor income share of GDP | Whether national output is reaching workers rather than capital owners | ILOSTAT / OECD / national accounts depending on coverage | A share is not a wage level; it can rise during recession. Use with income and employment measures. |
| Real wage growth versus CPI | Whether wages are keeping up with prices | ILOSTAT/OECD for higher-coverage module; national sources as documented extensions | Do not compare series with different worker populations as if identical. |

### 2. Cost of Staying Alive

| Candidate indicator | What it tells us | Best source path | Use / caution |
|---|---|---|---|
| Housing-cost overburden: share spending more than 40% of disposable income on housing | Direct evidence that shelter consumes an unsustainable share of income | Eurostat EU-SILC `ilc_lvho01` for Europe; OECD Affordable Housing Database HC1.2 where available | Strong for Europe. OECD years are uneven; preserve source year rather than pretending it is live annual data. |
| House-price-to-income movement | Whether purchase access is getting worse relative to income | OECD Housing Prices or IMF Global Housing Watch | Usually an index relative to a base year, not “years of income to buy a house.” It does not replace rent burden. |
| Essential-cost pressure | Whether food, energy, transport, and medical essentials are outpacing household income | Regional/national expansion after core build | No clean global harmonized basket. Better to add carefully by region than invent a false global number. |

### 3. Breathing Room or Debt

| Candidate indicator | What it tells us | Best source path | Use / caution |
|---|---|---|---|
| Household saving rate | Whether households retain a buffer after spending | OECD quarterly/annual household accounts; Eurostat for Europe | High saving is not automatically good: it can reflect fear, inequality, or forced retrenchment. A rapid fall is often more useful than the level. |
| Household debt-service ratio | Share of income consumed by required interest and principal payments | BIS Debt Service Ratios | Best direct repayment-pressure series, but only covers a limited set of countries. |
| Household debt / household credit | Leverage accumulated by households | IMF Global Debt Database; BIS credit to households | Debt stock is not the same as repayment burden. Use as a supplement to debt service. |
| Household arrears | Whether people are behind on rent/mortgage, utilities, or loans | Eurostat EU-SILC for Europe | Direct hardship signal, but not global. Do not silently substitute banking-system NPLs for household arrears. |

### 4. Ability to Say No

| Candidate indicator | What it tells us | Best source path | Use / caution |
|---|---|---|---|
| Time-related underemployment | People who have work but need more hours/income | ILOSTAT | Better than unemployment alone for unstable labor markets; definitions/coverage must be inspected. |
| Multiple-jobholding | Whether one job is no longer enough | OECD/Eurostat/ILO where available | Country coverage and definitions are patchy. This should begin as a high-quality regional module, not a made-up global estimate. |
| Employment-to-population | Broad access to paid work | ILO modeled estimates / WDI | Retain only as context. It is not proof of adequate pay or security. |
| Collective-bargaining coverage / union density | Ability to negotiate rather than accept whatever is offered | OECD/ILO | Institutionally important, but it measures potential power, not realized household affordability. |

### 5. Demand Still Alive

| Candidate indicator | What it tells us | Best source path | Use / caution |
|---|---|---|---|
| Real household final consumption per capita | Whether household purchasing capacity is expanding or being squeezed | World Bank WDI `NE.CON.PRVT.KD` divided by population `SP.POP.TOTL`; OECD national accounts for higher-frequency member-country data | Use multi-year real per-person change, not constant-dollar levels as an international standard of living rank. WDI includes households and NPISH. |
| Retail-sales volume / consumer confidence | Timely warning of weakening household demand | OECD monthly indicators; European Commission surveys; selected national/World Bank GEM data | Useful early-warning layer, not a globally uniform score. Confidence is sentiment, not household welfare. |
| Corporate profit margins versus labor share | Whether businesses are capturing more while wages/households lose ground | OECD/ILO/national accounts, later phase | This is conceptually central but needs careful sector definitions. Begin with labor share as the consistent side; add profit-margin measures only where source definitions match. |

## How the modules must be interconnected

The scoring should not treat every metric as an unrelated pill on a dashboard.

| Causal link | Evidence pair to show | Example visitor explanation |
|---|---|---|
| Pay → Survival | Real disposable income vs. housing-cost overburden | “Pay rose 2%, but the share of households spending over 40% of income on housing rose.” |
| Survival → Debt | Housing/essential pressure vs. saving rate, debt service, or arrears | “As core costs rose, household buffers weakened and required debt payments consumed more income.” |
| Debt → Labor dependence | Debt/arrears vs. underemployment or multiple jobholding | “Households with no buffer are less able to refuse bad work or absorb lost hours.” |
| Labor dependence → Demand | Precarity vs. real household consumption per person | “More people were working, but household demand per person stalled.” |
| Demand → Business strain | Consumption/retail volume vs. closures, layoffs, or business stress | “Demand weakening creates the conditions for revenue stress, closure, and more job cuts.” |
| Extraction → the whole loop | Labor share vs. household income, housing/debt, and consumption | “A growing share of output did not become usable household income, weakening the customer base.” |

The site should use the phrase **“consistent with pressure in the loop”**, not claim it has proven a simple one-way cause from a single country observation.

## Scoring rules to avoid fake precision

1. **Score deterioration as well as levels.** A country can look wealthy in level terms while household conditions are rapidly breaking down.
2. **Do not award high marks merely because people are employed.** One-job sufficiency matters more than raw labor-force attachment.
3. **Do not let national income conceal housing pressure.** Australia is the obvious current warning case: high income and formal employment can coexist with severe housing stress.
4. **Do not turn a rights score into a fictional police-violence meter.** Keep political rights/repression transparent and separate unless a defensible, directly relevant source is added.
5. **No imputed country values.** If a country lacks comparable household debt-service or multiple-job data, label the module “not yet comparable.” Do not fill blanks with guesswork.
6. **Preserve source year and definition.** A 2022 housing survey and a 2025 wage estimate must not be displayed as though they were one synchronized observation.
7. **Use source tiers.**
   - **Global annual core:** World Bank / ILO / IMF data with broad coverage.
   - **Higher-resolution module:** OECD / BIS / Eurostat, clearly marked as narrower coverage.
   - **Country dossier:** official national data, added only with a definition note.
8. **Show the raw figure beside the score.** A score without its data and transformation is not trustworthy.
9. **No overall grade until the weighting is discussed.** The first artifact should be a transparent dashboard of the cycle, not a black-box 0–100 ranking.

## Verified source map

| Need | Source | URL / API | Coverage note |
|---|---|---|---|
| Global real household consumption | World Bank WDI: household and NPISH final consumption, constant US$ `NE.CON.PRVT.KD` | https://api.worldbank.org/v2/country/all/indicator/NE.CON.PRVT.KD?format=json&per_page=20000 | Broad annual coverage; divide by WDI population `SP.POP.TOTL` for per-person trend. |
| Population | World Bank WDI `SP.POP.TOTL` | https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL?format=json&per_page=20000 | Required for consumption-per-person calculation. |
| Global household-debt stock | IMF Global Debt Database | https://www.imf.org/external/datamapper/datasets/GDD | Annual; household detail has uneven coverage. |
| Direct debt-payment pressure | BIS Debt Service Ratios | https://www.bis.org/statistics/dsr.htm | Quarterly but only a limited set of economies. |
| Household-credit stock | BIS credit to non-financial sector | https://www.bis.org/statistics/totcredit.htm | Quarterly, limited country coverage. |
| European housing hardship | Eurostat EU-SILC housing-cost overburden | https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvho01?lang=en | Annual, defined as housing costs over 40% of equivalised disposable income. |
| OECD/partner housing burden | OECD Affordable Housing Database HC1.2 | https://www.oecd.org/content/dam/oecd/en/data/insights/data-explainers/2024/06/oecd-affordable-housing-database/HC1-2-Housing-costs-over-income.xlsx | High-value direct burden data; reference years vary. |
| House-price/income pressure | OECD Housing Prices | https://www.oecd.org/en/data/indicators/housing-prices.html | Usually quarterly index data; a trend measure, not an absolute price-to-income ratio. |
| Household saving / disposable income | OECD Data Explorer / quarterly national accounts | https://data-explorer.oecd.org/ | High-quality but mostly OECD/partner coverage. |
| Underemployment, employment, labor income share | ILOSTAT | https://ilostat.ilo.org/data/ | Definitions and country coverage must be checked series-by-series. |
| Consumer confidence | OECD Consumer Confidence Index | https://www.oecd.org/en/data/indicators/consumer-confidence-index-cci.html | Monthly early warning for covered economies, not a global welfare measure. |

## First build sequence — deliberately small

1. Keep the legacy HVI online, but label it as **v1 / not yet the Household Circulation model**.
2. Create a new country-data schema that stores raw values, source URL, source year, frequency, definition, and coverage status before any score.
3. Build the first global chart: **five-year change in real household consumption per person** for every tracked country with usable WDI data.
4. Add the first direct-pressure pairing where sources are available: **housing burden + real disposable income**.
5. Add **household savings + debt-service** for BIS/OECD coverage, visibly marked as a higher-resolution module.
6. Add **underemployment and multiple-jobholding** only once sources/definitions are verified for the relevant countries.
7. Create the clickable cycle graphic only after every node has at least one raw sourced indicator and plain-language explanation.
8. Discuss weighting and whether a single score is even desirable after the first raw-data dashboard exposes the actual patterns.

## Open questions for later discussion

- Is the public title **Can People Still Make It?** too broad, or is it the right human-first entry point?
- Should the dashboard rank countries at all, or should it first show each country’s deterioration/improvement through the cycle?
- What counts as an “essential” basket for cross-country comparisons, and should that remain regional rather than global?
- How much weight should be given to levels versus change over the last 3–5 years?
- Should rights/repression remain a parallel context panel rather than an overall-score pillar?
- How should the site distinguish a temporary recession from a structural extraction spiral?
