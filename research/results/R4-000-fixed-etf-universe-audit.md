# R4-000 — Fixed-ETF Universe Eligibility and Data-quality Audit

## Status

`ACCEPT — UNIVERSE/DATA AUDIT PASSED; PERFORMANCE NOT RUN`

R4-000 only determines an immutable ETF universe. It does not calculate momentum
signals, portfolio returns, benchmark returns or any other strategy-performance result.

## Frozen Setup

- Candidate roster: `research/R4_CANDIDATES.csv`, frozen before price inspection
- Inception cutoff: before 2010-01-01
- Audit request: 2013-01-01 through 2014-06-30 inclusive
- Liquidity: 2013 median daily `raw close * volume`, minimum USD 5 million
- Coverage: at least 95% of the SPY trading calendar in both 2013 and 2014 H1
- Selection: maximum qualifying median dollar volume per category
- Tie-break: earlier inception, then alphabetical ticker
- Freeze date: 2014-06-30
- Data source: Yahoo Finance through yfinance 1.7.0

Raw close is used only for contemporaneous dollar-volume measurement. Adjusted OHLC is
stored separately for possible later research; no performance calculation used it here.

## Frozen Selection

| Category | ETF | 2013 median daily dollar volume | 2013 coverage | 2014 H1 coverage |
|---|---:|---:|---:|---:|
| U.S. broad equity | SPY | $18,446.15M | 100% | 100% |
| Developed ex-U.S. equity | EFA | $1,007.10M | 100% | 100% |
| Emerging-market equity | EEM | $2,372.14M | 100% | 100% |
| U.S. intermediate Treasury | IEF | $76.60M | 100% | 100% |
| U.S. long Treasury | TLT | $826.13M | 100% | 100% |
| U.S. investment-grade corporate bond | LQD | $221.54M | 100% | 100% |
| U.S. listed real estate | IYR | $599.11M | 100% | 100% |
| Gold | GLD | $1,211.81M | 100% | 100% |
| Broad commodities | DBC | $45.64M | 100% | 100% |

No category required a tie-break.

## Candidate Audit Summary

- Candidates: 31
- Valid Yahoo price frames: 30
- Explicit data failures: 1 (`TLO`; no historical payload returned)
- Candidates passing all eligibility, liquidity and coverage rules: 24
- Categories with at least one eligible candidate: 9/9
- Selected representatives: 9
- Manifest hash mismatches: 0
- Rows on or after 2023-01-01: 0
- Strategy or benchmark performance runs: 0

Candidates below the USD 5M threshold remain in the audit as ineligible; they were not
silently dropped. TLO likewise remains an explicit failure rather than being inferred to
be delisted or removed from the pre-registered roster.

## Integrity and Limitations

- The local immutable snapshot is `r4_000_fixed_etf_audit_v1`; downloaded snapshot files
  are intentionally git-ignored, while protocol, code and aggregate evidence are tracked.
- The issuer-family candidate roster is a practical closed roster, not a complete
  historical census of every ETF listed before 2010. R4 therefore supports a predefined
  asset-level robustness study, not a claim of exhaustive ETF-universe selection.
- Yahoo data is free research data and is not institutional-grade. The audit demonstrates
  completeness for the selected pre-freeze interval, not future availability guarantees.
- R4 is not stock-level PIT replication and does not repair the R3 data limitation.

## Decision

R4-000 is `ACCEPT` for universe construction and data feasibility. The frozen universe is
`SPY, EFA, EEM, IEF, TLT, LQD, IYR, GLD, DBC`.

R4-001 is technically eligible for a separate authorization decision. It has not been
authorized or run. Frozen R1-002 parameters and the Final OOS 2023–2025 seal remain intact.
