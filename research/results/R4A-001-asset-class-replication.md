# R4A-001 — Frozen Asset-class ETF Replication

## Verdict

`REJECT`

The frozen R1-002 strategy was applied without parameter changes to
SPY/EFA/EEM/IEF/TLT/LQD/IYR/GLD/DBC. Final OOS 2023–2025 remained sealed.

## Data Gate

- Snapshot: `r4a_development_2014_2022_v1`
- Source: Yahoo Finance via yfinance 1.7.0
- Request: 2014-07-01 inclusive, 2023-01-01 exclusive
- Common dates: 2,142; last date 2022-12-30
- Final OOS rows: 0
- Warm-up: exactly 126 pre-2015 common rows; evaluation begins in 2015

An initial diagnostic run incorrectly discarded the pre-2015 warm-up. It was discarded
before interpretation, the timing boundary was corrected and tested, and only the
registered warm-up run below is a research result.

## Performance

| Cost | Return | CAGR | Volatility | MDD | Sharpe | Sortino | Calmar | Turnover | Trades |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0bps | 40.13% | 4.31% | 17.39% | -25.79% | 0.330 | 0.398 | 0.167 | 214.11x | 227 |
| 5bps | 25.11% | 2.84% | 17.38% | -27.48% | 0.249 | 0.300 | 0.103 | 216.02x | 227 |
| 10bps | 11.68% | 1.39% | 17.39% | -31.05% | 0.167 | 0.201 | 0.045 | 217.91x | 227 |
| 20bps | -10.99% | -1.45% | 17.42% | -42.84% | 0.004 | 0.005 | -0.034 | 221.64x | 227 |

At 10bps, SPY returned 115.50% with Sharpe 0.610 and Calmar 0.299. Frozen-universe
equal-weight returned 33.37% with Sharpe 0.420 and Calmar 0.164.

## Generalization Diagnostics — 10bps

- Maximum single-ETF absolute realized-P&L share: 26.62% (`EEM`)
- ETFs with realized exits: 8/9; LQD had no realized exit
- Positive non-equity realized P&L: yes (IEF, GLD and DBC)
- Positive blocks: 2/4
  - 2015–2016: -13.44%
  - 2017–2018: +4.79%
  - 2019–2020: -0.17%
  - 2021–2022: +21.73%
- Rebalance signals: 403; risk-off signals: 29
- Most holding days: DBC 445, EEM 375, IYR 305

## Decision

The strategy passed the concentration-diversification diagnostics but failed the mandatory
return and risk-adjusted comparisons. Only two blocks were positive and cost robustness
was weak. Under the pre-registered rule this is `REJECT`, not `INCONCLUSIVE`.

The result does not justify parameter tuning, changing the frozen ETF universe, opening
Final OOS, or moving toward paper/live trading.
