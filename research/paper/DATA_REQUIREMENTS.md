# Data Requirements and Source Feasibility

## Minimum Publication Dataset

- Broad, stable multi-asset universe: equity indexes, government bonds/rates, currencies and commodities.
- Daily settlement or total-return data sufficient for monthly signals and ex-ante volatility.
- At least 25–30 years; preferably 40+ years and enough independent contracts per asset class.
- Point-in-time contract metadata, expiry, multiplier, currency and trading calendar.
- Reproducible continuous-futures construction or raw contracts with frozen roll rules.
- Risk-free/financing returns, FX conversion, transaction-cost proxies and benchmark factors.
- No observations from the sealed 2023–2025 project Final OOS unless separately authorized.

## Source Candidates

| Source | Access | Coverage/history | Main risks | Publication suitability |
|---|---|---|---|---|
| CME DataMine | Paid; possible institutional purchase | Official CME futures; products back to 1972 depending dataset | CME-only breadth; license; roll construction | High for covered contracts |
| LSEG Datastream / Workspace | University/institutional candidate | International futures, indexes, FX and total-return series | Entitlement and opaque continuous-series conventions | Medium-high after metadata audit |
| Bloomberg | University/institutional candidate | Broad futures and indexes | License, reproducibility and field conventions | Medium-high with archived query manifest |
| WRDS vendor datasets | University/institutional candidate | Subscription-dependent; CRSP excellent for equities | Futures access varies by institution | High for entitled datasets |
| CRSP via WRDS | University/institutional | Research-grade US securities/indices | Not a global futures solution | High for equity controls only |
| Kenneth French Data Library | Free | Long factor and momentum portfolios | Cross-sectional equity factors, not tradable futures | High for controls/benchmarks |
| Exchange public files | Mixed/free fragments | Official but inconsistent depth | Multiple formats and missing old contracts | Medium as verification source |
| Yahoo/Stooq ETFs | Free | Accessible adjusted ETF histories | Short history, vendor adjustments, survivorship/domain gap | Tier C pilot only |

## Feasibility Verdict

- Free data: sufficient for code pilots and a narrow Tier C ETF study, not for a credible global
  futures claim about Candidate 1.
- University data: potentially sufficient for Tier B, but access to Datastream/Bloomberg/WRDS and
  export/reproducibility rights must be confirmed by the user or institution.
- Institutional futures: preferred. Actual access is unknown and is not assumed.
