# R1-003 — Top 2 Equal-weight Diversification

## Decision

`REJECT — DEVELOPMENT HYPOTHESIS`

R1-002의 126-day absolute-momentum risk-off를 유지하고 selection만 Top 1에서 Top 2 equal-weight로 변경했다. 2023–2025 Final OOS는 다운로드하거나 조회하지 않았다.

## Hypothesis and Fixed Design

- Hypothesis: Top 2 동일가중이 single-name concentration과 MDD를 낮추면서 momentum premium의 상당 부분을 보존한다.
- Universe: AMD, TSLA, AMZN, AAPL (ex-post selected; selection/survivorship bias 가능)
- Development period: 2015-01-02–2022-12-30
- Signal: 기존 21/63/126-day relative momentum 동일가중
- Risk-off: 각 Top 2 후보의 126-day absolute momentum이 0 이하이면 해당 50% slot을 cash로 유지
- Rebalance/execution: 5거래일마다 종가 signal, 다음 거래일 시가 target-weight execution
- Benchmark: SPY primary, universe equal-weight buy-and-hold secondary
- Costs: commission 0bps, one-way slippage 0/5/10/20bps
- Parameter search: 없음. Top N 또는 weight 조합을 추가 탐색하지 않음.

## Cost Robustness

| Slippage | Return | CAGR | Ann. vol | MDD | Sharpe | Sortino | Calmar | Turnover | Trade records |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0bps | 1,646.73% | 46.54% | 39.98% | -47.60% | 1.155 | 1.530 | 0.978 | 92.43x | 740 |
| 5bps | 1,567.65% | 45.64% | 39.96% | -47.58% | 1.140 | 1.510 | 0.959 | 92.40x | 740 |
| 10bps | 1,492.38% | 44.74% | 39.95% | -47.57% | 1.125 | 1.490 | 0.941 | 92.38x | 741 |
| 20bps | 1,351.64% | 42.96% | 39.92% | -47.54% | 1.094 | 1.451 | 0.904 | 92.32x | 740 |

## 10bps Baseline Comparison

| Metric | R1-002 Top 1 | R1-003 Top 2 | Change |
|---|---:|---:|---:|
| Return | 3,910.64% | 1,492.38% | -2,418.26%p |
| CAGR | 63.75% | 44.74% | -19.01%p |
| Annual volatility | 60.42% | 39.95% | -20.47%p |
| MDD | -64.18% | -47.57% | +16.62%p |
| Sharpe | 1.111 | 1.125 | +0.013 |
| Sortino | 1.560 | 1.490 | -0.070 |
| Calmar | 0.993 | 0.941 | -0.053 |
| Turnover | 134.56x | 92.38x | -42.18x |
| Trade records | 116 | 741 | +625 |

10bps에서 SPY 대비 excess return은 1,380.21%p, universe equal-weight 대비 excess return은 683.41%p로 양수를 유지했다. 그러나 CAGR은 baseline의 약 70% 수준으로 감소했고 Calmar와 Sortino가 개선되지 않았다.

## Temporal Diagnostic — 10bps

| Period | R1-002 return | R1-003 return | R1-002 MDD | R1-003 MDD | R1-002 Sharpe | R1-003 Sharpe |
|---|---:|---:|---:|---:|---:|---:|
| 2015–2016 | 384.30% | 113.52% | -40.28% | -33.84% | 1.825 | 1.391 |
| 2017–2018 | 41.29% | 76.56% | -52.60% | -31.00% | 0.600 | 1.058 |
| 2019–2020 | 1,192.14% | 463.72% | -60.63% | -47.57% | 2.142 | 2.005 |
| 2021–2022 | -56.48% | -27.74% | -64.18% | -42.73% | -0.672 | -0.311 |

Downside 완화는 여러 구간에서 관찰되며 특히 2021–2022에서 뚜렷하다. 다만 강한 momentum 구간인 2015–2016과 2019–2020에서 premium 희석이 컸다.

## Concentration Diagnostic — 10bps

이 지표는 거래원장에 기록된 매도 실현손익을 종목별로 합산한 진단이며, 보유 중 미실현손익과 경로 상호작용을 포함하는 완전한 portfolio return attribution이 아니다.

| Strategy | AMD | TSLA | AMZN | AAPL | Dominant | Max absolute realized-P&L share |
|---|---:|---:|---:|---:|---|---:|
| R1-002 | $456,952 | $4,637,149 | $104,509 | -$1,287,970 | TSLA | 71.49% |
| R1-003 | $1,634 | $1,570,004 | $155,430 | -$234,693 | TSLA | 80.03% |

Top 2가 가격 노출과 volatility는 분산했지만 실현손익의 single-name concentration은 낮추지 못했다. TSLA가 여전히 지배적이며 명시적으로 요청된 concentration 성공 기준에는 실패했다.

## Conclusion

`REJECT`

MDD와 volatility, 2021–2022 downside는 실질적으로 개선되었고 Sharpe도 소폭 상승했다. 그러나 Calmar와 Sortino가 하락하고 CAGR 감소가 컸으며, 핵심 가설인 single-name P&L concentration도 악화되었다. 따라서 사전 등록된 공동 기준상 R1-003을 채택하지 않는다. R1-002를 development candidate로 유지하며 Top 3 또는 다른 weight로 즉시 재튜닝하지 않는다.

## Known Limitations

- Universe는 ex-post selected이므로 selection/survivorship bias 가능성이 있다.
- Yahoo/yfinance adjusted data는 institutional-grade point-in-time dataset이 아니다.
- 고정 bps slippage 외 spread, market impact, tax, FX는 포함하지 않는다.
- realized-P&L concentration은 완전한 return attribution이 아니다.
- Final OOS는 아직 봉인되어 있으므로 이 판정은 development hypothesis에 한정된다.
