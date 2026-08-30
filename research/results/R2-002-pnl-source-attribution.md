# R2-002 — P&L Source Attribution

## Classification

`PAYOFF_DRIVEN + PERIOD_CONCENTRATED`

`TRADE_OUTLIER_DRIVEN`과 단순 holding-duration 기반 `EXPOSURE_DRIVEN`은 확인되지 않았다.

## Method

Frozen R1-002 10bps 결과의 일별 equity 변화를 다음과 같이 분해했다.

```text
overnight = previous-close quantity × (today open - previous close)
intraday  = post-open-trade quantity × (today close - today open)
net       = overnight + intraday - commission - slippage
```

일별 최대 reconciliation error는 $1.57e-9, 전체 error는 $2.62e-9로 사전 허용치보다 작다. Final OOS는 조회하지 않았다.

## Symbol-level Attribution

| Symbol | Holding days | Holding share | Overnight | Intraday | Costs | Net contribution | Absolute net share | Gross path share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TSLA | 595 | 34.49% | $7,338,129 | -$2,592,153 | -$108,828 | $4,637,149 | 71.49% | 68.24% |
| AMD | 670 | 38.84% | $1,374,555 | -$836,126 | -$81,477 | $456,952 | 7.04% | 20.22% |
| AMZN | 325 | 18.84% | $312,220 | -$132,345 | -$75,366 | $104,509 | 1.61% | 4.11% |
| AAPL | 135 | 7.83% | -$794,442 | -$406,445 | -$87,083 | -$1,287,970 | 19.86% | 7.43% |

TSLA는 가장 오래 보유한 종목이 아니다. AMD의 holding share가 더 높지만 TSLA의 absolute net contribution은 전체의 71.49%다. 따라서 dependency는 보유시간보다 보유 중 payoff 크기로 설명된다.

또한 TSLA intraday contribution은 음수다. 전체 양의 기여는 overnight gap에서 발생했으며, 이는 다음 시가 체결을 사용하는 전략에서도 기존 보유분의 overnight exposure가 핵심 수익 원천이었음을 뜻한다.

## Period Attribution

| Period | AMD | TSLA | AMZN | AAPL | Total |
|---|---:|---:|---:|---:|---:|
| 2015–2016 | $355,357 | -$4,881 | $33,821 | $0 | $384,297 |
| 2017–2018 | $7,584 | -$18,886 | $225,023 | -$8,347 | $205,374 |
| 2019–2020 | -$194,236 | $8,339,227 | $0 | $76,853 | $8,221,844 |
| 2021–2022 | $288,247 | -$3,678,311 | -$154,335 | -$1,356,476 | -$4,900,875 |

TSLA의 양의 period contribution은 사실상 2019–2020 한 구간에서 발생했다. 이후 2021–2022에 약 $3.68M을 되돌렸다. 사전 60% threshold를 충족하므로 `PERIOD_CONCENTRATED`다.

## Largest Realized Trades

| Rank | Execution date | Symbol | Realized P&L |
|---:|---|---|---:|
| 1 | 2021-05-14 | TSLA | $3,643,686 |
| 2 | 2020-08-05 | TSLA | $3,227,964 |
| 3 | 2022-01-31 | TSLA | -$1,443,662 |
| 4 | 2021-10-27 | AMD | $969,054 |
| 5 | 2021-08-03 | AMZN | -$761,068 |

최대 거래는 전체 absolute realized-P&L의 21.09%다. 30% threshold보다 작으므로 한 거래만으로 결과가 만들어진 `TRADE_OUTLIER_DRIVEN`은 아니다. 다만 상위 두 양의 거래가 모두 TSLA라는 사실은 payoff concentration과 일치한다.

## Answer to the Research Question

R1-002의 TSLA 집중은 다음 순서로 설명된다.

1. 특정 기간의 가격 payoff: 2019–2020 TSLA overnight 상승이 가장 큰 원인
2. 반복된 TSLA payoff: 하나의 거래가 아니라 여러 보유 episode에서 큰 손익 발생
3. 보유 기간: 보조 요인이지만 주원인은 아님. AMD를 더 오래 보유함
4. 단일 대형 거래: 최대 비중이 threshold 미만이므로 주원인 아님

## Limitations and Stop Rule

- Attribution은 frozen development result의 회계적 분해이며 인과 추정이 아니다.
- Overnight gap의 경제적 원인을 설명하지 않는다.
- 현재 universe는 ex-post selected다.
- 결과를 근거로 close execution, TSLA 제거 또는 parameter 변경을 하지 않는다.
- Final OOS는 이중확인 gate로 계속 봉인한다.
