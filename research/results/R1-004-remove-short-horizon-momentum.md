# R1-004 — Remove Short-horizon Momentum Component

## Decision

`INCONCLUSIVE — DEVELOPMENT EVIDENCE CONFLICTS`

R1-002를 유지하면서 relative momentum score의 21-day 항만 제거했다. Final OOS 2023–2025는 다운로드하거나 조회하지 않았다.

## Hypothesis and Fixed Design

- Hypothesis: 21/63/126 composite에서 단기 21-day 항을 제거하면 최근 가격 움직임에 대한 민감도와 turnover 또는 concentration을 낮추면서 중기 momentum premium을 보존한다.
- Baseline: R1-002 126-day absolute-momentum risk-off.
- Single change: relative momentum weights 1/1/1 → 0/1/1.
- Unchanged: AMD/TSLA/AMZN/AAPL, Top 1, 126-day risk-off, 5거래일 rebalance, next-open execution, benchmark와 비용 조건.
- Parameter search: 없음. 다른 weight, lookback 또는 skip period를 조회하지 않음.

## Cost Robustness

| Slippage | Return | CAGR | Ann. vol | MDD | Sharpe | Sortino | Calmar | Turnover | Trades |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0bps | 8,511.66% | 81.35% | 60.07% | -64.92% | 1.284 | 1.810 | 1.253 | 117.64x | 78 |
| 5bps | 8,181.99% | 80.41% | 60.07% | -65.65% | 1.276 | 1.798 | 1.225 | 117.23x | 78 |
| 10bps | 7,865.13% | 79.47% | 60.06% | -66.36% | 1.267 | 1.786 | 1.198 | 116.82x | 78 |
| 20bps | 7,267.70% | 77.61% | 60.06% | -67.74% | 1.250 | 1.762 | 1.146 | 115.99x | 78 |

## 10bps Baseline Comparison

| Metric | R1-002 | R1-004 | Change |
|---|---:|---:|---:|
| Return | 3,910.64% | 7,865.13% | +3,954.49%p |
| CAGR | 63.75% | 79.47% | +15.72%p |
| Annual volatility | 60.42% | 60.06% | -0.36%p |
| MDD | -64.18% | -66.36% | -2.18%p |
| Sharpe | 1.111 | 1.267 | +0.156 |
| Sortino | 1.560 | 1.786 | +0.226 |
| Calmar | 0.993 | 1.198 | +0.204 |
| Turnover | 134.56x | 116.82x | -17.74x |
| Trade records | 116 | 78 | -38 |

R1-004의 10bps excess return은 SPY 대비 7,752.96%p, universe equal-weight 대비 7,056.16%p다. 전체기간 수익 및 risk-adjusted metric은 강하게 개선됐지만 MDD는 소폭 악화됐다.

## Temporal Diagnostic — 10bps

| Period | R1-002 return | R1-004 return | R1-002 MDD | R1-004 MDD | R1-002 Sharpe | R1-004 Sharpe |
|---|---:|---:|---:|---:|---:|---:|
| 2015–2016 | 384.30% | 524.84% | -40.28% | -25.16% | 1.825 | 2.096 |
| 2017–2018 | 41.29% | 118.02% | -52.60% | -48.50% | 0.600 | 1.023 |
| 2019–2020 | 1,192.14% | 1,272.35% | -60.63% | -60.63% | 2.142 | 2.177 |
| 2021–2022 | -56.48% | -59.13% | -64.18% | -66.36% | -0.672 | -0.762 |

초기 세 구간에서는 대체로 개선되지만 가장 최근 development block인 2021–2022에서는 수익률, MDD와 Sharpe가 모두 악화됐다. 이는 전체기간 결과와 방향이 충돌한다.

## Concentration Diagnostic — 10bps

아래 값은 거래원장 기반 realized-P&L 진단이며 완전한 portfolio return attribution이 아니다.

| Strategy | AMD | TSLA | AMZN | AAPL | Dominant | Max absolute realized-P&L share |
|---|---:|---:|---:|---:|---|---:|
| R1-002 | $456,952 | $4,637,149 | $104,509 | -$1,287,970 | TSLA | 71.49% |
| R1-004 | $644,531 | $9,085,291 | $360,907 | -$2,225,599 | TSLA | 73.77% |

Turnover와 거래 수는 감소했지만 single-name realized-P&L concentration은 개선되지 않았다.

## Conclusion

`INCONCLUSIVE`

전체기간 및 비용 robustness 증거만 보면 R1-004는 유망하지만, 최근 development downside와 concentration이 악화되어 사전 등록한 시간 일관성 조건과 충돌한다. 이 결과를 이용해 baseline이나 protocol을 사후 변경하지 않으며, 인접 weight/lookback을 재탐색하지 않는다. R1-002를 development candidate로 유지한다.

## Known Limitations

- Ex-post selected universe로 selection/survivorship bias 가능성이 있다.
- Yahoo/yfinance 데이터는 institutional-grade point-in-time dataset이 아니다.
- 고정 bps 비용 모델은 spread, market impact, tax와 FX를 포함하지 않는다.
- 종목별 realized P&L은 완전한 return attribution이 아니다.
- Final OOS가 봉인되어 있어 development evidence만으로 최종 전략을 정할 수 없다.
