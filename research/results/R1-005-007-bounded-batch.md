# R1-005–R1-007 — Bounded Development Batch

## Batch Outcome

| Experiment | Decision | Single change |
|---|---|---|
| R1-005 | `REJECT` | Composite score / trailing 63-day volatility |
| R1-006 | `REJECT` | Positive 126-day breadth가 2/4 미만이면 cash |
| R1-007 | `REJECT` | SPY 126-day momentum이 0 이하이면 cash |

세 가설은 결과 조회 전에 함께 고정했고 R1-002에 각각 독립 적용했다. 중간 결과에 따라 설정을 변경하지 않았다. Final OOS 2023–2025는 다운로드하거나 조회하지 않았다.

## Common Acceptance Rule

10bps에서 Sharpe/Sortino/Calmar 중 최소 2개 개선, 어느 것도 0.05 초과 악화 없음, MDD 악화 3%p 이내, CAGR 80% 이상 보존, 양의 benchmark excess return, turnover 증가 20% 이내를 모두 요구했다. 비용 조건과 2년 구간 및 realized-P&L concentration을 함께 진단했다.

## Primary Comparison — 10bps

| Metric | R1-002 | R1-005 | R1-006 | R1-007 |
|---|---:|---:|---:|---:|
| Return | 3,910.64% | 1,853.27% | 3,251.98% | 2,203.06% |
| CAGR | 63.75% | 48.74% | 59.87% | 52.05% |
| Annual volatility | 60.42% | 55.13% | 58.75% | 54.06% |
| MDD | -64.18% | -62.81% | -64.24% | -57.20% |
| Sharpe | 1.111 | 0.987 | 1.086 | 1.038 |
| Sortino | 1.560 | 1.355 | 1.455 | 1.318 |
| Calmar | 0.993 | 0.776 | 0.932 | 0.910 |
| Turnover | 134.56x | 159.09x | 120.18x | 104.39x |
| Trade records | 116 | 160 | 116 | 100 |
| Max absolute realized-P&L share | 71.49% | 63.96% | 86.13% | 66.78% |

세 실험 모두 SPY와 universe equal-weight benchmark 대비 양의 excess return을 유지했다. 그러나 세 실험 모두 Sharpe, Sortino와 Calmar가 R1-002보다 하락했다.

## Cost Robustness

### R1-005

| Slippage | CAGR | MDD | Sharpe | Sortino | Calmar | Turnover |
|---:|---:|---:|---:|---:|---:|---:|
| 0bps | 51.96% | -62.03% | 1.026 | 1.408 | 0.838 | 159.29x |
| 5bps | 50.34% | -62.32% | 1.007 | 1.381 | 0.808 | 159.19x |
| 10bps | 48.74% | -62.81% | 0.987 | 1.355 | 0.776 | 159.09x |
| 20bps | 45.60% | -63.76% | 0.949 | 1.303 | 0.715 | 158.90x |

### R1-006

| Slippage | CAGR | MDD | Sharpe | Sortino | Calmar | Turnover |
|---:|---:|---:|---:|---:|---:|---:|
| 0bps | 62.37% | -63.66% | 1.112 | 1.490 | 0.980 | 120.36x |
| 5bps | 61.11% | -63.95% | 1.099 | 1.472 | 0.956 | 120.27x |
| 10bps | 59.87% | -64.24% | 1.086 | 1.455 | 0.932 | 120.18x |
| 20bps | 57.41% | -64.81% | 1.060 | 1.420 | 0.886 | 119.98x |

### R1-007

| Slippage | CAGR | MDD | Sharpe | Sortino | Calmar | Turnover |
|---:|---:|---:|---:|---:|---:|---:|
| 0bps | 54.10% | -56.86% | 1.063 | 1.349 | 0.951 | 104.61x |
| 5bps | 53.07% | -57.03% | 1.050 | 1.333 | 0.931 | 104.50x |
| 10bps | 52.05% | -57.20% | 1.038 | 1.318 | 0.910 | 104.39x |
| 20bps | 50.04% | -57.55% | 1.013 | 1.288 | 0.870 | 104.15x |

## Temporal Diagnostic — 10bps

| Period | R1-002 return | R1-005 return | R1-006 return | R1-007 return |
|---|---:|---:|---:|---:|
| 2015–2016 | 384.30% | 278.18% | 311.34% | 415.47% |
| 2017–2018 | 41.29% | 11.24% | 32.89% | 34.87% |
| 2019–2020 | 1,192.14% | 522.43% | 927.68% | 472.06% |
| 2021–2022 | -56.48% | -28.44% | -42.75% | -44.44% |

세 후보 모두 2021–2022 downside는 개선했지만 강한 momentum 구간의 premium을 희생했다. 전체기간 risk-adjusted 성과 개선으로 이어지지 않았으므로 이 diagnostic만으로 ACCEPT 기준을 변경하지 않았다.

## Individual Decisions

### R1-005 — REJECT

Concentration은 71.49%에서 63.96%, 2021–2022 손실은 -56.48%에서 -28.44%로 개선됐다. 그러나 CAGR 보존율이 76.46%로 80% 기준에 미달했고 Sharpe, Sortino, Calmar가 모두 악화됐다. Turnover도 18.23% 증가했다.

### R1-006 — REJECT

Turnover와 최근 downside는 개선됐지만 Sharpe, Sortino, Calmar가 모두 하락했다. 특히 TSLA 중심 realized-P&L concentration이 86.13%로 크게 상승했다.

### R1-007 — REJECT

MDD는 6.21%p, concentration은 4.71%p 개선됐고 CAGR은 baseline의 약 81.65%를 보존했다. 하지만 Sharpe -0.073, Sortino -0.242, Calmar -0.083으로 모두 공통 허용 범위를 통과하지 못했다.

## Stop Rule and Limitations

- R1-005~R1-007 bounded batch를 종료한다.
- 다른 volatility window, breadth threshold 또는 SPY regime lookback을 탐색하지 않는다.
- R1-002를 development candidate로 유지하며 최종 전략으로 채택하지 않는다.
- Ex-post universe selection과 Yahoo 데이터 한계가 남아 있다.
- Fixed-bps 모델은 spread, impact, tax와 FX를 포함하지 않는다.
- Realized-P&L concentration은 완전한 return attribution이 아니다.
- Final OOS는 계속 봉인한다.
