# R1-002 — 126-day Absolute Momentum Risk-off

## Decision

`ACCEPT — DEVELOPMENT HYPOTHESIS ONLY`

R1-001 baseline은 소급 변경하지 않는다. 이 판정은 risk-off 가설이 development 구간에서 후속 candidate로 유지할 가치가 있다는 의미이며, final strategy 채택을 의미하지 않는다. 2023–2025 final OOS는 미다운로드·미조회 상태다.

## Hypothesis and Single Change

선택된 winner의 기존 126일 absolute momentum이 `<= 0`이면 다음 거래일 시가부터 cash를 보유한다. Universe, relative momentum 21/63/126, factor weight, Top 1, 5일 rebalance, 비용과 benchmark는 R1-001과 동일하다.

경제적 근거는 상대적으로 가장 강한 종목도 중기 절대수익률이 음수라면 전체 위험자산 국면이 약할 가능성이 높다는 것이다.

## Primary Results — Cost Robustness

| Slippage | Return | CAGR | Ann. vol | MDD | Sharpe | Sortino | Calmar | Turnover | Trades | Risk-off signals |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0bps | 4,404.07% | 66.31% | 60.43% | -62.50% | 1.137 | 1.596 | 1.061 | 135.35x | 116 | 33 |
| 5bps | 4,150.02% | 65.02% | 60.42% | -63.35% | 1.124 | 1.578 | 1.026 | 134.96x | 116 | 33 |
| 10bps | 3,910.64% | 63.75% | 60.42% | -64.18% | 1.111 | 1.560 | 0.993 | 134.56x | 116 | 33 |
| 20bps | 3,471.34% | 61.23% | 60.41% | -65.80% | 1.086 | 1.525 | 0.931 | 133.76x | 116 | 33 |

## 10bps Baseline Comparison

| Metric | R1-001 baseline | R1-002 risk-off | Change |
|---|---:|---:|---:|
| Return | 3,558.20% | 3,910.64% | +352.44%p |
| CAGR | 61.75% | 63.75% | +2.00%p |
| Annual volatility | 62.01% | 60.42% | -1.59%p |
| MDD | -71.01% | -64.18% | +6.83%p |
| Sharpe | 1.079 | 1.111 | +0.032 |
| Sortino | 1.580 | 1.560 | -0.020 |
| Calmar | 0.870 | 0.993 | +0.123 |
| Turnover | 142.06x | 134.56x | -7.50x |
| Trade records | 119 | 116 | -3 |

Cash 보유일은 163/1,888 평가일이다. MDD, Sharpe, Calmar, volatility와 turnover는 개선됐으나 Sortino는 소폭 악화했다.

## Temporal Robustness — 10bps

| Period | Baseline | Risk-off | SPY | Equal-weight | Risk-off MDD | Risk-off Sharpe |
|---|---:|---:|---:|---:|---:|---:|
| 2015–2016 | 408.4% | 384.3% | 11.7% | 83.3% | -40.3% | 1.82 |
| 2017–2018 | 34.3% | 41.3% | 15.3% | 68.4% | -52.6% | 0.60 |
| 2019–2020 | 1,425.9% | 1,192.1% | 55.1% | 342.0% | -60.6% | 2.14 |
| 2021–2022 | -63.8% | -56.5% | 6.8% | -35.0% | -64.2% | -0.67 |

사전 등록한 2021–2022 downside는 7.3%p 개선됐지만 여전히 두 benchmark보다 나쁘며 손실 규모도 크다. Risk-off는 문제를 완화했지만 해결하지 못했다.

## TSLA Exclusion Diagnostic — 10bps

이 결과는 baseline 변경이나 parameter tuning에 사용하지 않는다.

| Metric | TSLA-excluded baseline | TSLA-excluded risk-off |
|---|---:|---:|
| Return | 790.33% | 916.63% |
| CAGR | 33.92% | 36.32% |
| Annual volatility | 52.85% | 51.29% |
| MDD | -57.93% | -50.31% |
| Sharpe | 0.809 | 0.852 |
| Sortino | 1.213 | 1.219 |
| Calmar | 0.586 | 0.722 |
| Turnover | 141.68x | 130.24x |

TSLA를 제외해도 risk-off의 downside/risk-adjusted 개선 방향은 유지됐다. 다만 primary 결과의 절대 수익이 TSLA에 크게 의존한다는 R1-001 진단도 재확인됐다.

## Conclusion

`ACCEPT`

Risk-off는 네 비용 조건에서 결과 방향을 유지했고, primary 및 TSLA 제외 diagnostic 모두에서 MDD와 Sharpe/Calmar를 개선했다. 2021–2022 downside도 개선했으므로 단일 가설의 개발단계 성공 기준을 대체로 충족한다.

제약은 명확하다. Sortino가 primary에서 소폭 악화했고, MDD -64.18%는 여전히 매우 크며, TSLA 집중과 ex-post universe bias는 해결되지 않았다. 따라서 R1-002는 후속 candidate로 유지하되 final OOS를 열거나 최종 채택하지 않는다.
