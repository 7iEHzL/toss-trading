# R5-002 — Frozen-rule Contaminated Period Stress

## Verdict

`REJECT — STRONG PERIOD INSTABILITY; SECOND OPINION REQUIRED`

R5-001에서 고정한 규칙을 한 글자도 조정하지 않고 2015–2022에 적용했다. 이 기간은
R1–R4에서 반복 관찰됐으므로 clean OOS가 아니며, 결과는 `RESEARCHER_CONTAMINATED_STRESS_DIAGNOSTIC`
으로만 해석한다. Final OOS 2023–2025는 접근하지 않았다.

## Frozen Setup

- Same nine ETFs, 12-month sign, EWMA decay 60/61, inverse-volatility allocation
- Month-end close signal, next-open execution
- Long/cash, unlevered; 0/5/10/20bps
- Evaluation: 2015-01-01–2022-12-31 with pre-2015 warm-up
- Parameter changes/search: 0

## Results

| Strategy, 10bps | Total return | CAGR | Volatility | MDD | Sharpe | Sortino | Calmar | Turnover |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Candidate | -0.87% | -0.11% | 10.00% | -22.10% | 0.037 | 0.043 | -0.005 | 30.16x |
| Inverse volatility, no trend | 25.11% | 2.84% | 7.69% | -21.02% | 0.403 | 0.490 | 0.135 | 5.42x |
| Equal-weight trend | 7.07% | 0.86% | 11.01% | -21.84% | 0.131 | 0.153 | 0.039 | 31.68x |
| Equal-weight buy-and-hold | 34.12% | 3.74% | 9.83% | -20.97% | 0.422 | 0.513 | 0.178 | — |
| SPY buy-and-hold | 114.51% | 10.02% | 18.63% | -33.72% | 0.610 | 0.730 | 0.297 | — |

## Cost and Period Diagnostics

- Candidate return: 0bps +2.24%, 5bps +0.70%, 10bps -0.87%, 20bps -3.85%.
- Positive two-year blocks: 1/4.
- Block returns: -0.51%, -5.16%, +18.61%, -10.59%.
- Maximum positive block contribution share: 100%.
- Maximum asset absolute P&L contribution: 33.55% (IYR, negative).
- Attribution reconciliation error: approximately 3.5e-11.

## Interpretation

The frozen trend overlay did not add value in the later known period. It reduced performance
relative to pure inverse volatility and equal-weight trend, incurred much higher turnover than
pure risk allocation, and depended entirely on the 2019–2020 positive block. This directly
conflicts with R5-001's broad positive 2007–2014 evidence.

Because 2015–2022 is researcher-contaminated, this is not formal clean OOS rejection. It is
nevertheless strong enough to prevent promotion, parameter search, R5-003 attribution or
Final OOS use without a high-impact second opinion.
