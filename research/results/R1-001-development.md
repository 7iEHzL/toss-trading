# R1-001 Development Baseline Evaluation

## Decision

`INCONCLUSIVE — SECOND OPINION REQUIRED`

이 결과는 2015–2022 development 데이터만 사용했다. 2023–2025 final OOS는 다운로드하거나 조회하지 않았다.

## Hypothesis

기존 Cross-sectional Momentum Rotation은 parameter 변경 없이도 거래비용 적용 후 benchmark 대비 해석 가능한 성과를 보이며, 시간 구간과 특정 종목에 과도하게 의존하지 않는다.

## Fixed Setup

- Primary universe: AMD, TSLA, AMZN, AAPL
- Robustness universe: primary + SPXL
- Momentum: 21/63/126 거래일, 동일 가중
- Selection: Top 1
- Rebalance: 5 거래일
- Signal/execution: 종가 signal, 다음 거래일 시가 execution
- Initial cash: USD 100,000
- Primary benchmark: SPY buy-and-hold
- Secondary benchmark: universe equal-weight buy-and-hold
- Slippage: one-way 0/5/10/20bps
- Commission: 0

## Data Validation

- Source: Yahoo Finance via yfinance 1.2.0
- Requested interval: 2015-01-01 inclusive to 2023-01-01 exclusive
- Actual interval: 2015-01-02 to 2022-12-30
- Symbols: 6
- Rows per symbol: 2,014
- Common trading dates: 2,014
- Missing values: 0
- Duplicate dates: 0
- Adjusted OHLC: yes (`auto_adjust=True`)
- File integrity: per-file SHA-256 recorded and verified on load
- Final OOS downloaded: false

Yahoo/yfinance 데이터는 research baseline 용도이며 institutional-grade로 간주하지 않는다. Universe는 ex-post 선정되어 selection/survivorship bias 가능성이 있다.

## Primary Baseline — Cost Robustness

| Slippage | Cumulative return | CAGR | Ann. vol | MDD | Sharpe | Sortino | Calmar | Turnover | Trade records |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0bps | 4,020.65% | 64.34% | 62.02% | -69.53% | 1.104 | 1.618 | 0.925 | 143.05x | 119 |
| 5bps | 3,782.28% | 63.04% | 62.01% | -70.28% | 1.092 | 1.599 | 0.897 | 142.55x | 119 |
| 10bps | 3,558.20% | 61.75% | 62.01% | -71.01% | 1.079 | 1.580 | 0.870 | 142.06x | 119 |
| 20bps | 3,147.82% | 59.20% | 62.01% | -72.43% | 1.053 | 1.543 | 0.817 | 141.06x | 119 |

비용 증가에도 전체기간 수익 방향은 유지되지만 turnover와 MDD가 매우 높다.

## Benchmarks — Same Evaluation Dates

| Benchmark | Cumulative return | CAGR | Ann. vol | MDD | Sharpe | Sortino | Calmar |
|---|---:|---:|---:|---:|---:|---:|---:|
| SPY | 112.17% | 10.57% | 18.98% | -33.72% | 0.625 | 0.742 | 0.314 |
| Universe equal-weight | 808.97% | 34.29% | 39.20% | -60.25% | 0.949 | 1.334 | 0.569 |

10bps baseline은 두 benchmark보다 전체기간 수익과 risk-adjusted metric이 높지만 절대 MDD는 더 크다.

## Temporal Robustness — 10bps

첫 구간은 126 거래일 warm-up 이후부터 시작한다.

| Period | Strategy return | SPY return | Equal-weight return | Strategy MDD | Strategy Sharpe |
|---|---:|---:|---:|---:|---:|
| 2015–2016 | 408.4% | 11.7% | 83.3% | -42.1% | 1.87 |
| 2017–2018 | 34.3% | 15.3% | 68.4% | -59.8% | 0.55 |
| 2019–2020 | 1,425.9% | 55.1% | 342.0% | -60.6% | 2.24 |
| 2021–2022 | -63.8% | 6.8% | -35.0% | -71.0% | -0.75 |

성과 방향과 위험조정 성과가 구간별로 크게 충돌한다. 특히 가장 최근 development block에서 두 benchmark보다 크게 부진했다.

## Concentration Diagnostics — 10bps

- Holding days: AMD 700, TSLA 620, AMZN 340, AAPL 227
- Realized P&L: AMD -400,706; TSLA +4,811,692; AMZN -836,329; AAPL +688,761 USD
- Final open position: AAPL

실현손익이 TSLA에 크게 집중됐다. 이 값은 미실현손익을 포함한 완전한 종목별 attribution이 아니지만, 단일 종목 의존 가능성을 명확히 보여준다.

## SPXL Robustness

| Slippage | Cumulative return | CAGR | MDD | Sharpe | Turnover | Trade records |
|---:|---:|---:|---:|---:|---:|---:|
| 0bps | 4,910.87% | 68.69% | -65.44% | 1.150 | 151.25x | 125 |
| 5bps | 4,606.96% | 67.29% | -65.95% | 1.136 | 150.78x | 125 |
| 10bps | 4,321.88% | 65.90% | -66.46% | 1.123 | 150.32x | 125 |
| 20bps | 3,802.43% | 63.15% | -67.45% | 1.096 | 149.39x | 125 |

SPXL 포함 시 전체기간 결과는 개선되지만 이는 레버리지 노출 효과와 momentum 효과를 분리하지 못하므로 primary baseline 변경 근거로 사용하지 않는다.

## Conclusion

`INCONCLUSIVE`

비용 강건성과 전체기간 benchmark 초과는 확인됐다. 그러나 -71% MDD, 높은 turnover, 2021–2022의 큰 손실, TSLA 중심의 실현손익 집중 때문에 “안정적인 baseline”이라는 가설은 development 결과만으로 ACCEPT할 수 없다. 반대로 단순 비교 기준으로서의 유용성까지 즉시 REJECT할 근거도 충분하지 않다.

Final OOS는 계속 봉인한다. 다음 연구 질문을 정하기 전에 baseline을 그대로 진단 기준으로 유지할지, risk-control이 없는 구조를 baseline 결함으로 보고 별도의 단순 control을 추가할지 second opinion이 필요하다.
