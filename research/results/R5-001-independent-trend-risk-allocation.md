# R5-001 — Independent Trend with Risk-based Allocation

## Verdict

`ACCEPT — DEVELOPMENT EVIDENCE ONLY; NOT A FINAL CANDIDATE`

Option A의 단일 canonical ETF adaptation을 2007-03-01–2014-12-31에서 실행했다.
R5-001 이전에 signal, allocation, 비용과 판정 기준을 고정했으며 parameter search는 없다.

## Frozen Setup

- Universe: SPY/EFA/EEM/IEF/TLT/LQD/IYR/GLD/DBC
- Signal: trailing 12-calendar-month adjusted return > 0
- Allocation: active assets inverse EWMA volatility; decay 60/61; weights sum to 100%
- Inactive allocation: cash, return 0%
- Rebalance: month-end close signal, next trading-day open execution
- Short/leverage/portfolio volatility target: none
- Primary cost: 10bps one-way; robustness 0/5/10/20bps
- Data: local immutable Yahoo/yfinance 1.7.0 snapshot, 2006-02-03–2014-12-31
- Final OOS 2023–2025: SEALED

## Data Gate

- Symbols: 9/9
- Minimum common-SPY-calendar coverage: 99.9554%
- Latest row: 2014-12-31
- Final OOS downloaded: false
- Manifest/hash validation: passed

An initial validator incorrectly required DBC data on its issuer inception date. DBC's first
Yahoo row is the next trading day, 2006-02-06. The validator was corrected to the actual
pre-registered requirement—at least 95% coverage and a full warm-up before 2007-03-01—before
strategy performance was run.

## Results

| Strategy, 10bps | Total return | CAGR | Volatility | MDD | Sharpe | Sortino | Calmar | Turnover |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Candidate | 72.29% | 7.19% | 8.04% | -12.66% | 0.905 | 1.254 | 0.568 | 21.90x |
| Inverse volatility, no trend | 55.23% | 5.77% | 8.01% | -22.01% | 0.742 | 1.007 | 0.262 | 5.32x |
| Equal-weight trend | 78.32% | 7.66% | 10.38% | -18.79% | 0.762 | 1.061 | 0.408 | 24.86x |
| Equal-weight buy-and-hold | 42.72% | 4.64% | 11.59% | -32.32% | 0.447 | 0.589 | 0.144 | — |
| SPY buy-and-hold | 74.22% | 7.34% | 22.34% | -55.19% | 0.424 | 0.525 | 0.133 | — |

The candidate did not beat SPY CAGR, but it materially reduced volatility and drawdown and
improved risk-adjusted metrics. Equal-weight trend earned more total return, while the
inverse-volatility overlay improved Sharpe, Calmar and MDD.

## Cost Robustness

| One-way cost | Total return | CAGR | Sharpe | Calmar | MDD |
|---:|---:|---:|---:|---:|---:|
| 0bps | 76.12% | 7.49% | 0.937 | 0.595 | -12.59% |
| 5bps | 74.19% | 7.34% | 0.921 | 0.582 | -12.62% |
| 10bps | 72.29% | 7.19% | 0.905 | 0.568 | -12.66% |
| 20bps | 68.54% | 6.89% | 0.872 | 0.542 | -12.72% |

## Dependency Diagnostics

- Positive two-year blocks: 4/4
- Block returns: 19.95%, 12.32%, 14.73%, 12.30%
- Maximum positive block contribution share: 27.33%
- Maximum single-asset absolute P&L contribution: 19.22% (SPY)
- Trades at 10bps: 638
- Attribution reconciliation error: approximately -2.6e-11

All pre-registered R5-001 checks passed: Sharpe/Calmar/CAGR improvement over no-trend
inverse volatility, MDD preservation versus equal-weight trend, period/name diversification
and 20bps robustness.

## Interpretation

This is a development ACCEPT, not final validation. The result supports the narrow claim
that independent trend added risk-adjusted value over pure inverse-volatility in this period,
and risk weighting improved drawdown versus equal-weight trend. It does not prove a universal
trend premium or authorize paper/live trading.

Important limitations:

- The 2007–2014 sample is short and contains the Global Financial Crisis.
- The researcher knew broad historical events even though these strategy returns had not been inspected.
- ETFs are long/cash total-return proxies, not the futures long/short portfolios in the literature.
- Cash return is fixed at zero; taxes, spread beyond fixed bps, FX and market impact are omitted.
- The nine-ETF universe is pre-frozen but not a complete global opportunity set.
- 2015–2022 remains researcher-contaminated and cannot be labelled clean OOS.

## Next Step

Proceed only to R5-002's already bounded cost/subperiod robustness and implementation
sensitivity checks. Do not open Final OOS or search adjacent parameters.
