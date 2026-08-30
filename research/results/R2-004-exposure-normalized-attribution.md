# R2-004 — Exposure-normalized Return Attribution

## Classification

`CAPITAL_SCALING`

Frozen R1-002의 2019–2020 TSLA dollar contribution을 단위 노출당 return과 portfolio notional로 분리했다. Final OOS는 조회하지 않았다.

## Primary Comparison

| Metric | TSLA | Pooled other holdings | Difference/ratio |
|---|---:|---:|---:|
| Overnight observations | 303 | 170 | — |
| Mean overnight return | 0.564% | 0.285% | +0.279%p |
| Median overnight return | 0.629% | 0.256% | +0.373%p |
| Daily overnight volatility | 3.552% | 1.931% | +1.621%p |
| Positive hit rate | 62.05% | 57.06% | +4.987%p |
| Average prior-close notional | $3.21M | $0.81M | 3.94x |
| Median prior-close notional | $2.24M | $0.73M | 3.08x |
| Exposure-weighted overnight return | 0.515% | 0.243% | +0.272%p |
| Total overnight dollar P&L | $5.01M | $0.34M | — |

R2-003의 302 observations는 overnight contribution이 정확히 0인 날을 제외했다. R2-004의 303 observations는 exposure-normalized return 분포를 위해 보유 중 zero-gap day도 포함한다.

## Pre-registered Classification Test

### Return edge

두 조건을 모두 요구했다.

1. Mean overnight return advantage ≥0.10%p: 통과, +0.279%p
2. Positive hit-rate advantage ≥5%p: 미통과, +4.987%p

Hit-rate가 threshold보다 약 0.013%p 낮다. 매우 경계적인 결과지만 threshold를 소급 완화하지 않으므로 `RETURN_EDGE`로 분류하지 않는다.

### Capital scaling

Average prior-close notional ratio ≥1.5x를 요구했다. 실제 ratio는 3.94x이므로 명확히 통과한다.

최종 분류는 `CAPITAL_SCALING`이다.

## TSLA Period Diagnostic

| Period | Observations | Mean overnight | Median overnight | Hit rate | Average notional | Exposure-weighted return | Dollar P&L |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2015–2016 | 5 | 0.252% | 1.196% | 60.00% | $0.09M | 0.223% | $1,053 |
| 2017–2018 | 110 | 0.105% | 0.190% | 58.18% | $0.48M | 0.091% | $47,742 |
| 2019–2020 | 303 | 0.564% | 0.629% | 62.05% | $3.21M | 0.515% | $5,007,569 |
| 2021–2022 | 177 | 0.206% | 0.231% | 55.93% | $8.00M | 0.161% | $2,281,765 |

2021–2022의 average notional은 2019–2020보다 약 2.49배 컸지만 exposure-weighted overnight return은 0.515%에서 0.161%로 낮아졌다. 따라서 dollar 규모에는 capital scaling이 중요하지만 2019–2020의 더 강한 return regime도 경제적으로 중요한 diagnostic이다.

## Combined Interpretation

- 높은 dollar P&L은 커진 portfolio notional의 영향을 명확히 받았다.
- 동시에 TSLA의 단위 노출당 overnight return은 pooled others보다 높고 volatility도 컸다.
- 사전 정량 기준상 return-edge hit-rate를 근소하게 통과하지 못했으므로 공식 분류는 capital scaling만 유지한다.
- 가장 균형 잡힌 해석은 “2019–2020의 강한 TSLA overnight regime가 복리로 커진 자본에 적용되면서 dollar contribution이 확대됐다”이다.

## Stop Rule

- Threshold를 완화하거나 comparison group을 바꾸지 않는다.
- Volatility targeting, position cap, overnight hedge 또는 execution 변경을 도입하지 않는다.
- 추가 development attribution을 진행하지 않는다.
- Final OOS는 이중확인 gate로 봉인한다.
