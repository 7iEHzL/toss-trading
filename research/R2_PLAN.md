# R2 Robustness and Dependency Audit Plan

## Status

`R2 COMPLETE — R2-004: CAPITAL_SCALING`

## Objective

R2는 R1-002의 수익을 높이기 위한 parameter tuning 단계가 아니다. Frozen R1-002 development candidate가 특정 종목, 특정 기간 또는 연구 데이터 구성에 얼마나 의존하는지 정량화하고 Final OOS 개봉 전 해석 위험을 줄이는 단계다.

## Fixed Inputs

- Candidate: frozen R1-002 configuration
- Development snapshot: 2015–2022 only
- Universe: AMD, TSLA, AMZN, AAPL
- Benchmarks, costs, signal/execution: R1 protocol 유지
- Final OOS: double-confirmation gate로 봉인

## R2-001 Pre-registration — Leave-one-out Universe Dependency Audit

### Research Question

R1-002의 development 성과가 universe의 특정 단일 종목 포함 여부에 과도하게 의존하는가?

### Hypothesis

R1-002가 일반적인 cross-sectional momentum 효과라면 AMD, TSLA, AMZN, AAPL 중 하나를 각각 제외해도 risk-adjusted 성과와 benchmark excess의 방향이 유지되어야 한다.

### Design

- Full universe R1-002를 reference로 사용한다.
- AMD, TSLA, AMZN, AAPL을 각각 한 번씩 제외한 네 diagnostic을 모두 실행한다.
- 모든 diagnostic은 결과와 관계없이 보고한다.
- 제외 결과를 이용해 새로운 universe를 선택하거나 baseline을 변경하지 않는다.
- Primary cost 10bps, robustness 0/5/10/20bps.
- Metrics: CAGR, MDD, Sharpe, Sortino, Calmar, turnover, trades, benchmark excess와 realized-P&L concentration.

### Dependency Classification

- `CONCENTRATED`: 어느 하나의 종목 제외로 CAGR이 full-universe 대비 30% 이상 감소하거나 Sharpe가 0.20 이상 감소하거나 benchmark excess가 음수로 전환.
- `DIRECTIONALLY_ROBUST`: 네 제외 결과 모두 위 concentration trigger를 피하고 두 benchmark 대비 excess return이 양수.
- `MIXED`: 데이터 또는 metric 방향이 충돌해 위 두 분류가 명확하지 않음.

이 분류는 전략 ACCEPT/REJECT가 아니라 universe dependency 진단이다.

## R2-001 Stop Rule

- 네 leave-one-out 결과를 모두 확인한 뒤 종료한다.
- 가장 성과가 좋은 subset을 새 universe로 채택하지 않는다.
- 추가 조합 제거, Top N 또는 parameter search를 하지 않는다.

## R2-001 Result

`CONCENTRATED`

TSLA 제외 시 10bps CAGR이 63.75%에서 36.32%로 43.03% 감소하고 Sharpe가 1.111에서 0.852로 0.259 하락했다. 사전등록한 두 concentration trigger를 충족한다. 모든 leave-one-out 결과의 SPY excess는 양수였지만 TSLA 제외 시 universe equal-weight 대비 excess는 17.15%p로 크게 축소됐다.

AAPL 제외 결과는 full universe보다 개선됐지만 audit 결과를 이용해 AAPL을 제거하거나 universe를 재선정하지 않는다. R2-001은 dependency 진단으로 종료하며 추가 subset 조합을 탐색하지 않는다.

## R2-002 Pre-registration — P&L Source Attribution

### Research Question

R1-002의 TSLA dependency는 단순히 더 오래 보유해서인지, 보유 중 가격 상승이 커서인지, 소수 대형 실현거래 또는 특정 시간 구간에 집중됐기 때문인지?

### Scope

- Frozen R1-002의 10bps primary result만 진단한다.
- 전략 parameter, universe, signal 또는 execution을 변경하지 않는다.
- Final OOS를 조회하지 않는다.

### Exact Daily Decomposition

각 거래일의 종목별 가격 기여를 다음처럼 계산한다.

```text
overnight contribution = previous-close quantity × (today open - previous close)
intraday contribution  = post-open-trade quantity × (today close - today open)
net contribution       = overnight + intraday - commission - slippage cost
```

모든 종목의 net contribution 합은 portfolio equity의 일별 변화와 일치해야 한다. 허용 reconciliation error는 일별 USD 1e-6, 전체 USD 1e-4다.

### Diagnostics

- 종목별 overnight, intraday, execution cost와 net contribution
- 종목별 close-to-close holding days 및 holding-day share
- 매도 거래별 realized P&L과 최대 절대 거래 비중
- 2015–2016, 2017–2018, 2019–2020, 2021–2022 종목별 net contribution
- 종목별 absolute contribution share와 net-profit contribution ratio

### Interpretation Rule

- `EXPOSURE_DRIVEN`: dominant 종목의 holding-day share와 absolute contribution share가 모두 가장 큼.
- `PAYOFF_DRIVEN`: holding-day share는 최대가 아니거나 absolute contribution share보다 현저히 낮지만 가격 contribution이 지배적.
- `TRADE_OUTLIER_DRIVEN`: 한 매도 거래가 전체 absolute realized-P&L의 30% 이상.
- `PERIOD_CONCENTRATED`: 한 2년 구간이 dominant 종목 positive contribution의 60% 이상.
- 여러 조건이 동시에 충족되면 복수 원인으로 분류한다.

이 기준은 전략 ACCEPT/REJECT 또는 universe 변경에 사용하지 않는다.

## R2-002 Result

`PAYOFF_DRIVEN + PERIOD_CONCENTRATED`

- TSLA holding-day share는 34.49%로 AMD의 38.84%보다 낮지만 absolute net contribution share는 71.49%, gross daily P&L path share는 68.24%다. 따라서 단순 보유기간보다 payoff 크기가 지배 원인이다.
- TSLA net contribution은 overnight +$7.34M, intraday -$2.59M, execution cost -$0.11M으로 구성된다. 수익 원천은 장중 상승이 아니라 overnight gap이다.
- TSLA의 2019–2020 contribution은 +$8.34M이며 2021–2022에는 -$3.68M이다. Positive contribution이 한 2년 구간에 60% 이상 집중되어 `PERIOD_CONCENTRATED`다.
- 최대 단일 실현거래는 TSLA +$3.64M이며 전체 absolute realized-P&L의 21.09%로 30% threshold 미만이다. `TRADE_OUTLIER_DRIVEN`은 아니다.
- 일별 최대 reconciliation error는 $1.6e-9, 전체 error는 $2.6e-9로 허용치 이내다.

R2-002는 attribution audit로 종료하며 결과를 이용해 execution timing, universe 또는 parameter를 사후 변경하지 않는다.

## R2-003 Pre-registration — Overnight Gap Concentration

### Research Question

2019–2020 TSLA overnight contribution은 소수 극단 gap에서 발생했는가, 아니면 다수의 양의 overnight return이 누적된 결과인가?

### Scope and Metrics

- Frozen R1-002 10bps attribution만 사용한다.
- Symbol/period: TSLA, 2019-01-01–2020-12-31.
- 양의 overnight contribution 일수, 음의 일수, 합계, 평균, 중앙값을 기록한다.
- 양의 overnight contribution 중 top 1/5/10 day share와 HHI를 기록한다.
- 가장 큰 양·음의 overnight contribution 날짜와 금액을 기록한다.
- 전략, execution, universe 또는 parameter를 변경하지 않는다.

### Classification

- `EXTREME_GAP_DRIVEN`: 최대 1일이 positive overnight 합계의 20% 이상이거나 상위 5일이 50% 이상.
- `DISTRIBUTED`: 상위 5일이 30% 미만이고 positive overnight day가 30일 이상.
- `MIXED`: 위 두 조건 사이.

### Stop Rule

- 위 고정 분포만 계산하고 threshold 또는 기간을 변경하지 않는다.
- 결과를 이용해 close execution이나 overnight hedge를 사후 도입하지 않는다.
- Final OOS는 봉인한다.

## R2-003 Result

`DISTRIBUTED`

- Observation days 302: positive 188, negative 114.
- Positive overnight total +$14.13M, negative total -$9.12M, net +$5.01M.
- Top 1 positive day share 4.65%, top 5 14.07%, top 10 23.39%, positive HHI 0.0122.
- Largest positive day: 2020-11-17, +$657,684.
- Largest negative day: 2020-09-08, -$786,998.

상위 5일 비중이 30% 미만이고 양의 overnight day가 30일 이상이므로 사전 기준상 `DISTRIBUTED`다. TSLA payoff는 2019–2020이라는 구간에는 집중됐지만 그 구간 안에서는 소수 extreme gap이 아니라 많은 overnight observation에 분산됐다.

## R2-004 Pre-registration — Exposure-normalized Return Attribution

### Research Question

TSLA의 큰 dollar contribution은 단위 투자금당 overnight return 우위인가, 복리로 커진 portfolio notional 효과인가, 아니면 둘 다인가?

### Scope

- Frozen R1-002 10bps 결과만 사용한다.
- Primary comparison: 2019–2020 TSLA overnight observations와 같은 기간 다른 보유종목의 pooled observations.
- Secondary diagnostic: TSLA의 다른 2년 구간 및 종목별 전체 보유기간 분포.
- Final OOS는 다운로드하거나 조회하지 않는다.

### Metrics

- Equal-observation overnight/intraday mean, median, volatility와 positive hit rate
- Exposure-weighted overnight/intraday return
- Average and median prior-close/open notional
- Observation count 및 period별 동일 지표

### Classification

- `RETURN_EDGE`: TSLA 2019–2020 mean overnight return이 pooled others보다 0.10%p/day 이상 높고 positive hit rate도 5%p 이상 높음.
- `CAPITAL_SCALING`: TSLA average prior-close overnight notional이 pooled others의 1.5배 이상.
- `BOTH`: 두 조건 모두 충족.
- `INCONCLUSIVE`: 어느 조건도 충족하지 않거나 표본이 없어 직접 비교 불가.

Median, volatility와 exposure-weighted return은 classification을 바꾸지 않는 필수 diagnostic이다.

### Stop Rule

- Threshold, period 또는 comparison group을 결과 확인 후 변경하지 않는다.
- 결과를 이용해 position sizing, execution timing, universe 또는 parameter를 변경하지 않는다.
- R2-004 후 추가 development attribution을 진행하지 않고 R2 completion으로 이동한다.

## R2-004 Result

`CAPITAL_SCALING`

- TSLA 2019–2020 mean overnight return 0.564%, pooled others 0.285%: +0.279%p/day.
- Positive hit rate 62.05% vs 57.06%: +4.987%p로 사전 5%p threshold를 0.013%p 하회.
- Average prior-close notional $3.21M vs $0.81M: 3.94x로 1.5x threshold 충족.
- Median notional $2.24M vs $0.73M: 3.08x.
- Exposure-weighted overnight return 0.515% vs 0.243%.

사전 규칙상 return edge는 mean과 hit-rate 조건을 모두 요구하므로 `RETURN_EDGE`는 부여하지 않는다. 다만 threshold 경계에 매우 가까우며 median 및 exposure-weighted return도 높은 점은 필수 diagnostic으로 보존한다. Capital scaling은 명확하다.

R2-004를 끝으로 추가 development attribution을 중단하고 R2를 종료한다.
