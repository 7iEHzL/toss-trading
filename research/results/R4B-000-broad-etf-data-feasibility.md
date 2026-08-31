# R4B-000 — Broad ETF Data Feasibility

## Verdict

`CONDITIONAL — DATA EXISTS, ACCESS NOT VERIFIED`

R4B requires a 2014-06-30 historical ETF master including later liquidations and mergers.
A current-survivor screen is not an acceptable substitute.

## Source Review

### CRSP Survivor-Bias-Free U.S. Mutual Fund Database

Official documentation describes active and inactive funds, an ETF/ETN flag, historical
fund headers, dead-fund and delisting-reason fields, and acquiring-fund identifiers for
mergers. This is structurally suitable for the R4B-000 master/identity gate.

- Product: https://www.crsp.org/research-data-products/crsp-survivor-bias-free-us-mutual-fund-database/
- Guide: https://www.crsp.org/crsp_pdf/crsp-survivor-bias-free-us-mutual-fund-database-guide-crspsift/
- Access status: subscription required; no project license or sample rows verified

### Nasdaq Trader

The public symbol directory is described as current-day data. Nasdaq Daily List provides
historical listing, delisting, name and symbol events, but is only a corporate-action
component. It does not by itself establish a complete historical ETF master, exposure
taxonomy, adjusted next-open prices and liquidation proceeds.

- Current directory: https://www.nasdaqtrader.com/Trader.aspx?id=symbollookup
- Daily List description: https://www.nasdaqtrader.com/Trader.aspx?id=DailyListPD

## Decision

R4B-001 remains `NOT AUTHORIZED`. A licensed CRSP-equivalent source must first pass
row-level sample checks for 2014 membership, stable identity, exposure deduplication,
inactive funds, adjusted OHLC and terminal treatment. Current surviving ETFs plus Yahoo
would repeat the survivorship and missing-security problem identified in R3.

No performance, parameter search or Final OOS access occurred in R4B-000.

## Free-data-only Follow-up

The user selected a free-data-only constraint. The final audit considered official SEC
EDGAR archives/submissions and Nasdaq exchange event data.

- SEC EDGAR APIs and archives are free and include filing histories and former-name
  metadata, but they do not expose a complete point-in-time 2014 ETF master joined to
  exchange ticker validity, exposure identity, adjusted OHLC and liquidation proceeds.
- Structured N-CEN/N-PORT datasets start too late to establish the 2014 freeze universe.
- Nasdaq Daily List has historical listing/delisting and symbol events but is a monthly
  subscription product, not a free source.
- A reconstruction from current symbols, Yahoo and manually collected issuer filings would
  have no known denominator for missing inactive ETFs and would fail the mapping and
  reproducibility gates.

Final verdict: `R4B CLOSED — BLOCKED BY FREE-DATA COVERAGE`. R4B-001 is permanently
`NOT AUTHORIZED` under this free-data protocol. It may be reopened only through a new
licensed historical-data decision.
