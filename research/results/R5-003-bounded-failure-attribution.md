# R5-003 — Bounded Failure Attribution

## Status

`COMPLETE — DESCRIPTIVE EVIDENCE OF SIGNAL AND ALLOCATION INSTABILITY`

R5-001/002의 frozen signal, allocation, universe, timing과 비용을 변경하지 않고 두 기간의
차이를 한 번 분해했다. 이 분석은 인과 추론이나 strategy rescue가 아니다.

## Trend Signal Effectiveness

| Diagnostic | 2007–2014 | 2015–2022 |
|---|---:|---:|
| Asset-month observations | 837 | 855 |
| Positive-signal next-month mean payoff | 0.646% | 0.305% |
| Negative-signal next-month mean asset payoff | 0.235% | 0.576% |
| Positive-signal hit rate | 58.33% | 56.42% |
| Negative-signal hit rate | 44.73% | 44.00% |
| Overall directional hit rate | 54.48% | 51.70% |
| Signal persistence | 90.58% | 89.36% |

Positive-trend continuation weakened by roughly half. More importantly, negative-signal
assets rose rather than fell in both periods, and their missed subsequent payoff was much
larger in 2015–2022. The long/cash rule therefore gave up more rebound return in the later
period.

## Risk Allocation

| Incremental comparison | 2007–2014 | 2015–2022 |
|---|---:|---:|
| Candidate minus no-trend inverse-vol total return | +17.06%p | -25.98%p |
| Candidate minus no-trend inverse-vol Sharpe | +0.163 | -0.366 |
| Candidate minus equal-weight trend total return | -6.03%p | -7.93%p |
| Candidate minus equal-weight trend Sharpe | +0.143 | -0.094 |

The trend overlay added value over pure inverse volatility early and destroyed value later.
Inverse-volatility weighting improved the risk-adjusted equal-weight trend result early but
also changed sign later. Both signal and allocation effects are temporally unstable.

## Turnover and Whipsaw

| Diagnostic | 2007–2014 | 2015–2022 |
|---|---:|---:|
| Signal transitions | 78 | 90 |
| False entry/exit transitions | 42 | 43 |
| False-transition rate | 53.85% | 47.78% |
| Turnover at 10bps | 21.90x | 30.16x |
| Trades | 638 | 565 |

The later period had more transitions and turnover, but a lower false-transition rate. A
simple increase in whipsaw frequency is therefore not the primary explanation. The result is
more consistent with weaker payoff conditional on signal, particularly missed rebounds after
negative signals.

## Asset Contribution

| Group net P&L | 2007–2014 | 2015–2022 |
|---|---:|---:|
| Equity | +$17,813 | -$3,330 |
| Bonds and credit | +$36,976 | +$12,332 |
| Real assets | +$17,498 | -$9,868 |

- Early maximum asset absolute contribution: 19.22% (SPY).
- Late maximum asset absolute contribution: 33.55% (IYR, negative).
- The later failure was not a single-asset event, although IYR was the largest loss source.
- Bonds/credit remained positive; equity and real assets changed from positive to negative.

## Period and Crisis Contribution

- 2007–2014: all four two-year blocks were positive. The NBER GFC recession window
  contributed about +$2,793 versus +$69,494 outside that window. Early success was therefore
  not mechanically concentrated in the recession window.
- 2015–2022: only 2019–2020 was positive. The NBER COVID recession window contributed
  approximately -$4,215 versus +$3,349 outside it. The rapid crash/rebound interval hurt this
  long/cash implementation rather than providing crisis alpha.

The NBER windows are descriptive calendar classifications, not causal regime instruments.

## Cost Contribution

- Early 0-to-10bps total-return drag: 3.83%p; 10bps slippage dollars approximately $2,920.
- Late 0-to-10bps total-return drag: 3.11%p; 10bps slippage dollars approximately $3,184.
- Costs turned a weak late gross result (+2.24%) into a negative net result (-0.87%), but the
  candidate already lagged structural baselines before costs. Cost is an amplifier, not the
  root cause.

## Main Explanation

`DIRECTIONAL PAYOFF DETERIORATION + ALLOCATION EFFECT REVERSAL`, amplified by costs.

Confidence is `MODERATE` for descriptive attribution and `LOW` for causality. The sample has
only nine ETFs and two eight-year periods, 2015–2022 is researcher-contaminated, cash earns
zero, and ETF long/cash differs materially from futures long/short TSMOM.

## Stop Rule

R5-003 is complete. No lookback, volatility window, rebalance, regime filter, leverage,
universe or cost parameter is changed. R5 ends without a final trading candidate and Final
OOS remains SEALED.
